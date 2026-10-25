
import json
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from risk_scorer import RiskScorer


def main():
    input_path = BASE_DIR / "data" / "synthetic_transactions.json"
    output_path = BASE_DIR / "data" / "evaluation_report.json"

    with input_path.open("r", encoding="utf-8") as file:
        transactions = json.load(file)

    scorer = RiskScorer()
    results = [
        scorer.score_transaction(transaction)
        for transaction in transactions
    ]

    assessed = [r for r in results if r["risk_score"] is not None]
    unassessed = [r for r in results if r["risk_score"] is None]

    risk_counts = Counter(r["risk_level"] for r in assessed)
    scenario_counts = Counter(
        transaction["scenario_type"] for transaction in transactions
    )
    scenario_scores = {}

    for transaction, result in zip(transactions, results):
        scenario = transaction["scenario_type"]
        scenario_scores.setdefault(scenario, []).append(result["risk_score"])

    scenario_summary = {}
    for scenario, scores in scenario_scores.items():
        valid_scores = [score for score in scores if score is not None]
        scenario_summary[scenario] = {
            "count": len(scores),
            "assessed": len(valid_scores),
            "average_score": (
                round(sum(valid_scores) / len(valid_scores), 2)
                if valid_scores else None
            ),
        }

    report = {
        "report_version": "1.0.0",
        "scoring_version": scorer.config["scoring_version"],
        "score_type": "RULE_BASED",
        "data_mode": "SYNTHETIC",
        "total_transactions": len(transactions),
        "assessed_transactions": len(assessed),
        "unassessed_transactions": len(unassessed),
        "risk_level_counts": dict(risk_counts),
        "scenario_counts": dict(scenario_counts),
        "scenario_summary": scenario_summary,
        "limitations": [
            "All transactions are synthetic.",
            "Scenario categories are generated test conditions, not verified fraud labels.",
            "Results describe this rule configuration only.",
            "These results do not establish real-world fraud detection accuracy.",
        ],
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print("Evaluation complete")
    print(f"Total transactions: {len(transactions)}")
    print(f"Assessed: {len(assessed)}")
    print(f"Unassessed: {len(unassessed)}")
    print("\nRisk level counts:")
    for level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        print(f"{level}: {risk_counts.get(level, 0)}")

    print("\nAverage score by scenario:")
    for scenario, summary in sorted(scenario_summary.items()):
        print(
            f"{scenario}: {summary['average_score']} "
            f"(n={summary['count']})"
        )

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
