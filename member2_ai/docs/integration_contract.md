# TRUSTRAIL AI — Risk Scoring Integration Contract



**Owner:** Member 2 — AI/ML and Risk Scoring

**Version:** 1.0

**Status:** Initial prototype contract

**Scoring method:** Rule-based

**Data mode:** Synthetic only



## 1. Purpose



This contract defines how the transaction risk-scoring module accepts transaction data and returns an explainable assessment.



The score is intended to prioritise transactions for human review. It is not a probability of fraud and does not prove that a transaction is fraudulent.



## 2. Input



The scorer accepts one transaction as a Python dictionary with these fields:



| Field | Type |

|---|---|

| transaction_id | string |

| timestamp | ISO 8601 datetime string |

| amount | finite, non-negative number |

| currency | string |

| channel | string |

| merchant_category | string |

| account_age_days | non-negative integer |

| transactions_last_hour | non-negative integer |

| amount_deviation | finite, non-negative number |

| device_change | boolean |

| location_change | boolean |

| prior_declines | non-negative integer |

| scenario_type | string |

| data_mode | string; must be SYNTHETIC |



## 3. Example Input



```json

{

  "transaction_id": "TXN-0001",

  "timestamp": "2026-10-20T10:00:00",

  "amount": 450.0,

  "currency": "INR",

  "channel": "UPI",

  "merchant_category": "Groceries",

  "account_age_days": 850,

  "transactions_last_hour": 1,

  "amount_deviation": 0.4,

  "device_change": false,

  "location_change": false,

  "prior_declines": 0,

  "scenario_type": "ordinary",

  "data_mode": "SYNTHETIC"

}

```



## 4. Successful Response



The scorer returns a dictionary containing:



- `transaction_id`: transaction identifier

- `risk_score`: integer from 0 to 100

- `risk_level`: LOW, MEDIUM, HIGH, or CRITICAL

- `score_type`: RULE_BASED

- `reasons`: list of triggered rules

- `scoring_version`: configured version

- `data_mode`: SYNTHETIC

- `validation_errors`: empty list when validation succeeds

- `review_guidance`: guidance for a human reviewer



Each triggered reason contains:



- `rule_id`

- `title`

- `explanation`

- `points`



The score is capped at the configured maximum.



## 5. Validation Failure Response

If required fields are missing or invalid, the scorer returns a dictionary containing:

- `transaction_id`: the supplied transaction identifier, if available; otherwise `null`
- `risk_score`: `null`
- `risk_level`: `UNASSESSED`
- `score_type`: the configured score type
- `reasons`: an empty list
- `scoring_version`: the configured scoring version
- `data_mode`: the supplied data mode, if available; otherwise `UNKNOWN`
- `validation_errors`: a list of validation messages
- `review_guidance`: instruction to correct or verify the input data before assessing risk

The backend must not treat an unassessed transaction as LOW risk. It should check `validation_errors` and `risk_score` before using the assessment.


## 6. Python Integration Example



The backend can call the scorer directly from Python:



```python

from src.risk_scorer import RiskScorer



scorer = RiskScorer()

result = scorer.score_transaction(transaction)

```



Here, `transaction` must be a dictionary matching the input contract.



The backend should inspect `result["validation_errors"]` and `result["risk_score"]` before treating the assessment as successful.



## 7. Integration Notes



- The current implementation accepts SYNTHETIC data only.

- The scorer is a Python module, not an HTTP API.

- An API endpoint must be implemented by the backend team if the frontend needs HTTP access.

- The backend must preserve the scorer's explanations instead of inventing reasons.

- The final field names and response format should be confirmed jointly by Members 2 and 4.

- The scoring weights and thresholds are demonstration settings, not validated production thresholds.

- Synthetic scenario labels are not verified fraud labels.

- A human reviewer must make the final decision.



## 8. Current Verification



The current test suite contains 11 automated tests, including checks for missing fields, negative amounts, invalid timestamps, NaN, infinity, and score capping.



The latest recorded test run passed all 11 tests. Re-run the test suite after any code or configuration changes.
