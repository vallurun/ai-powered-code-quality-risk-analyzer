import re, io
from typing import Dict, Any, List
from radon.complexity import cc_visit
from radon.metrics import mi_visit

DIFF_FILE_RE = re.compile(r'^\+\+\+ b/(?P<path>.+)$', re.M)

def parse_files(patch: str) -> List[str]:
    return DIFF_FILE_RE.findall(patch)

def cyclomatic_complexity(py_code: str) -> float:
    try:
        blocks = cc_visit(py_code)
        if not blocks:
            return 0.0
        return sum(b.complexity for b in blocks) / len(blocks)
    except Exception:
        return 0.0

def featureize(patch: str) -> Dict[str, Any]:
    files = parse_files(patch)
    lines_added = sum(1 for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
    lines_removed = sum(1 for l in patch.splitlines() if l.startswith('-') and not l.startswith('---'))
    py_files = [f for f in files if f.endswith('.py')]

    avg_cc = 0.0
    if py_files:
        # naive: compute CC on added lines only
        added_py = "\n".join(l[1:] for l in patch.splitlines() if l.startswith('+') and l.endswith('.py') is False)
        avg_cc = cyclomatic_complexity(added_py)

    return {
        "num_files": len(files),
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "num_py_files": len(py_files),
        "avg_cc": avg_cc,
    }

def suggestions_for(path: str) -> List[str]:
    sugs = []
    if path.endswith(".py"):
        sugs.append("Run pylint/ruff; ensure type hints.")
    if path.endswith((".js", ".ts")):
        sugs.append("Run eslint; check async error handling.")
    if path.endswith(".sql"):
        sugs.append("Validate query plans and indexes.")
    if "test" not in path.lower():
        sugs.append("Consider adding/expanding unit tests.")
    return sugs
