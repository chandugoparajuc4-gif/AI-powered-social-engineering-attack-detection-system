
# AI-Powered Social Engineering Detection System

## 1. Project Overview

The AI-Powered Social Engineering Detection System is a
machine learning-based application that analyzes text messages
to identify suspicious patterns and potential social engineering
attacks.

The system uses TF-IDF and Logistic Regression to classify
messages as Safe or Suspicious. It also identifies warning
indicators such as urgent language, suspicious links, threats,
and requests for sensitive information.

## 2. Project Objectives

- Detect potentially suspicious messages.
- Classify messages as Safe or Suspicious.
- Identify common social engineering warning indicators.
- Display suspicious probability and risk levels.
- Maintain analysis history.
- Export analysis history as a CSV file.
- Provide a simple web interface for users.

## 3. Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression
- Flask
- HTML
- CSS
- JavaScript
- Matplotlib
- Joblib

## 4. Project Features

### Message Analysis
Users can enter a message and analyze it using the trained
machine learning model.

### Suspicious Message Detection
The model classifies messages as Safe or Suspicious.

### Warning Indicators
The application checks for indicators such as:
- Urgent language
- Requests for credentials or sensitive information
- Suspicious links
- Threats or intimidation
- Financial requests
- Impersonation or secrecy
- Remote access requests

### Risk Level
The application displays a risk level based on suspicious
probability:
- LOW: below 30%
- MEDIUM: 30% to below 70%
- HIGH: 70% or above

These are project-defined display thresholds, not validated
security ratings.

### Dashboard
The dashboard displays:
- Total analyzed messages
- Suspicious messages
- Safe messages
- High-risk messages

### Analysis History
The application saves recent analyses in browser local storage.

### CSV Export
Users can download their analysis history as a CSV file.

## 5. Project Structure

```text
AI-powered-social-engineering-attack-detection-system/
|
|-- backend/
|   |-- app.py
|
|-- data/
|   |-- messages.csv
|
|-- models/
|   |-- social_engineering_model.joblib
|   |-- tfidf_vectorizer.joblib
|
|-- static/
|   |-- style.css
|   |-- script.js
|
|-- templates/
|   |-- index.html
|
|-- generate_dataset.py
|-- train_model.py
|-- evaluate_model.py
|-- detector.py
|-- evaluation_report.txt
|-- confusion_matrix.png
|-- requirements.txt
|-- README.md
```

## 6. Installation

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd AI-powered-social-engineering-attack-detection-system
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the environment on Windows

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

## 7. Run the Application

Start the Flask application:

```bash
python backend/app.py
```

Open the following address in your browser:

http://127.0.0.1:5000

## 8. Model Evaluation

The model was evaluated using a held-out test set from
the project's synthetic dataset.

| Metric | Result |
|---|---:|
| Accuracy | 93.40% |
| Safe Precision | 1.00 |
| Safe Recall | 0.71 |
| Safe F1-score | 0.83 |
| Suspicious Precision | 0.92 |
| Suspicious Recall | 1.00 |
| Suspicious F1-score | 0.96 |

### Confusion Matrix

| Actual / Predicted | Safe | Suspicious |
|---|---:|---:|
| Safe | 17 | 7 |
| Suspicious | 0 | 82 |

The confusion matrix is saved in `confusion_matrix.png`.

## 9. Dataset

The project uses a synthetic message dataset for development
and initial model evaluation.

The results may not represent performance on real-world
messages. Further testing with independent, representative
datasets is required.

## 10. Limitations

- The training dataset is synthetic.
- New or unfamiliar scam messages may be misclassified.
- Suspicious probability is not a guarantee that a message
  is fraudulent.
- The application is a prototype and should not be used as
  the sole basis for security decisions.

## 11. Future Improvements

- Evaluate using independent public datasets.
- Add more diverse message examples.
- Improve detection of new social engineering techniques.
- Add user authentication and database-backed history.
- Improve model monitoring and performance evaluation.

## 12. Author

Developed as an academic machine learning project.


## Application Screenshot

![Social Engineering Detection System](social-engineering-detector.png)