# TRUSTRAIL AI — Transaction Data Dictionary



## 1. Purpose



This document defines the input fields for Member 2's transaction risk-scoring module.



The module calculates an explainable, rule-based risk score to help prioritise transactions for human review. A risk score is not proof of fraud.



All initial test data will be synthetic.



## 2. Transaction Input Schema



| Field | Type | Description | Example |

|---|---|---|---|

| transaction\_id | string | Unique transaction identifier | TXN-0001 |

| timestamp | string | Transaction date and time | 2026-10-20T14:30:00 |

| amount | number | Transaction amount, non-negative | 12500.00 |

| currency | string | Three-letter currency code | INR |

| channel | string | Transaction channel | UPI |

| merchant\_category | string | Merchant category | Electronics |

| account\_age\_days | integer | Account age in days | 240 |

| transactions\_last\_hour | integer | Transactions in the previous hour | 8 |

| amount\_deviation | number | Deviation from normal transaction amount; definition to be finalised | 3.2 |

| device\_change | boolean | Whether a device change was detected | true |

| location\_change | boolean | Whether a location change was detected | false |

| prior\_declines | integer | Previous declined attempts in an agreed time window | 2 |

| scenario\_type | string | Synthetic scenario label | velocity\_spike |

| data\_mode | string | Data origin | SYNTHETIC |



## 3. Validation Rules



* Transaction ID must not be empty.
* Amount must be numeric and non-negative.
* Account age, transaction count, and prior declines must be non-negative integers.
* Device and location change indicators must be Boolean values.
* Missing or invalid values must be reported explicitly.
* Missing information must not silently be treated as normal behaviour.
* Unknown categorical values must be handled explicitly.
* Synthetic scenario labels must not be presented as verified real-world fraud labels.



## 4. Planned Risk-Scoring Output



The initial output fields are:



* transaction\_id
* risk\_score
* risk\_level
* score\_type
* reasons
* scoring\_version
* data\_mode



The exact output contract must be confirmed with Member 4 before integration.



## 5. Important Notes



* The meaning and threshold of amount\_deviation must be defined before scoring.
* The observation window for prior\_declines must be agreed upon.
* The allowed channel, merchant category, and scenario values must be documented.
* Do not use real customer information, bank account numbers, card numbers, or credentials.
* The initial scorer will use transparent rules rather than an unvalidated machine-learning model.
