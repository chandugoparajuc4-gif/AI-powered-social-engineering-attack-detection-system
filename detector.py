from pathlib import Path
import re

import joblib


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).parent

MODEL_FILE = PROJECT_FOLDER / "models" / "social_engineering_model.joblib"
VECTORIZER_FILE = PROJECT_FOLDER / "models" / "tfidf_vectorizer.joblib"


# --------------------------------------------------
# Load trained model and TF-IDF vectorizer
# --------------------------------------------------

print("Loading trained model...")

model = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)

print("Model loaded successfully.")


# --------------------------------------------------
# Warning indicator rules
# --------------------------------------------------

WARNING_PATTERNS = {
    "Urgent language": [
        r"\burgent\b",
        r"\bimmediately\b",
        r"\basap\b",
        r"\bact now\b",
        r"\bfinal warning\b",
        r"\bquickly\b",
        r"\bwithin \d+ (minutes?|hours?|days?)\b",
    ],

    "Credential or sensitive information request": [
        r"\bpassword\b",
        r"\bpin\b",
        r"\botp\b",
        r"\bverification code\b",
        r"\bsecurity code\b",
        r"\bcard number\b",
        r"\bbank details\b",
        r"\baccount details\b",
        r"\blogin details\b",
    ],

    "Suspicious link": [
        r"https?://",
        r"\bclick (here|this)\b",
        r"\bverify.*link\b",
        r"\blogin.*link\b",
    ],

    "Threat or intimidation": [
        r"\barrested\b",
        r"\blegal case\b",
        r"\bprosecution\b",
        r"\barrest\b",
        r"\baccount will be blocked\b",
        r"\baccount has been suspended\b",
        r"\bdisconnected\b",
        r"\bfinal warning\b",
    ],

    "Prize or reward claim": [
        r"\bwon\b",
        r"\bwinner\b",
        r"\bprize\b",
        r"\breward\b",
        r"\bgift card\b",
        r"\bfree vacation\b",
        r"\bclaim your prize\b",
    ],

    "Financial request": [
        r"\bwire transfer\b",
        r"\bsend .*money\b",
        r"\bprocessing fee\b",
        r"\bpay\b",
        r"\bpayment\b",
        r"\bbank account\b",
        r"\btransfer\b",
    ],

    "Impersonation or secrecy": [
        r"\bthis is your ceo\b",
        r"\bthis is the ceo\b",
        r"\bthis is your boss\b",
        r"\bkeep this confidential\b",
        r"\bdo not tell\b",
        r"\bdo not discuss\b",
        r"\bprivate payment\b",
    ],

    "Remote access request": [
        r"\bremote access\b",
        r"\ballow remote access\b",
        r"\binstall this software\b",
        r"\btechnical support\b",
        r"\btech support\b",
    ],
}


# --------------------------------------------------
# Detect warning indicators
# --------------------------------------------------

def detect_indicators(message):
    """
    Check a message against known social-engineering
    warning patterns.
    """

    indicators = []

    for indicator_name, patterns in WARNING_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, message, re.IGNORECASE):
                indicators.append(indicator_name)
                break

    return indicators


# --------------------------------------------------
# Analyze a message
# --------------------------------------------------

def analyze_message(message):

    if not message or not message.strip():
        return {
            "prediction": "Unknown",
            "confidence": 0,
            "indicators": [],
            "message": "Please enter a message to analyze."
        }

    message = message.strip()

    # Convert message into TF-IDF features
    message_vector = vectorizer.transform([message])

    # Predict
    prediction = model.predict(message_vector)[0]

    # Get probability
    probabilities = model.predict_proba(message_vector)[0]

    suspicious_probability = probabilities[1]

    # Convert probability to percentage
    confidence = round(suspicious_probability * 100, 2)

    # Detect rule-based indicators
    indicators = detect_indicators(message)

    if prediction == 1:
        result = "Suspicious"
    else:
        result = "Safe"

    return {
        "prediction": result,
        "confidence": confidence,
        "indicators": indicators,
        "message": message
    }


# --------------------------------------------------
# Command-line testing
# --------------------------------------------------

if __name__ == "__main__":

    print("\n======================================")
    print("AI SOCIAL ENGINEERING DETECTOR")
    print("======================================")

    message = input("\nEnter a message to analyze:\n> ")

    result = analyze_message(message)

    print("\n--------------------------------------")
    print("ANALYSIS RESULT")
    print("--------------------------------------")

    print(f"Prediction : {result['prediction']}")
    print(f"Suspicious Probability : {result['confidence']}%")

    if result["indicators"]:

        print("\nWarning Indicators:")

        for indicator in result["indicators"]:
            print(f"- {indicator}")

    else:
        print("\nWarning Indicators:")
        print("- No obvious warning indicators detected.")

    print("--------------------------------------")