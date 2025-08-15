from fastapi import FastAPI
from .schemas import AnalyzeRequest, AnalyzeResponse, FileSuggestion
from .feature_extractor import featureize, parse_files, suggestions_for
from .model import load_model
import numpy as np

app = FastAPI(title="1ES AI Code Reviewer")
model = load_model()

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    feats = featureize(req.patch)
    X = np.array([[
        feats["num_files"],
        feats["lines_added"],
        feats["lines_removed"],
        feats["num_py_files"],
        feats["avg_cc"],
    ]], dtype=float)
    prob = float(model.predict_proba(X)[0][1])
    files = []
    for p in parse_files(req.patch):
        files.append(FileSuggestion(path=p, risk=prob, suggestions=suggestions_for(p)))
    return AnalyzeResponse(overall_risk=prob, files=files)

@app.get("/healthz")
def health():
    return {"ok": True}
