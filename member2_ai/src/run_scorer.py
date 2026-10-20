
import json
from pathlib import Path

from risk_scorer import RiskScorer


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sample_transactions.json"


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        transactions = json.load(file)

    scorer = RiskScorer()

    for transaction in transactions:
        result = scorer.score_transaction(transaction)

        print("=" * 55)
        print(f"Transaction: {result['transaction_id']}")
        print(f"Risk score:  {result['risk_score']}")
        print(f"Risk level:  {result['risk_level']}")

        if result["validation_errors"]:
            print("Validation errors:")
            for error in result["validation_errors"]:
                print(f"- {error}")
        else:
            print("Triggered rules:")
            if not result["reasons"]:
                print("- None")
            for reason in result["reasons"]:
                print(
                    f"- {reason['rule_id']}: {reason['title']} "
                    f"(+{reason['points']})"
                )

        print(f"Review guidance: {result['review_guidance']}")


if __name__ == "__main__":
    main()
