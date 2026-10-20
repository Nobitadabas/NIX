\# TRUSTRAIL AI — Risk Scoring Integration Contract



\*\*Owner:\*\* Member 2 — AI/ML and Risk Scoring  

\*\*Version:\*\* 1.0  

\*\*Status:\*\* Initial prototype contract  

\*\*Scoring method:\*\* Rule-based  

\*\*Data mode:\*\* Synthetic only



\## 1. Purpose



This contract defines how the transaction risk-scoring module accepts transaction data and returns an explainable assessment.



The score is intended to prioritise transactions for human review. It is not a probability of fraud and does not prove that a transaction is fraudulent.



\## 2. Input



The scorer accepts one transaction as a Python dictionary with these fields:



| Field | Type |

|---|---|

| transaction\_id | string |

| timestamp | ISO 8601 datetime string |

| amount | finite, non-negative number |

| currency | string |

| channel | string |

| merchant\_category | string |

| account\_age\_days | non-negative integer |

| transactions\_last\_hour | non-negative integer |

| amount\_deviation | finite, non-negative number |

| device\_change | boolean |

| location\_change | boolean |

| prior\_declines | non-negative integer |

| scenario\_type | string |

| data\_mode | string; must be SYNTHETIC |



\## 3. Example Input



```json

{

&#x20; "transaction\_id": "TXN-0001",

&#x20; "timestamp": "2026-10-20T10:00:00",

&#x20; "amount": 450.0,

&#x20; "currency": "INR",

&#x20; "channel": "UPI",

&#x20; "merchant\_category": "Groceries",

&#x20; "account\_age\_days": 850,

&#x20; "transactions\_last\_hour": 1,

&#x20; "amount\_deviation": 0.4,

&#x20; "device\_change": false,

&#x20; "location\_change": false,

&#x20; "prior\_declines": 0,

&#x20; "scenario\_type": "ordinary",

&#x20; "data\_mode": "SYNTHETIC"

}

```



\## 4. Successful Response



The scorer returns a dictionary containing:



\- `transaction\_id`: transaction identifier

\- `risk\_score`: integer from 0 to 100

\- `risk\_level`: LOW, MEDIUM, HIGH, or CRITICAL

\- `score\_type`: RULE\_BASED

\- `reasons`: list of triggered rules

\- `scoring\_version`: configured version

\- `data\_mode`: SYNTHETIC

\- `validation\_errors`: empty list when validation succeeds

\- `review\_guidance`: guidance for a human reviewer



Each triggered reason contains:



\- `rule\_id`

\- `title`

\- `explanation`

\- `points`



The score is capped at the configured maximum.



\## 5. Validation Failure Response



If required fields are missing or invalid, the scorer returns:



\- `risk\_score`: null

\- `risk\_level`: UNASSESSED

\- `reasons`: empty list

\- `validation\_errors`: list of validation messages

\- `review\_guidance`: instruction to correct or verify the input



The backend must not treat an unassessed transaction as LOW risk.



\## 6. Python Integration Example



The backend can call the scorer directly from Python:



```python

from src.risk\_scorer import RiskScorer



scorer = RiskScorer()

result = scorer.score\_transaction(transaction)

```



Here, `transaction` must be a dictionary matching the input contract.



The backend should inspect `result\["validation\_errors"]` and `result\["risk\_score"]` before treating the assessment as successful.



\## 7. Integration Notes



\- The current implementation accepts SYNTHETIC data only.

\- The scorer is a Python module, not an HTTP API.

\- An API endpoint must be implemented by the backend team if the frontend needs HTTP access.

\- The backend must preserve the scorer's explanations instead of inventing reasons.

\- The final field names and response format should be confirmed jointly by Members 2 and 4.

\- The scoring weights and thresholds are demonstration settings, not validated production thresholds.

\- Synthetic scenario labels are not verified fraud labels.

\- A human reviewer must make the final decision.



\## 8. Current Verification



The current test suite contains 11 automated tests, including checks for missing fields, negative amounts, invalid timestamps, NaN, infinity, and score capping.



The latest recorded test run passed all 11 tests. Re-run the test suite after any code or configuration changes.

