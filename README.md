# PFAS Growth Activity Prediction Tool

## Project Overview
This project is a Flask-based Web application utilizing machine learning models (XGBoost) and chemical fingerprinting to predict the growth activity inhibition of algae exposed to PFAS. The application features a user-friendly interface that allows researchers to input chemical structures (SMILES) and key environmental parameters to generate real-time predictions validated by a Strict Applicability Domain assessment.

## Repository Contents
*   `app.py`: The main application script.
*   `model_artifacts_strict.pkl`: The pre-trained XGBoost model and artifacts.
*   `requirements.txt`: List of Python dependencies.
*   `index.html`: The frontend interface (Must be placed in a `templates` folder).

## Prerequisites
*   **Python 3.10** or higher.
*   **pip** (Python package installer).

## Installation & Setup

1.  **Clone or Download**:
    Clone this repository or download the ZIP file and extract it.

    ```bash
    git clone https://github.com/jerrysss231/Algal-Activity-Predictor.git
    ```

2.  **Important: Directory Structure Setup**:
    To ensure the application runs correctly, please verify the folder structure. **Flask requires the HTML file to be in a `templates` folder.**
    *   Create a new folder named `templates` in the project root.
    *   Move `index.html` into the `templates` folder.

    The structure should look like this:
    ```text
    Project_Folder/
    ├── app.py
    ├── model_artifacts_strict.pkl
    ├── requirements.txt
    └── templates/
        └── index.html
    ```

3.  **Install Dependencies**:
    Open a terminal in the project directory and run:

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  Start the server:

    ```bash
    python app.py
    ```

2.  Open your web browser and navigate to: **http://127.0.0.1:5000**

## Test Data
To verify the tool's functionality, please use the following inputs:
*   **SMILES**: `C(F)(F)(F)C(F)(F)C(=O)O`
*   **Temperature**: `25`
*   **Light intensity**: `4000`
*   **Exposure time**: `4`
*   **Concentration**: `100`
