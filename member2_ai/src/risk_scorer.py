
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


CONFIG_PATH = Path(__file__).with_name("scoring_config.json")


class RiskScorer:
    def __init__(self, config_path: Path = CONFIG_PATH):
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

    def score_transaction(self, transaction: dict[str, Any]) -> dict[str, Any]:
        errors = self._validate_transaction(transaction)

        if errors:
            return {
                "transaction_id": (
                    transaction.get("transaction_id")
                    if isinstance(transaction, dict)
                    else None
                ),
                "risk_score": None,
                "risk_level": "UNASSESSED",
                "score_type": self.config["score_type"],
                "reasons": [],
                "scoring_version": self.config["scoring_version"],
                "data_mode": (
                    transaction.get("data_mode", "UNKNOWN")
                    if isinstance(transaction, dict)
                    else "UNKNOWN"
                ),
                "validation_errors": errors,
                "review_guidance": (
                    "Correct or verify the input data before assessing risk."
                ),
            }

        score = 0
        reasons = []

        for rule in self.config["rules"]:
            if self._rule_matches(transaction, rule):
                score += rule["points"]
                reasons.append({
                    "rule_id": rule["rule_id"],
                    "title": rule["title"],
                    "explanation": self._explain_rule(transaction, rule),
                    "points": rule["points"],
                })

        score = min(score, self.config["maximum_score"])

        return {
            "transaction_id": transaction["transaction_id"],
            "risk_score": score,
            "risk_level": self._get_risk_level(score),
            "score_type": self.config["score_type"],
            "reasons": reasons,
            "scoring_version": self.config["scoring_version"],
            "data_mode": transaction["data_mode"],
            "validation_errors": [],
            "review_guidance": self._get_review_guidance(reasons),
        }

    @staticmethod
    def _validate_transaction(transaction: dict[str, Any]) -> list[str]:
        if not isinstance(transaction, dict):
            return ["Transaction must be a JSON object."]

        errors = []

        required_fields = [
            "transaction_id",
            "timestamp",
            "amount",
            "currency",
            "channel",
            "merchant_category",
            "account_age_days",
            "transactions_last_hour",
            "amount_deviation",
            "device_change",
            "location_change",
            "prior_declines",
            "scenario_type",
            "data_mode",
        ]

        for field in required_fields:
            if field not in transaction or transaction[field] is None:
                errors.append(f"Missing required field: {field}")

        if errors:
            return errors

        if (
            not isinstance(transaction["transaction_id"], str)
            or not transaction["transaction_id"].strip()
        ):
            errors.append("transaction_id must be a non-empty string.")

        amount = transaction["amount"]

        if (
            isinstance(amount, bool)
            or not isinstance(amount, (int, float))
            or not math.isfinite(amount)
            or amount < 0
        ):
            errors.append("amount must be a finite, non-negative number.")

        integer_fields = [
            "account_age_days",
            "transactions_last_hour",
            "prior_declines",
        ]

        for field in integer_fields:
            value = transaction[field]

            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or value < 0
            ):
                errors.append(
                    f"{field} must be a non-negative integer."
                )

        deviation = transaction["amount_deviation"]

        if (
            isinstance(deviation, bool)
            or not isinstance(deviation, (int, float))
            or not math.isfinite(deviation)
            or deviation < 0
        ):
            errors.append(
                "amount_deviation must be a finite, non-negative number."
            )

        for field in ["device_change", "location_change"]:
            if not isinstance(transaction[field], bool):
                errors.append(f"{field} must be a Boolean value.")

        string_fields = [
            "timestamp",
            "currency",
            "channel",
            "merchant_category",
            "scenario_type",
            "data_mode",
        ]

        for field in string_fields:
            value = transaction[field]

            if not isinstance(value, str) or not value.strip():
                errors.append(f"{field} must be a non-empty string.")

        timestamp = transaction["timestamp"]

        if isinstance(timestamp, str) and timestamp.strip():
            try:
                datetime.fromisoformat(timestamp)
            except ValueError:
                errors.append(
                    "timestamp must be a valid ISO 8601 datetime."
                )

        if transaction["data_mode"] != "SYNTHETIC":
            errors.append(
                "This initial module accepts SYNTHETIC data only."
            )

        return errors

    @staticmethod
    def _rule_matches(
        transaction: dict[str, Any],
        rule: dict[str, Any],
    ) -> bool:
        value = transaction[rule["field"]]
        operator = rule["operator"]
        threshold = rule["threshold"]

        if operator == "greater_than":
            return value > threshold

        if operator == "greater_than_or_equal":
            return value >= threshold

        if operator == "less_than":
            return value < threshold

        if operator == "equals":
            return value == threshold

        raise ValueError(
            f"Unsupported scoring operator: {operator}"
        )

    @staticmethod
    def _explain_rule(
        transaction: dict[str, Any],
        rule: dict[str, Any],
    ) -> str:
        field = rule["field"]
        value = transaction[field]

        explanations = {
            "amount_deviation": (
                f"Amount deviation is {value}, "
                "above the configured threshold."
            ),
            "transactions_last_hour": (
                f"{value} transactions occurred in the previous hour."
            ),
            "device_change": "A device change was detected.",
            "location_change": "A location change was detected.",
            "prior_declines": (
                f"{value} previous declined attempts were recorded."
            ),
            "account_age_days": (
                f"The account is {value} days old."
            ),
        }

        return explanations.get(
            field,
            f"{field} matched rule {rule['rule_id']}.",
        )

    def _get_risk_level(self, score: int) -> str:
        for level, limits in self.config["risk_levels"].items():
            if limits["min_score"] <= score <= limits["max_score"]:
                return level

        raise ValueError(
            f"No risk level configured for score {score}."
        )

    @staticmethod
    def _get_review_guidance(
        reasons: list[dict[str, Any]],
    ) -> str:
        if not reasons:
            return (
                "No configured risk rules were triggered. "
                "This does not guarantee that the transaction is safe."
            )

        return (
            "Review the contributing signals, verify the transaction context, "
            "and follow the authorised human-review process. "
            "Do not treat the score as proof of fraud."
        )
