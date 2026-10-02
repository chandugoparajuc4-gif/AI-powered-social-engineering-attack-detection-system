import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Load dataset
data = pd.read_csv("data/messages.csv")

X = data["text"].astype(str)
y = data["label"].astype(str).str.strip().map({
    "0": "safe",
    "1": "suspicious"
})

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Convert text into numerical features
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vectorized, y_train)

# Make predictions
y_pred = model.predict(X_test_vectorized)

# Calculate evaluation metrics
print("\nMODEL EVALUATION")
print("------------------------------")

print("Accuracy:",
      round(accuracy_score(y_test, y_pred) * 100, 2), "%")

print("Precision:",
      round(precision_score(
          y_test, y_pred,
          pos_label="suspicious",
          zero_division=0
      ), 4))

print("Recall:",
      round(recall_score(
          y_test, y_pred,
          pos_label="suspicious",
          zero_division=0
      ), 4))

print("F1 Score:",
      round(f1_score(
          y_test, y_pred,
          pos_label="suspicious",
          zero_division=0
      ), 4))

print("\nCLASSIFICATION REPORT")
print("------------------------------")
print(classification_report(y_test, y_pred, zero_division=0))

print("CONFUSION MATRIX")
print("------------------------------")
print("Labels:", ["safe", "suspicious"])
print(confusion_matrix(
    y_test,
    y_pred,
    labels=["safe", "suspicious"]
))




# Create confusion matrix visualization
cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["safe", "suspicious"]
)

plt.figure(figsize=(7, 5))
plt.imshow(cm, interpolation="nearest")
plt.title("Social Engineering Detection - Confusion Matrix")
plt.colorbar()

labels = ["Safe", "Suspicious"]
plt.xticks([0, 1], labels)
plt.yticks([0, 1], labels)

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")

for i in range(2):
    for j in range(2):
        plt.text(
            j, i, str(cm[i, j]),
            ha="center",
            va="center"
        )

plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=300)
plt.show()

print("Confusion matrix saved as confusion_matrix.png")


# Save evaluation report
report = classification_report(
    y_test,
    y_pred,
    labels=["safe", "suspicious"],
    target_names=["Safe", "Suspicious"],
    zero_division=0
)

with open("evaluation_report.txt", "w", encoding="utf-8") as file:
    file.write("SOCIAL ENGINEERING DETECTION MODEL\n")
    file.write("EVALUATION REPORT\n")
    file.write("=" * 40 + "\n\n")

    file.write(
        f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n\n"
    )

    file.write("Classification Report:\n")
    file.write(report + "\n")

    file.write("Confusion Matrix:\n")
    file.write(str(cm) + "\n")

print("Evaluation report saved as evaluation_report.txt")