"""
generate_dataset.py
Creates a labeled dataset of safe and suspicious messages.
Output: data/messages.csv

Columns:
    text     - the message
    label    - 0 = safe, 1 = suspicious
    category - safe, phishing, prize_scam, tech_support, ceo_fraud, threat_scam
"""

import random
from pathlib import Path

import pandas as pd

random.seed(42)  # makes results repeatable

# ---------- Building blocks used to fill in the templates ----------
BANKS = ["HDFC Bank", "SBI", "ICICI Bank", "Axis Bank", "PayPal", "Chase", "Wells Fargo"]
COMPANIES = ["Amazon", "Microsoft", "Netflix", "Google", "Apple", "Flipkart", "Paytm"]
NAMES = ["Priya", "Rahul", "Anita", "John", "Sarah", "Karthik", "Meera", "David"]
AMOUNTS = ["$500", "Rs. 25,000", "$1,200", "Rs. 4,999", "$89.99", "Rs. 1,50,000"]
DEADLINES = ["24 hours", "2 hours", "30 minutes", "today", "end of day"]
FAKE_LINKS = [
    "http://secure-login-verify.com/account",
    "http://bit.ly/3xYz9Ab",
    "http://paypa1-support.net/verify",
    "http://amazon-rewards-claim.xyz/win",
    "http://bank-update-kyc.info/login",
    "http://tinyurl.com/urgent-verify",
]
GIFTS = ["iPhone 15", "Rs. 10,00,000", "$1,000 gift card", "a free vacation", "a brand new car"]
BOSSES = ["CEO", "Director", "Managing Director", "CFO"]

# ---------- Suspicious message templates ----------
PHISHING = [
    "URGENT: Your {bank} account has been suspended. Verify your details within {deadline} at {link}",
    "Dear customer, unusual login detected on your {bank} account. Click {link} to confirm your password immediately.",
    "Your {bank} KYC has expired. Update now at {link} or your account will be blocked.",
    "Security alert from {company}: confirm your identity and card number here {link} to avoid suspension.",
    "Action required: your {company} password expires in {deadline}. Login at {link} to keep access.",
    "{bank} notice: suspicious transaction of {amount}. Verify your OTP and PIN at {link} now.",
]

PRIZE_SCAM = [
    "Congratulations {name}! You have won {gift}. Claim your prize now at {link}",
    "You are our lucky winner! Send a small processing fee to receive {gift}. Reply within {deadline}.",
    "{company} giveaway: you were selected to receive {gift}. Click {link} and enter your bank details.",
    "Final notice: unclaimed reward of {amount} is waiting. Confirm your details at {link} before it expires.",
    "Dear {name}, you have been chosen for a free {gift}. Act fast, offer ends in {deadline}!",
]

TECH_SUPPORT = [
    "WARNING: Your computer is infected with a virus. Call {company} support immediately and allow remote access.",
    "{company} Security: we detected hackers on your device. Install this software now {link} to fix it.",
    "Your {company} account was hacked. Share the verification code we sent you so our agent can secure it.",
    "Alert! Your device has 5 viruses. Do not turn off your computer. Call the toll free number within {deadline}.",
    "Hello, this is {company} technical support. Please give us your password to remove the malware.",
]

CEO_FRAUD = [
    "Hi {name}, this is the {boss}. I am in a meeting and need you to buy gift cards urgently. Keep this confidential.",
    "{name}, please process an urgent wire transfer of {amount} to this new vendor today. Do not discuss with anyone.",
    "This is your {boss}. I need you to send {amount} right now. I cannot take calls. Reply as soon as possible.",
    "Quick favor {name}: change the vendor bank account details before {deadline}. This is confidential and urgent.",
    "From the {boss}: I need your help with a private payment of {amount}. Do not tell the finance team yet.",
]

THREAT_SCAM = [
    "FINAL WARNING: A legal case has been filed against you. Pay {amount} within {deadline} or you will be arrested.",
    "Your electricity will be disconnected tonight unless you pay {amount} at {link}. Act now.",
    "Tax department notice: you owe {amount}. Pay immediately via gift cards to avoid prosecution.",
    "Your parcel is held at customs. Pay a fee of {amount} at {link} within {deadline} or it will be destroyed.",
    "We have your personal photos. Send {amount} in {deadline} or we will share them with your contacts.",
]

# ---------- Safe message templates (including tricky ones) ----------
SAFE = [
    "Hi {name}, are we still meeting for lunch tomorrow at 1 pm?",
    "Don't forget the team meeting at 3 pm in conference room B.",
    "Thanks for sending the report, {name}. I'll review it and get back to you by Friday.",
    "Happy birthday {name}! Hope you have a wonderful day with family.",
    "Your {company} order has been shipped and will arrive on Thursday. Track it in the official app.",
    "Reminder: your dentist appointment is scheduled for Monday at 10 am.",
    "Can you share the project slides before tomorrow's class?",
    "Your {bank} statement for this month is now available. Log in through the official app to view it.",
    "Your OTP is 482913. Do not share this code with anyone, including {bank} staff.",
    "Payment of {amount} to {company} was successful. Thank you for your purchase.",
    "Hey {name}, I'm running ten minutes late. Please start without me.",
    "The quarterly budget review is on Wednesday. Please bring your department's figures.",
    "Dinner at my place on Saturday? I'm making pasta.",
    "Your {company} subscription renews next month. You can manage it anytime in your account settings.",
    "Please find the meeting notes attached. Let me know if I missed anything.",
    "Great job on the presentation today, {name}! The client loved it.",
    "Your package from {company} was delivered to your front door at 2:15 pm.",
    "Reminder: the library book you borrowed is due on Friday.",
    "{bank} will never ask for your PIN or password. Stay alert and report suspicious messages.",
    "Weekly update: the server maintenance finished successfully and all services are running normally.",
]

CATEGORIES = {
    "phishing": PHISHING,
    "prize_scam": PRIZE_SCAM,
    "tech_support": TECH_SUPPORT,
    "ceo_fraud": CEO_FRAUD,
    "threat_scam": THREAT_SCAM,
    "safe": SAFE,
}


def fill_template(template: str) -> str:
    """Replace placeholders like {bank} with random choices."""
    return template.format(
        bank=random.choice(BANKS),
        company=random.choice(COMPANIES),
        name=random.choice(NAMES),
        amount=random.choice(AMOUNTS),
        deadline=random.choice(DEADLINES),
        link=random.choice(FAKE_LINKS),
        gift=random.choice(GIFTS),
        boss=random.choice(BOSSES),
    )


def build_dataset(per_category_suspicious: int = 120, safe_count: int = 600) -> pd.DataFrame:
    rows = []
    for category, templates in CATEGORIES.items():
        count = safe_count if category == "safe" else per_category_suspicious
        for _ in range(count):
            template = random.choice(templates)
            text = fill_template(template)
            label = 0 if category == "safe" else 1
            rows.append({"text": text, "label": label, "category": category})

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset="text")           # remove exact repeats
    df = df.sample(frac=1, random_state=42)          # shuffle rows
    return df.reset_index(drop=True)


def main():
    project_folder = Path(__file__).parent
    data_folder = project_folder / "data"
    data_folder.mkdir(exist_ok=True)

    df = build_dataset()
    output_path = data_folder / "messages.csv"
    df.to_csv(output_path, index=False)

    print(f"Dataset saved to: {output_path}")
    print(f"Total messages: {len(df)}")
    print("\nMessages per category:")
    print(df["category"].value_counts())
    print("\nSafe vs suspicious (0 = safe, 1 = suspicious):")
    print(df["label"].value_counts())
    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()