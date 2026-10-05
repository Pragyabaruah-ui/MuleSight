import pandas as pd
import numpy as np

# Number of accounts and transactions
NUM_ACCOUNTS = 2000
NUM_TRANSACTIONS = 50000

# Create account IDs
accounts = [f"A{i:04d}" for i in range(1, NUM_ACCOUNTS + 1)]

# Generate random transactions
np.random.seed(42)

senders = np.random.choice(accounts, NUM_TRANSACTIONS)
receivers = np.random.choice(accounts, NUM_TRANSACTIONS)

# Make sure sender and receiver are different
same_account = senders == receivers
while same_account.any():
    receivers[same_account] = np.random.choice(
        accounts, same_account.sum()
    )
    same_account = senders == receivers

# Generate transaction amounts
amounts = np.round(
    np.random.lognormal(mean=7, sigma=1, size=NUM_TRANSACTIONS),
    2
)

# Generate timestamps
timestamps = pd.date_range(
    start="2026-01-01",
    end="2026-03-31",
    periods=NUM_TRANSACTIONS
)

# Create transaction DataFrame
transactions = pd.DataFrame({
    "transaction_id": [f"T{i:06d}" for i in range(1, NUM_TRANSACTIONS + 1)],
    "timestamp": timestamps,
    "sender": senders,
    "receiver": receivers,
    "amount": amounts,
    "channel": np.random.choice(
        ["UPI", "IMPS", "NEFT"], 
        NUM_TRANSACTIONS,
        p=[0.70, 0.20, 0.10]
    )
})

# Save the dataset
transactions.to_csv("../data/transactions.csv", index=False)

print("Transaction dataset created successfully!")
print(f"Number of transactions: {len(transactions)}")
print(f"Number of accounts: {NUM_ACCOUNTS}")
print("\nFirst 5 transactions:")
print(transactions.head())