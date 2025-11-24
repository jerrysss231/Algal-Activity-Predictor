import os
import sys
import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, jsonify, render_template
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from xgboost import XGBRegressor 

# ================= 关键修改：资源路径处理 =================
# 这个函数用于解决打包成 exe 后，临时文件夹路径错乱的问题
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 初始化 Flask，明确告诉它去哪里找 HTML 模板
app = Flask(__name__, template_folder=resource_path('templates'))


# ================= 核心类定义 (保持不变) =================
class StrictApplicabilityDomain:
    def __init__(self, tanimoto_threshold=0.65):
        self.tanimoto_threshold = tanimoto_threshold
        self.ranges = {}
        self.categories = {}
        self.train_fps = []

    def fit(self, df, mol_list, num_cols, cat_cols):
        pass

    def predict(self, mol, meta_dict):
        reasons = []
        if mol is None:
            return False, "Invalid Molecule (SMILES Parse Error)", 0.0

        query_fp = AllChem.GetMACCSKeysFingerprint(mol)
        sims = DataStructs.BulkTanimotoSimilarity(query_fp, self.train_fps)
        max_sim = max(sims) if sims else 0.0

        if max_sim < self.tanimoto_threshold:
            reasons.append(f"Structure Dissimilar (Max Sim: {max_sim:.3f} < {self.tanimoto_threshold})")

        for col, (min_v, max_v) in self.ranges.items():
            val = meta_dict.get(col)
            if val is not None:
                try:
                    val = float(val)
                    if not (min_v <= val <= max_v):
                        reasons.append(f"{col} out of range ({val} not in [{min_v:.2f}, {max_v:.2f}])")
                except:
                    reasons.append(f"Invalid number for {col}")

        for col, allowed_set in self.categories.items():
            val = meta_dict.get(col)
            if val not in allowed_set:
                reasons.append(f"Invalid {col}: '{val}'")

        is_valid = len(reasons) == 0
        reason_str = "; ".join(reasons) if not is_valid else "Pass"
        return is_valid, reason_str, max_sim


# ================= 辅助函数 =================
def standardize_smiles(smiles):
    try:
        rxn_carboxylate = AllChem.ReactionFromSmarts('[CX3:1](=[O:2])[OX2H1:3]>>[CX3:1](=[O:2])[O-:3]')
        rxn_sulfonate = AllChem.ReactionFromSmarts('[SD4:1](=[O:2])(=[O:3])[OX2H1:4]>>[SD4:1](=[O:2])(=[O:3])[O-:4]')
        rxn_sulfonamide = AllChem.ReactionFromSmarts('[N!H0+0;$(N-S(=O)(=O)C(F)(F)):1]>>[N-:1]')
        REACTIONS = [rxn_carboxylate, rxn_sulfonate, rxn_sulfonamide]

        mol = Chem.MolFromSmiles(smiles, sanitize=False)
        if mol is None: return None
        frags = Chem.GetMolFrags(mol, asMols=True)
        if len(frags) > 1:
            mol = max(frags, default=mol, key=lambda m: m.GetNumAtoms())
        Chem.SanitizeMol(mol)

        for rxn in REACTIONS:
            steps = 0
            while steps < 10:
                products = rxn.RunReactants((mol,))
                if products:
                    new_mol = products[0][0]
                    try:
                        Chem.SanitizeMol(new_mol)
                        if Chem.MolToSmiles(new_mol) != Chem.MolToSmiles(mol):
                            mol = new_mol
                            steps += 1
                        else:
                            break
                    except:
                        break
                else:
                    break
        return mol
    except:
        return None


# ================= 加载模型 (使用 resource_path) =================
# 注意：这里使用了 resource_path 来确保 exe 能找到 pkl 文件
ARTIFACTS_PATH = resource_path("model_artifacts_strict.pkl")
artifacts = {}

try:
    print(f"Loading artifacts from {ARTIFACTS_PATH}...")
    artifacts = joblib.load(ARTIFACTS_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load model.\nError: {e}")


# ================= 路由 =================
@app.route('/')
def index():
    options = artifacts.get('unique_options', {'Species': [], 'Habitat': []})
    return render_template('index.html', options=options)


@app.route('/predict', methods=['POST'])
def predict():
    if not artifacts:
        return jsonify({'error': 'Model not loaded properly'}), 500

    try:
        data = request.form
        smiles = data.get('smiles', '').strip()

        try:
            meta_dict = {
                'temperature': float(data.get('temperature')),
                'Light intensity(lux)': float(data.get('light')),
                'Exposure time (d)': float(data.get('time')),
                'PFAS concentration (μg/L)': float(data.get('concentration')),
                'Species': data.get('species'),
                'Habitat': data.get('habitat')
            }
        except ValueError:
            return jsonify({'error': 'Numerical fields error'}), 400

        mol = standardize_smiles(smiles)
        if mol is None:
            return jsonify({'error': 'Invalid SMILES'}), 400

        # AD Check
        ad_model = artifacts['ad_model']
        is_valid_ad, ad_reason, similarity = ad_model.predict(mol, meta_dict)

        # Feature Engineering
        feature_cols = artifacts['train_columns']
        df_input = pd.DataFrame(0, index=[0], columns=feature_cols)

        num_cols = artifacts['feature_names']
        num_indices = artifacts['num_indices']
        scaler = artifacts['scaler']

        raw_nums = [[meta_dict[col] for col in num_cols]]

        species_col = f"Species_{meta_dict['Species']}"
        habitat_col = f"Habitat_{meta_dict['Habitat']}"

        if species_col in df_input.columns:
            df_input[species_col] = 1
        if habitat_col in df_input.columns:
            df_input[habitat_col] = 1

        X_meta = df_input.values.astype(float)
        X_meta[:, num_indices] = scaler.transform(raw_nums)

        arr = np.zeros(167, dtype=int)
        fp = AllChem.GetMACCSKeysFingerprint(mol)
        DataStructs.ConvertToNumpyArray(fp, arr)

        fp_mask = artifacts['fp_mask']
        X_fp_selected = arr[fp_mask].reshape(1, -1)

        X_final = np.hstack([X_meta, X_fp_selected])

        model = artifacts['model']
        prediction = model.predict(X_final)[0]

        result = {
            'prediction': float(prediction),
            'ad_status': 'Pass' if is_valid_ad else 'Warning',
            'ad_message': ad_reason,
            'similarity': float(similarity),
            'standardized_smiles': Chem.MolToSmiles(mol)
        }

        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 自动打开浏览器
    import webbrowser
    from threading import Timer
    
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000")
        
    Timer(1, open_browser).start()
    
    # 生产环境运行
    app.run(port=5000)
if __name__ == '__main__':
    try:
        # 自动打开浏览器
        import webbrowser
        from threading import Timer
        
        def open_browser():
            webbrowser.open_new("http://127.0.0.1:5000")
            
        Timer(1, open_browser).start()
        
        # 生产环境运行
        print("正在启动服务器...")
        app.run(port=5000)
        
    except Exception as e:
        # ==========================================
        # 关键修改：如果出错，打印错误并暂停，不让窗口关闭
        # ==========================================
        import traceback
        print("\n" + "="*60)
        print("程序发生严重错误，无法启动！")
        print("错误详情如下：")
        print("="*60 + "\n")
        traceback.print_exc()
        print("\n" + "="*60)
        input("请按回车键退出...")  # 这行代码会卡住窗口