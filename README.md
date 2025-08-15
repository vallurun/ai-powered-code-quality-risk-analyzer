# AI-Powered Code Quality & Risk Analyzer

A lightweight **AI-assisted code review service** that ingests a unified diff (`git diff`/PR patch),
extracts features (churn, complexity via Radon, file types, lint findings), and predicts **defect risk**
using a simple ML model. Exposes a REST API for CI/PR pipelines (Azure DevOps/GitHub).

> This is a local-first prototype with a pluggable feature extractor and model. Swap in real PR webhooks,
> Azure Data Explorer as a feature store, and a stronger model for production.

## Highlights
- **FastAPI** microservice with `/analyze` endpoint
- **Feature extraction**: churn, file counts, radon cyclomatic complexity, simple heuristics
- **Model**: scikit-learn LogisticRegression (trained on synthetic data for demo)
- **Inline hints**: returns suggestions + risk score per file
- **CI**: pytest + GitHub Actions

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Train the demo model and start API
python -m src.model && uvicorn src.app:app --reload --port 8080
```

Analyze a patch:
```bash
curl -X POST http://localhost:8080/analyze -H "Content-Type: application/json" -d @data/sample_request.json
```

## Structure
```
1es-ai-code-reviewer/
├─ src/
│  ├─ app.py               # FastAPI app
│  ├─ model.py             # Train/load demo model
│  ├─ feature_extractor.py # Parse diff & compute features
│  └─ schemas.py           # Pydantic models
├─ data/
│  ├─ sample_diff.patch
│  └─ sample_request.json
├─ tests/
│  └─ test_features.py
├─ .github/workflows/
│  └─ ci.yml
├─ requirements.txt
└─ README.md
```

## Azure Integration (next steps)
- Push features to **Azure Data Explorer** for longitudinal modeling
- Gate PRs in **Azure DevOps**: fail if risk > threshold or suggestions contain "security"
- Send metrics to **Application Insights**

## License
MIT
