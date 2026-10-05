import pandas as pd
import numpy as np

# Load the normal transaction data
transactions = pd.read_csv("../data/transactions.csv")

np.random.seed(42)

# Columns to identify suspicious transactions
transactions["is_suspicious"] = 0
transactions["typology"] = "Normal"

# ---------------------------------------------------
# 1. FAN-IN
# Many accounts send money to one mule account
# ---------------------------------------------------

mule_fan_in = "A0001"

senders = [f"A{i:04d}" for i in range(100, 130)]

fan_in_rows = []

for i, sender in enumerate(senders):
    fan_in_rows.append({
        "transaction_id": f"FI{i:04d}",
        "timestamp": f"2026-03-20 10:{i:02d}:00",
        "sender": sender,
        "receiver": mule_fan_in,
        "amount": np.random.randint(3000, 10000),
        "channel": "UPI",
        "is_suspicious": 1,
        "typology": "Fan-in"
    })


# ---------------------------------------------------
# 2. FAN-OUT
# One mule account sends money to many accounts
# ---------------------------------------------------

mule_fan_out = "A0002"

fan_out_rows = []

for i in range(30):
    receiver = f"A{i + 200:04d}"

    fan_out_rows.append({
        "transaction_id": f"FO{i:04d}",
        "timestamp": f"2026-03-21 14:{i:02d}:00",
        "sender": mule_fan_out,
        "receiver": receiver,
        "amount": np.random.randint(3000, 10000),
        "channel": "UPI",
        "is_suspicious": 1,
        "typology": "Fan-out"
    })


# ---------------------------------------------------
# 3. RAPID PASS-THROUGH
# Mule receives money and quickly sends it elsewhere
# ---------------------------------------------------

mule_rapid = "A0003"

rapid_rows = []

for i in range(20):

    receive_time = f"2026-03-22 11:{i:02d}:00"
    send_time = f"2026-03-22 11:{i:02d}:30"

    amount = np.random.randint(5000, 15000)

    # Money received
    rapid_rows.append({
        "transaction_id": f"RP_IN{i:04d}",
        "timestamp": receive_time,
        "sender": f"A{i + 300:04d}",
        "receiver": mule_rapid,
        "amount": amount,
        "channel": "UPI",
        "is_suspicious": 1,
        "typology": "Rapid Pass-through"
    })

    # Money forwarded shortly after
    rapid_rows.append({
        "transaction_id": f"RP_OUT{i:04d}",
        "timestamp": send_time,
        "sender": mule_rapid,
        "receiver": f"A{i + 400:04d}",
        "amount": amount * 0.95,
        "channel": "UPI",
        "is_suspicious": 1,
        "typology": "Rapid Pass-through"
    })


# ---------------------------------------------------
# 4. CIRCULAR FLOW
# A → B → C → D → A
# ---------------------------------------------------

circular_rows = []

circle = ["A0004", "A0005", "A0006", "A0007"]

for i in range(len(circle)):

    sender = circle[i]
    receiver = circle[(i + 1) % len(circle)]

    circular_rows.append({
        "transaction_id": f"CF{i:04d}",
        "timestamp": f"2026-03-23 16:{i:02d}:00",
        "sender": sender,
        "receiver": receiver,
        "amount": 25000,
        "channel": "UPI",
        "is_suspicious": 1,
        "typology": "Circular Flow"
    })


# ---------------------------------------------------
# Combine everything
# ---------------------------------------------------

fraud_transactions = pd.DataFrame(
    fan_in_rows + fan_out_rows + rapid_rows + circular_rows
)

transactions = pd.concat(
    [transactions, fraud_transactions],
    ignore_index=True
)

# Save the new dataset
transactions.to_csv(
    "../data/transactions_with_fraud.csv",
    index=False
)

print("Suspicious transactions added successfully!")
print(f"Total transactions: {len(transactions)}")

print("\nSuspicious transactions by typology:")
print(
    transactions[transactions["is_suspicious"] == 1]["typology"]
    .value_counts()
)

print("\nSuspicious accounts:")
print(["A0001", "A0002", "A0003", "A0004", "A0005", "A0006", "A0007"])