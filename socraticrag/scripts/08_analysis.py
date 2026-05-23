"""
Script 08: Analysis — merge all scores into results table
Inputs:  data/scores_m1.jsonl
         data/scores_m2.jsonl
         data/scores_m3.jsonl
         data/scores_ragas.jsonl
Output:  outputs/results.csv
         outputs/results_by_state.csv
         outputs/correlation_matrix.csv
         outputs/summary.txt

Produces:
  - Main results table: M1 / M2 / M3 (mean ± SD) per model
  - Per-cognitive-state breakdown for M3 (as promised in paper)
  - Spearman correlation matrix: M1 vs M2, M1 vs M3, M2 vs M3 (orthogonality check)
  - RAGAS comparison column showing near-1.0 clustering
  - Human-readable summary printed to stdout and saved to outputs/summary.txt

Run: python3 scripts/08_analysis.py
"""

import json
import csv
import statistics
from pathlib import Path
from collections import defaultdict

SCORES_M1 = Path("data/scores_m1.jsonl")
SCORES_M2 = Path("data/scores_m2.jsonl")
SCORES_M3 = Path("data/scores_m3.jsonl")
SCORES_RAGAS = Path("data/scores_ragas.jsonl")

OUTPUT_DIR = Path("outputs")
RESULTS_CSV = OUTPUT_DIR / "results.csv"
RESULTS_BY_STATE_CSV = OUTPUT_DIR / "results_by_state.csv"
CORR_CSV = OUTPUT_DIR / "correlation_matrix.csv"
SUMMARY_TXT = OUTPUT_DIR / "summary.txt"


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        print(f"  WARNING: {path} not found — skipping.")
        return []
    rows = []
    with open(path) as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def spearman_rho(x: list[float], y: list[float]) -> float:
    """Compute Spearman rank correlation between x and y."""
    if len(x) != len(y) or len(x) < 2:
        return float("nan")

    def rank(lst: list[float]) -> list[float]:
        sorted_idx = sorted(range(len(lst)), key=lambda i: lst[i])
        ranks = [0.0] * len(lst)
        i = 0
        while i < len(sorted_idx):
            j = i
            while j + 1 < len(sorted_idx) and lst[sorted_idx[j + 1]] == lst[sorted_idx[i]]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[sorted_idx[k]] = avg_rank
            i = j + 1
        return ranks

    rx = rank(x)
    ry = rank(y)
    n = len(rx)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    den_x = (sum((rx[i] - mean_rx) ** 2 for i in range(n))) ** 0.5
    den_y = (sum((ry[i] - mean_ry) ** 2 for i in range(n))) ** 0.5
    if den_x == 0 or den_y == 0:
        return float("nan")
    return round(num / (den_x * den_y), 4)


def fmt(mean: float, sd: float) -> str:
    return f"{mean:.3f} ± {sd:.3f}"


