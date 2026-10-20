# TRUSTRAIL AI — Member 2 Risk Scoring Module



## Overview



This module provides a deterministic, explainable, rule-based transaction risk scorer for TRUSTRAIL AI. It uses synthetic transaction data to prioritize transactions for human review. A high score is not proof of fraud.



## Features



- Synthetic transaction data generation.

- Configurable scoring rules and thresholds.

- Risk scores, risk levels, and explanations.

- Validation of missing and invalid transaction fields.

- Synthetic scenario evaluation and JSON reports.

- Automated unit tests.

- Data dictionary and integration contract.



## Project Structure



- `src/risk_scorer.py` — risk-scoring logic.

- `src/scoring_config.json` — scoring rules and configuration.

- `src/generate_data.py` — synthetic data generator.

- `src/run_scorer.py` — scorer runner.

- `src/generate_report.py` — assessment report generation.

- `src/evaluate_scorer.py` — synthetic scenario evaluation.

- `tests/test_risk_scorer.py` — automated tests.

- `data/` — sample transactions and generated reports.

- `docs/data_dictionary.md` — transaction field definitions.

- `docs/integration_contract.md` — scorer input and output contract.



## Setup



Open Command Prompt in the repository root and activate the existing virtual environment:



.venv\Scripts\activate
cd member2_ai



Use the Python environment and dependencies required by the project.



## Run the Module



Run these commands separately from the `member2_ai` directory:


python src\generate_data.py
python src\run_scorer.py
python src\generate_report.py
python src\evaluate_scorer.py
python -m unittest discover -s tests -v



## Integration



The scorer is currently a Python module, not an HTTP API. The backend can call the scoring function directly from Python, as documented in `docs/integration_contract.md`.



The final input and response schema must be confirmed with Member 4 before integration. The frontend should use actual scorer outputs.



## Evaluation Limitations



- The dataset contains synthetic transactions, not real banking data.

- Synthetic scenario labels are not verified fraud labels.

- Evaluation results describe performance on the generated scenarios only and do not establish real-world fraud detection accuracy.

- The risk score is a rule-based prioritization signal, not a calibrated fraud probability.

- A human reviewer must make the final decision.

- Never include real customer information, banking credentials, account numbers, or card numbers.



## Testing



The latest recorded local test run passed all 11 unit tests. Rerun the tests after changes and report the actual results.



## Current Status



The initial Member 2 implementation has been pushed to the `member2-ai-risk-module` branch. Backend integration and full end-to-end verification are still pending.
