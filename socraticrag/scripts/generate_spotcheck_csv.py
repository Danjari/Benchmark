"""
Generate professor spot-check CSV files for M2 and M3 human validation.

Outputs:
  data/spotcheck_M2_professor.csv
  data/spotcheck_M3_professor.csv

Usage:
  python3 scripts/generate_spotcheck_csv.py
"""

import json
import csv
import re
from pathlib import Path


def strip_latex(text: str) -> str:
    """Convert LaTeX math notation to plain readable text."""
    if not text:
        return text

    # Display math: \[ ... \] and $$ ... $$
    text = re.sub(r'\$\$(.+?)\$\$', lambda m: _latex_expr(m.group(1)), text, flags=re.DOTALL)
    text = re.sub(r'\\\[(.+?)\\\]', lambda m: _latex_expr(m.group(1)), text, flags=re.DOTALL)

    # Inline math: \( ... \) and $ ... $
    text = re.sub(r'\\\((.+?)\\\)', lambda m: _latex_expr(m.group(1)), text, flags=re.DOTALL)
    text = re.sub(r'\$(.+?)\$', lambda m: _latex_expr(m.group(1)), text)

    # Clean up any remaining backslash commands not inside math
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)

    # Collapse multiple spaces/newlines introduced by stripping
    text = re.sub(r'  +', ' ', text)
    text = text.strip()
    return text


def _latex_expr(expr: str) -> str:
    """Convert a single LaTeX math expression to a readable approximation."""
    expr = expr.strip()

    # Named commands → readable symbols
    replacements = [
        (r'\\mathcal\{([^}]+)\}', r'\1'),
        (r'\\mathrm\{([^}]+)\}', r'\1'),
        (r'\\mathbf\{([^}]+)\}', r'\1'),
        (r'\\mathbb\{([^}]+)\}', r'\1'),
        (r'\\text\{([^}]+)\}', r'\1'),
        (r'\\hat\{([^}]+)\}', r'\1_hat'),
        (r'\\tilde\{([^}]+)\}', r'\1_tilde'),
        (r'\\bar\{([^}]+)\}', r'\1_bar'),
        (r'\\vec\{([^}]+)\}', r'\1'),
        (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)'),
        (r'\\sqrt\{([^}]+)\}', r'sqrt(\1)'),
        (r'\\sum', 'sum'),
        (r'\\prod', 'prod'),
        (r'\\int', 'integral'),
        (r'\\infty', 'inf'),
        (r'\\alpha', 'alpha'),
        (r'\\beta', 'beta'),
        (r'\\gamma', 'gamma'),
        (r'\\delta', 'delta'),
        (r'\\epsilon', 'epsilon'),
        (r'\\theta', 'theta'),
        (r'\\lambda', 'lambda'),
        (r'\\mu', 'mu'),
        (r'\\sigma', 'sigma'),
        (r'\\pi', 'pi'),
        (r'\\tau', 'tau'),
        (r'\\phi', 'phi'),
        (r'\\psi', 'psi'),
        (r'\\omega', 'omega'),
        (r'\\rightarrow', '->'),
        (r'\\leftarrow', '<-'),
        (r'\\leq', '<='),
        (r'\\geq', '>='),
        (r'\\neq', '!='),
        (r'\\approx', '≈'),
        (r'\\times', 'x'),
        (r'\\cdot', '·'),
        (r'\\ldots', '...'),
        (r'\\mid', '|'),
        (r'\\_', '_'),
        (r'\\,', ' '),
        (r'\\;', ' '),
        (r'\\!', ''),
        (r'\\\s', ' '),
        # Superscripts and subscripts: x^{n} → x^n, x_{i} → x_i
        (r'\^\{([^}]+)\}', r'^\1'),
        (r'_\{([^}]+)\}', r'_\1'),
        # Remove remaining braces
        (r'\{([^}]*)\}', r'\1'),
        # Remove remaining backslash commands
        (r'\\[a-zA-Z]+', ''),
        (r'\\', ''),
    ]
    for pattern, repl in replacements:
        expr = re.sub(pattern, repl, expr)

    return expr.strip()

