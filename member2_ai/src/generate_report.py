
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))
from risk_scorer import RiskScorer


def main():
    input_path = BASE_DIR / "data" / "sample_transactions.json"
    output_path = BASE_DIR / "data" / "risk_assessment_report.json"

    with input_path.open("r", encoding="utf-8") as file:
        transactions = json.load(file)

    scorer = RiskScorer()
    results = [
        scorer.score_transaction(transaction)
        for transaction in transactions
    ]

    report = {
        "report_version": "1.0.0",
        "score_type": "RULE_BASED",
        "data_mode": "SYNTHETIC",
        "transaction_count": len(results),
        "assessments": results,
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f"Report created: {output_path}")
    print(f"Transactions processed: {len(results)}")
    print(f"Assessed: {sum(r['risk_score'] is not None for r in results)}")
    print(f"Unassessed: {sum(r['risk_score'] is None for r in results)}")


if __name__ == "__main__":
    main()
