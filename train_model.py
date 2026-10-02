from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).parent

DATA_FILE = PROJECT_FOLDER / "data" / "messages.csv"
MODEL_FOLDER = PROJECT_FOLDER / "models"

MODEL_FOLDER.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_FILE)

print(f"Total messages: {len(df)}")


# --------------------------------------------------
# 3. Prepare input and target
# --------------------------------------------------

X = df["text"].astype(str)
y = df["label"]


# --------------------------------------------------
# 4. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training messages: {len(X_train)}")
print(f"Testing messages: {len(X_test)}")


# --------------------------------------------------
# 5. Convert text into numerical features
# --------------------------------------------------

print("\nCreating TF-IDF features...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_features=5000
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"Training feature shape: {X_train_tfidf.shape}")
print(f"Testing feature shape: {X_test_tfidf.shape}")


# --------------------------------------------------
# 6. Train Logistic Regression model
# --------------------------------------------------

print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_tfidf, y_train)


# --------------------------------------------------
# 7. Make predictions
# --------------------------------------------------

print("Making predictions...")

y_pred = model.predict(X_test_tfidf)


# --------------------------------------------------
# 8. Evaluate model
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Safe", "Suspicious"]
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 9. Save model and vectorizer
# --------------------------------------------------

model_file = MODEL_FOLDER / "social_engineering_model.joblib"
vectorizer_file = MODEL_FOLDER / "tfidf_vectorizer.joblib"

joblib.dump(model, model_file)
joblib.dump(vectorizer, vectorizer_file)

print("\n==============================")
print("MODEL SAVED")
print("==============================")

print(f"Model: {model_file}")
print(f"Vectorizer: {vectorizer_file}")

print("\nTraining completed successfully!")