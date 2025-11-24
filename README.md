# PFAS Growth Activity Predictor - Standalone Executable

## Overview
This repository contains the standalone executable (`.exe`) for the PFAS Growth Activity Prediction model. This application allows users to predict algae growth activity based on chemical structure (SMILES) and environmental conditions without installing Python or any dependencies.

## How to Use (Quick Start)

**No Python environment setup is required.** Please follow the steps below:

1.  **Download**: Navigate to the `dist` (or `Release`) folder in this repository and download the file named **`PFAS_Predictor.exe`**.
2.  **Run**: Double-click the downloaded `.exe` file on a Windows machine.
    *   *Note: Please allow a few seconds for the application to initialize. A command prompt window (black window) will appear; this is the background server.*
3.  **Access**: The application will automatically open your default web browser and navigate to the prediction interface (`http://127.0.0.1:5000`).
4.  **Predict**: Enter the required parameters (SMILES, Temperature, Light, etc.) and click "Predict Activity".

**Important Notes:**
*   **Do not close the command prompt window** while using the web interface. Closing it will shut down the server.
*   Since this software is a self-packaged academic tool (using PyInstaller) and not digitally signed, Windows Defender or antivirus software might display a warning. You can safely choose "Run anyway" to proceed.

## Example Test Data
To test the functionality, you may use the following values:

*   **SMILES**: `C(F)(F)(F)C(F)(F)C(=O)O` (Perfluorobutanoic acid)
*   **Temperature**: `25`
*   **Light intensity**: `4000`
*   **Exposure time**: `4`
*   **Concentration**: `100`
*   **Species**: *Select any from the dropdown*
*   **Habitat**: *Select any from the dropdown*

---
For any issues regarding the execution, please contact the corresponding author.