_VERDICT_LABELS = {
    "ENTAILED":     "SUPPORTED",
    "NOT_ENTAILED": "NOT SUPPORTED",
}

def human_verdict(v: str) -> str:
    return _VERDICT_LABELS.get(v, v)


M2_INPUT  = Path("data/m2_spot_check.jsonl")
M3_INPUT  = Path("data/m3_spot_check.jsonl")
M2_OUTPUT = Path("data/spotcheck_M2_professor.csv")
M3_OUTPUT = Path("data/spotcheck_M3_professor.csv")


def build_m2():
    rows = []
    with open(M2_INPUT) as f:
        for line in f:
            rows.append(json.loads(line))

    headers = [
        "row_id",
        "cognitive_state",
        "context_C",
        "tutor_response_R",
        "presupposition_number",
        "presupposition_text",
        "YOUR_VERDICT",   # professor fills: SUPPORTED or NOT SUPPORTED
        "notes",          # optional
    ]

    out_rows = []
    row_id = 1
    for item in rows:
        presups  = item.get("m2_presuppositions", [])
        state    = item.get("cognitive_state", "")
        chunk    = strip_latex(item.get("chunk_text", ""))
        response = strip_latex(item.get("response", ""))

        if not presups:
            out_rows.append({
                "row_id": row_id,
                "cognitive_state": state,
                "context_C": chunk,
                "tutor_response_R": response,
                "presupposition_number": "—",
                "presupposition_text": "(no presuppositions extracted — vacuous response)",
                "YOUR_VERDICT": "N/A — skip this row",
                "notes": "",
            })
            row_id += 1
            continue

        for p_idx, presup in enumerate(presups):
            out_rows.append({
                "row_id": row_id,
                "cognitive_state": state,
                "context_C": chunk,
                "tutor_response_R": response,
                "presupposition_number": p_idx + 1,
                "presupposition_text": presup,
                "YOUR_VERDICT": "",
                "notes": "",
            })
            row_id += 1

    with open(M2_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Saved M2 CSV → {M2_OUTPUT}  ({len(out_rows)} rows)")


def build_m3():
    rows = []
    with open(M3_INPUT) as f:
        for line in f:
            rows.append(json.loads(line))

    headers = [
        "row_id",
        "cognitive_state",
        "target_concept",
        "context_C",
        "student_utterance_U",
        "tutor_response_R",
        "YOUR_PERCEPTION",      # professor fills: 0, 1, 2, or 3
        "YOUR_ORCHESTRATION",   # professor fills: 0, 1, 2, or 3
        "YOUR_ELICITATION",     # professor fills: 0, 1, 2, or 3
        "YOUR_TOTAL",           # professor fills or auto-sum in Google Sheets
        "notes",
    ]

    out_rows = []
    for idx, item in enumerate(rows):
        profile = item.get("profile", {})
        out_rows.append({
            "row_id": idx + 1,
            "cognitive_state": item.get("cognitive_state", ""),
            "target_concept": profile.get("target_concept", ""),
            "context_C": strip_latex(item.get("chunk_text", "")),
            "student_utterance_U": strip_latex(item.get("utterance", "")),
            "tutor_response_R": strip_latex(item.get("response", "")),
            "YOUR_PERCEPTION": "",
            "YOUR_ORCHESTRATION": "",
            "YOUR_ELICITATION": "",
            "YOUR_TOTAL": "",
            "notes": "",
        })

    with open(M3_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Saved M3 CSV → {M3_OUTPUT}  ({len(out_rows)} rows)")


if __name__ == "__main__":
    build_m2()
    build_m3()
    print("\nDone. Import into Google Sheets: File → Import → Upload.")
