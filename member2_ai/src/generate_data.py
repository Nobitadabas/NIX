
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = BASE_DIR / "data" / "synthetic_transactions.json"

SEED = 42
DEFAULT_COUNT = 200


def generate_transaction(index, scenario, rng, timestamp):
    transaction = {
        "transaction_id": f"SYN-{index:05d}",
        "timestamp": timestamp.isoformat(timespec="seconds"),
        "amount": round(rng.uniform(100, 3000), 2),
        "currency": "INR",
        "channel": rng.choice(["UPI", "Card", "NetBanking"]),
        "merchant_category": rng.choice(
            ["Groceries", "Food", "Shopping", "Travel", "Electronics"]
        ),
        "account_age_days": rng.randint(60, 2000),
        "transactions_last_hour": rng.randint(0, 4),
        "amount_deviation": round(rng.uniform(0, 1.5), 2),
        "device_change": False,
        "location_change": False,
        "prior_declines": 0,
        "scenario_type": scenario,
        "data_mode": "SYNTHETIC",
    }

    if scenario == "ordinary":
        pass

    elif scenario == "high_amount_deviation":
        transaction["amount"] = round(rng.uniform(10000, 50000), 2)
        transaction["amount_deviation"] = round(rng.uniform(3.1, 6.0), 2)

    elif scenario == "velocity_spike":
        transaction["transactions_last_hour"] = rng.randint(10, 20)

    elif scenario == "new_device":
        transaction["device_change"] = True

    elif scenario == "location_change":
        transaction["location_change"] = True

    elif scenario == "repeated_declines":
        transaction["prior_declines"] = rng.randint(2, 5)

    elif scenario == "multiple_signals":
        transaction["amount_deviation"] = round(rng.uniform(3.1, 5.0), 2)
        transaction["transactions_last_hour"] = rng.randint(10, 15)
        transaction["device_change"] = True
        transaction["location_change"] = True
        transaction["prior_declines"] = rng.randint(2, 4)

    elif scenario == "new_account":
        transaction["account_age_days"] = rng.randint(1, 29)

    elif scenario == "high_amount_normal_pattern":
        transaction["amount"] = round(rng.uniform(20000, 50000), 2)
        transaction["amount_deviation"] = round(rng.uniform(0, 1.5), 2)

    elif scenario == "repeated_low_value":
        transaction["amount"] = round(rng.uniform(10, 200), 2)
        transaction["transactions_last_hour"] = rng.randint(10, 18)

    return transaction


def main():
    rng = random.Random(SEED)
    scenarios = [
        "ordinary",
        "high_amount_deviation",
        "velocity_spike",
        "new_device",
        "location_change",
        "repeated_declines",
        "multiple_signals",
        "new_account",
        "high_amount_normal_pattern",
        "repeated_low_value",
    ]

    transactions = []
    start_time = datetime(2026, 10, 20, 10, 0, 0)

    for index in range(1, DEFAULT_COUNT + 1):
        scenario = scenarios[(index - 1) % len(scenarios)]
        timestamp = start_time + timedelta(minutes=index * 3)

        transaction = generate_transaction(
            index, scenario, rng, timestamp
        )
        transactions.append(transaction)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=2)

    print(f"Generated {len(transactions)} synthetic transactions.")
    print(f"Random seed: {SEED}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