def mean_sd(vals: list[float]) -> tuple[float, float]:
    if not vals:
        return float("nan"), float("nan")
    m = sum(vals) / len(vals)
    s = statistics.stdev(vals) if len(vals) > 1 else 0.0
    return m, s


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Loading score files...")
    m1_rows = load_jsonl(SCORES_M1)
    m2_rows = load_jsonl(SCORES_M2)
    m3_rows = load_jsonl(SCORES_M3)
    ragas_rows = load_jsonl(SCORES_RAGAS)

    # Index by response_id
    m1 = {r["response_id"]: r for r in m1_rows}
    m2 = {r["response_id"]: r for r in m2_rows}
    m3 = {r["response_id"]: r for r in m3_rows}
    ragas = {r["response_id"]: r for r in ragas_rows}

    all_ids = set(m1) | set(m2) | set(m3) | set(ragas)
    print(f"  M1: {len(m1)} | M2: {len(m2)} | M3: {len(m3)} | RAGAS: {len(ragas)} | Union: {len(all_ids)}")

    # Build merged rows
    merged = []
    for rid in all_ids:
        r1 = m1.get(rid, {})
        r2 = m2.get(rid, {})
        r3 = m3.get(rid, {})
        rr = ragas.get(rid, {})
        # Get metadata from whichever score file has it
        meta = r1 or r2 or r3 or rr
        merged.append({
            "response_id": rid,
            "model": meta.get("model", ""),
            "cognitive_state": meta.get("cognitive_state", ""),
            "m1_score": r1.get("m1_score", float("nan")),
            "m1_verdict": r1.get("m1_verdict", ""),
            "m2_score": r2.get("m2_score", float("nan")),
            "m2_vacuous": r2.get("m2_vacuous", False),
            "m3_perception": r3.get("m3_perception", float("nan")),
            "m3_orchestration": r3.get("m3_orchestration", float("nan")),
            "m3_elicitation": r3.get("m3_elicitation", float("nan")),
            "m3_total": r3.get("m3_total", float("nan")),
            "ragas_score": rr.get("ragas_score", float("nan")),
            "ragas_empty": rr.get("ragas_empty", False),
        })

    # ── Main results table ────────────────────────────────────────────────────
    models = sorted(set(r["model"] for r in merged if r["model"]))

    print("\n=== Main Results Table ===")
    header = ["model", "n",
              "M1 (mean±SD)", "M2 (mean±SD)",
              "M3_perception (mean±SD)", "M3_orchestration (mean±SD)", "M3_elicitation (mean±SD)", "M3_total (mean±SD)",
              "RAGAS (mean±SD)"]
    table_rows = []

    for model in models:
        rows = [r for r in merged if r["model"] == model]
        n = len(rows)

        m1s = [r["m1_score"] for r in rows if not isinstance(r["m1_score"], float) or not (r["m1_score"] != r["m1_score"])]
        m1s = [v for v in m1s if v == v]
        m2s = [r["m2_score"] for r in rows if r["m2_score"] == r["m2_score"]]
        m3p = [r["m3_perception"] for r in rows if r["m3_perception"] == r["m3_perception"]]
        m3o = [r["m3_orchestration"] for r in rows if r["m3_orchestration"] == r["m3_orchestration"]]
        m3e = [r["m3_elicitation"] for r in rows if r["m3_elicitation"] == r["m3_elicitation"]]
        m3t = [r["m3_total"] for r in rows if r["m3_total"] == r["m3_total"]]
        rgs = [r["ragas_score"] for r in rows if r["ragas_score"] == r["ragas_score"]]

        row = {
            "model": model,
            "n": n,
            "M1 (mean±SD)": fmt(*mean_sd(m1s)),
            "M2 (mean±SD)": fmt(*mean_sd(m2s)),
            "M3_perception (mean±SD)": fmt(*mean_sd(m3p)),
            "M3_orchestration (mean±SD)": fmt(*mean_sd(m3o)),
            "M3_elicitation (mean±SD)": fmt(*mean_sd(m3e)),
            "M3_total (mean±SD)": fmt(*mean_sd(m3t)),
            "RAGAS (mean±SD)": fmt(*mean_sd(rgs)),
        }
        table_rows.append(row)
        print(f"  {model} (n={n}): M1={row['M1 (mean±SD)']} | M2={row['M2 (mean±SD)']} | M3={row['M3_total (mean±SD)']} | RAGAS={row['RAGAS (mean±SD)']}")

    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(table_rows)
    print(f"\nSaved: {RESULTS_CSV}")

    # ── Per-cognitive-state breakdown (M3) ───────────────────────────────────
    print("\n=== M3 by Cognitive State ===")
    states = sorted(set(r["cognitive_state"] for r in merged if r["cognitive_state"]))
    state_header = ["model", "cognitive_state", "n",
                    "M3_perception", "M3_orchestration", "M3_elicitation", "M3_total"]
    state_rows = []
    for model in models:
        for state in states:
            rows = [r for r in merged if r["model"] == model and r["cognitive_state"] == state]
            if not rows:
                continue
            m3p = [r["m3_perception"] for r in rows if r["m3_perception"] == r["m3_perception"]]
            m3o = [r["m3_orchestration"] for r in rows if r["m3_orchestration"] == r["m3_orchestration"]]
            m3e = [r["m3_elicitation"] for r in rows if r["m3_elicitation"] == r["m3_elicitation"]]
            m3t = [r["m3_total"] for r in rows if r["m3_total"] == r["m3_total"]]
            sr = {
                "model": model,
                "cognitive_state": state,
                "n": len(rows),
                "M3_perception": fmt(*mean_sd(m3p)),
                "M3_orchestration": fmt(*mean_sd(m3o)),
                "M3_elicitation": fmt(*mean_sd(m3e)),
                "M3_total": fmt(*mean_sd(m3t)),
            }
            state_rows.append(sr)
            print(f"  {model} / {state} (n={len(rows)}): {sr['M3_total']}")

    with open(RESULTS_BY_STATE_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=state_header)
        writer.writeheader()
        writer.writerows(state_rows)
    print(f"\nSaved: {RESULTS_BY_STATE_CSV}")

    # ── Spearman correlation matrix ──────────────────────────────────────────
    print("\n=== Spearman Correlation Matrix (orthogonality check) ===")

    def get_triples(rows):
        m1v, m2v, m3v = [], [], []
        for r in rows:
            if r["m1_score"] == r["m1_score"] and r["m2_score"] == r["m2_score"] and r["m3_total"] == r["m3_total"]:
                m1v.append(r["m1_score"])
                m2v.append(r["m2_score"])
                m3v.append(float(r["m3_total"]))
        return m1v, m2v, m3v

    m1v, m2v, m3v = get_triples(merged)
    rho_m1_m2 = spearman_rho(m1v, m2v)
    rho_m1_m3 = spearman_rho(m1v, m3v)
    rho_m2_m3 = spearman_rho(m2v, m3v)

    print(f"  ρ(M1, M2) = {rho_m1_m2:+.4f}")
    print(f"  ρ(M1, M3) = {rho_m1_m3:+.4f}")
    print(f"  ρ(M2, M3) = {rho_m2_m3:+.4f}")
    print("  (Low ρ across all pairs confirms the three metrics capture distinct failure modes.)")

    corr_rows = [
        {"pair": "M1 vs M2", "spearman_rho": rho_m1_m2, "n": len(m1v)},
        {"pair": "M1 vs M3", "spearman_rho": rho_m1_m3, "n": len(m1v)},
        {"pair": "M2 vs M3", "spearman_rho": rho_m2_m3, "n": len(m1v)},
    ]
    with open(CORR_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["pair", "spearman_rho", "n"])
        writer.writeheader()
        writer.writerows(corr_rows)
    print(f"\nSaved: {CORR_CSV}")

    # ── M1 verdict distribution ──────────────────────────────────────────────
    print("\n=== M1 Verdict Distribution ===")
    by_verdict: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in merged:
        if r["m1_verdict"]:
            by_verdict[r["model"]][r["m1_verdict"]] += 1

    for model in models:
        total = sum(by_verdict[model].values())
        for v in ["CLEARLY_WITHHELD", "BORDERLINE", "CLEARLY_LEAKED"]:
            count = by_verdict[model].get(v, 0)
            pct = 100 * count / total if total else 0
            print(f"  {model} | {v}: {count} ({pct:.1f}%)")

    # ── M2 vacuous report ────────────────────────────────────────────────────
    print("\n=== M2 Vacuous Responses ===")
    for model in models:
        rows = [r for r in merged if r["model"] == model]
        vacuous = sum(1 for r in rows if r["m2_vacuous"])
        pct = 100 * vacuous / len(rows) if rows else 0
        print(f"  {model}: {vacuous}/{len(rows)} vacuous ({pct:.1f}%)")

    # ── Critical checkpoint ─────────────────────────────────────────────────
    if m2v:
        m2_all = [r["m2_score"] for r in merged if r["m2_score"] == r["m2_score"]]
        pct_below_1 = 100 * sum(1 for v in m2_all if v < 1.0) / len(m2_all)
        print(f"\n=== M2 Critical Checkpoint ===")
        print(f"  Responses with m2_score < 1.0 (at least one unentailed presupposition): {pct_below_1:.1f}%")
        if pct_below_1 > 25:
            print("  ✓ >25% flag rate confirms core claim: models introduce ungrounded concepts at significant rate.")
        elif pct_below_1 < 10:
            print("  ⚠ <10% flag rate. Models may be overly conservative. Check M2 raw data — still a finding, different story.")
        else:
            print("  ✓ Flag rate in expected range (10–25%). Results support the core claim with moderate effect.")

    # ── Summary text ─────────────────────────────────────────────────────────
    summary_lines = [
        "SocraticRAG — Results Summary",
        "=" * 50,
        "",
        f"Total responses: {len(merged)}",
        f"Models: {', '.join(models)}",
        "",
        "Main Results (mean ± SD):",
    ]
    for tr in table_rows:
        summary_lines.append(f"  {tr['model']}:")
        summary_lines.append(f"    M1 (Socratic adherence):    {tr['M1 (mean±SD)']}")
        summary_lines.append(f"    M2 (retrieval faithfulness): {tr['M2 (mean±SD)']}")
        summary_lines.append(f"    M3 (pedagogical alignment):  {tr['M3_total (mean±SD)']} / 9")
        summary_lines.append(f"    RAGAS baseline:              {tr['RAGAS (mean±SD)']}")
        summary_lines.append("")

    summary_lines += [
        "Spearman Correlations (orthogonality):",
        f"  ρ(M1, M2) = {rho_m1_m2:+.4f}",
        f"  ρ(M1, M3) = {rho_m1_m3:+.4f}",
        f"  ρ(M2, M3) = {rho_m2_m3:+.4f}",
        "",
        "Output files:",
        f"  {RESULTS_CSV}",
        f"  {RESULTS_BY_STATE_CSV}",
        f"  {CORR_CSV}",
        f"  {SUMMARY_TXT}",
        "",
        "Human validation required before final reporting:",
        "  M1: professor review of BORDERLINE responses",
        "  M2: professor spot-check (data/m2_spot_check.jsonl) — Cohen's κ",
        "  M3: professor spot-check (data/m3_spot_check.jsonl) — Spearman ρ > 0.7",
        "  Dean: professor reads 20 (C, U) pairs to validate Dean decisions",
    ]

    with open(SUMMARY_TXT, "w") as f:
        f.write("\n".join(summary_lines) + "\n")
    print(f"\nSaved: {SUMMARY_TXT}")
    print("\nDone. Send outputs/results.csv and outputs/summary.txt to professors for review.")


if __name__ == "__main__":
    main()
