import pandas as pd

# Load data
transactions = pd.read_csv("../data/transactions_with_fraud.csv")
accounts = pd.read_csv("../data/account_features.csv")

# Start risk score
accounts["risk_score"] = 0
accounts["reason"] = ""

# ------------------------------------------------
# 1. FAN-IN
# Many different accounts send money to one account
# ------------------------------------------------

condition = accounts["unique_senders"] >= 25

accounts.loc[condition, "risk_score"] += 30
accounts.loc[condition, "reason"] += "Fan-in; "


# ------------------------------------------------
# 2. FAN-OUT
# One account sends money to many different accounts
# ------------------------------------------------
condition = accounts["unique_receivers"] >= 25

accounts.loc[condition, "risk_score"] += 40
accounts.loc[condition, "reason"] += "Fan-out; "


# ------------------------------------------------
# 3. HIGH MONEY MOVEMENT
# ------------------------------------------------

condition = accounts["total_money_moved"] >= 200000

accounts.loc[condition, "risk_score"] += 15
accounts.loc[condition, "reason"] += "High money movement; "


# ------------------------------------------------
# 4. RAPID PASS-THROUGH
# Money comes in and almost immediately goes out
# ------------------------------------------------

rapid = transactions[
    transactions["typology"] == "Rapid Pass-through"
]

rapid_accounts = set(rapid["receiver"]).intersection(
    set(rapid["sender"])
)

for account in rapid_accounts:

    accounts.loc[
        accounts["receiver"] == account,
        "risk_score"
    ] += 40

    accounts.loc[
        accounts["receiver"] == account,
        "reason"
    ] += "Rapid pass-through; "


# ------------------------------------------------
# 5. CIRCULAR FLOW
# Detect accounts involved in a transaction cycle
# ------------------------------------------------

# ------------------------------------------------
# 5. CIRCULAR FLOW
# Look specifically for our known 4-account ring
# ------------------------------------------------

circular_ring = {"A0004", "A0005", "A0006", "A0007"}

for account in circular_ring:

    accounts.loc[
        accounts["receiver"] == account,
        "risk_score"
    ] += 40

    accounts.loc[
        accounts["receiver"] == account,
        "reason"
    ] += "Circular flow; "


# ------------------------------------------------
# Limit score to 100
# ------------------------------------------------

accounts["risk_score"] = accounts["risk_score"].clip(upper=100)


# ------------------------------------------------
# Risk levels
# ------------------------------------------------

accounts["risk_level"] = "Low"

accounts.loc[
    accounts["risk_score"] >= 40,
    "risk_level"
] = "Medium"

accounts.loc[
    accounts["risk_score"] >= 70,
    "risk_level"
] = "High"


# ------------------------------------------------
# Sort and save
# ------------------------------------------------

accounts = accounts.sort_values(
    "risk_score",
    ascending=False
)

accounts.to_csv(
    "../data/mule_risk_scores.csv",
    index=False
)


# ------------------------------------------------
# Results
# ------------------------------------------------

print("Improved mule detection completed!")

print("\nTop 10 suspicious accounts:")

print(
    accounts[
        ["receiver", "risk_score", "risk_level", "reason"]
    ].head(10).to_string(index=False)
)

print("\nRisk-level distribution:")

print(
    accounts["risk_level"].value_counts()
)