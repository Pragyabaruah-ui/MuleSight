import pandas as pd

# Load our risk scores
accounts = pd.read_csv("../data/mule_risk_scores.csv")

# These are the mule accounts we intentionally created
known_mules = {
    "A0001",
    "A0002",
    "A0003",
    "A0004",
    "A0005",
    "A0006",
    "A0007"
}

# Accounts flagged as High risk
high_risk = set(
    accounts.loc[
        accounts["risk_level"] == "High",
        "receiver"
    ]
)

# Check which known mules were detected
detected = known_mules.intersection(high_risk)

print("Known mule accounts:")
print(sorted(known_mules))

print("\nHigh-risk accounts detected:")
print(sorted(high_risk))

print("\nKnown mules detected:")
print(sorted(detected))

print(f"\nMule accounts detected: {len(detected)} / {len(known_mules)}")

detection_rate = len(detected) / len(known_mules) * 100

print(f"Detection rate: {detection_rate:.2f}%")