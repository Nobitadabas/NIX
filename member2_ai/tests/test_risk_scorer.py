
import json
import unittest
from pathlib import Path

from src.risk_scorer import RiskScorer


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sample_transactions.json"


class TestRiskScorer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scorer = RiskScorer()

        with open(DATA_PATH, "r", encoding="utf-8") as file:
            cls.transactions = json.load(file)

    def test_sample_transactions_are_scored(self):
        for transaction in self.transactions:
            with self.subTest(transaction=transaction["transaction_id"]):
                result = self.scorer.score_transaction(transaction)
                self.assertIsInstance(result["risk_score"], int)
                self.assertGreaterEqual(result["risk_score"], 0)
                self.assertLessEqual(result["risk_score"], 100)

    def test_ordinary_transaction_has_low_score(self):
        result = self.scorer.score_transaction(self.transactions[0])
        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["risk_level"], "LOW")

    def test_high_velocity_triggers_rule(self):
        result = self.scorer.score_transaction(self.transactions[2])
        rule_ids = [reason["rule_id"] for reason in result["reasons"]]
        self.assertIn("R002", rule_ids)

    def test_multiple_signals_accumulate(self):
        result = self.scorer.score_transaction(self.transactions[4])
        self.assertEqual(result["risk_score"], 35)
        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_missing_field_is_rejected(self):
        transaction = self.transactions[0].copy()
        del transaction["amount"]

        result = self.scorer.score_transaction(transaction)

        self.assertIsNone(result["risk_score"])
        self.assertEqual(result["risk_level"], "UNASSESSED")
        self.assertTrue(result["validation_errors"])

    def test_negative_amount_is_rejected(self):
        transaction = self.transactions[0].copy()
        transaction["amount"] = -100

        result = self.scorer.score_transaction(transaction)

        self.assertIsNone(result["risk_score"])
        self.assertTrue(result["validation_errors"])

    def test_real_data_is_not_accepted_yet(self):
        transaction = self.transactions[0].copy()
        transaction["data_mode"] = "REAL"

        result = self.scorer.score_transaction(transaction)

        self.assertIsNone(result["risk_score"])
        self.assertTrue(result["validation_errors"])

    def test_score_is_capped_at_100(self):
        transaction = self.transactions[4].copy()
        transaction.update({
            "amount_deviation": 5.0,
            "transactions_last_hour": 12,
            "device_change": True,
            "location_change": True,
            "prior_declines": 3,
            "account_age_days": 10,
        })

        result = self.scorer.score_transaction(transaction)

        self.assertEqual(result["risk_score"], 90)
        self.assertEqual(result["risk_level"], "CRITICAL")


    def test_invalid_timestamp_is_rejected(self):
        transaction = self.transactions[0].copy()
        transaction["timestamp"] = "not-a-valid-date"

        result = self.scorer.score_transaction(transaction)

        self.assertIsNone(result["risk_score"])
        self.assertTrue(
            any("timestamp" in error for error in result["validation_errors"])
        )

    def test_nan_amount_is_rejected(self):
        transaction = self.transactions[0].copy()
        transaction["amount"] = float("nan")

        result = self.scorer.score_transaction(transaction)

        self.assertIsNone(result["risk_score"])
        self.assertTrue(result["validation_errors"])

    def test_infinite_deviation_is_rejected(self):
        transaction = self.transactions[0].copy()
        transaction["amount_deviation"] = float("inf")

        result = self.scorer.score_transaction(transaction)

        self.assertIsNone(result["risk_score"])
        self.assertTrue(result["validation_errors"])



if __name__ == "__main__":
    unittest.main()
