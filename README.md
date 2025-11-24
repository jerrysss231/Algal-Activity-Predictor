# PFAS Growth Activity Prediction Tool

## Overview
This project is a Flask-based Web application utilizing machine learning models (XGBoost) and chemical fingerprinting to predict the growth activity inhibition of algae exposed to PFAS. The application features a user-friendly interface that allows researchers to input chemical structures (SMILES) and key environmental parameters (e.g., temperature, light intensity, concentration) to generate real-time predictions validated by a Strict Applicability Domain assessment.

## Prerequisites
*   **Python 3.9** or higher installed.
*   **pip** (Python package installer).

## Installation

1.  **Unzip** the archive to a local directory.
2.  Open a terminal (Command Prompt or PowerShell) and navigate to the project directory.
3.  Install the required dependencies using the following command:

    ```bash
    pip install -r requirements.txt
    ```

    *Note: If you encounter issues installing RDKit via pip, you may use Conda: `conda install -c conda-forge rdkit`.*

## How to Run

1.  In the terminal, ensure you are in the project root directory (where `app.py` is located).
2.  Run the application with the command:

    ```bash
    python app.py
    ```

3.  Once the server starts, you will see a message indicating the server is running (usually `Running on http://127.0.0.1:5000`).
4.  Open your web browser and visit: **http://127.0.0.1:5000**

## Test Data
To verify the functionality, you may use the following sample inputs:
*   **SMILES**: `C(F)(F)(F)C(F)(F)C(=O)O`
*   **Temperature**: `25`
*   **Light intensity**: `4000`
*   **Exposure time**: `4`
*   **Concentration**: `100`
*   **Species**: *Select any option*
*   **Habitat**: *Select any option*

---
**Note:** Please keep the terminal window open while using the web interface.
