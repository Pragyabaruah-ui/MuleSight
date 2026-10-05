import pandas as pd

# Load transaction data
transactions = pd.read_csv("../data/transactions_with_fraud.csv")

# Convert timestamp to datetime
transactions["timestamp"] = pd.to_datetime(
    transactions["timestamp"],
    format="mixed"
)

# -----------------------------
# Features for money received
# -----------------------------

received = transactions.groupby("receiver").agg(
    total_received=("amount", "sum"),
    received_count=("amount", "count"),
    unique_senders=("sender", "nunique")
)

# -----------------------------
# Features for money sent
# -----------------------------

sent = transactions.groupby("sender").agg(
    total_sent=("amount", "sum"),
    sent_count=("amount", "count"),
    unique_receivers=("receiver", "nunique")
)

# -----------------------------
# Combine account features
# -----------------------------

account_features = received.join(sent, how="outer").fillna(0)

# -----------------------------
# Additional features
# -----------------------------

account_features["total_transactions"] = (
    account_features["received_count"]
    + account_features["sent_count"]
)

account_features["total_money_moved"] = (
    account_features["total_received"]
    + account_features["total_sent"]
)

# Ratio of money sent compared to money received
account_features["send_receive_ratio"] = (
    account_features["total_sent"]
    / account_features["total_received"].replace(0, 1)
)

# -----------------------------
# Save account-level dataset
# -----------------------------

account_features = account_features.reset_index()
account_features.rename(columns={"index": "account"}, inplace=True)

account_features.to_csv(
    "../data/account_features.csv",
    index=False
)

print("Account features created successfully!")
print(f"Number of accounts analyzed: {len(account_features)}")

print("\nSample account features:")
print(account_features.head())