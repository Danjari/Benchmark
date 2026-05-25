"""
Generate professor spot-check Markdown files for M2 and M3 human validation.

LaTeX is kept intact so formulas render in any Markdown viewer.
Recommended viewer: https://markdownlivepreview.com/

Outputs:
  data/spotcheck_M2_professor.md
  data/spotcheck_M3_professor.md

Usage:
  python3 scripts/generate_spotcheck_md.py
"""

import json
from pathlib import Path

M2_INPUT  = Path("data/m2_spot_check.jsonl")
M3_INPUT  = Path("data/m3_spot_check.jsonl")
M2_OUTPUT = Path("data/spotcheck_M2_professor.md")
M3_OUTPUT = Path("data/spotcheck_M3_professor.md")


# ── M2 ────────────────────────────────────────────────────────────────────────

def build_m2():
    items = []
    with open(M2_INPUT) as f:
        for line in f:
            items.append(json.loads(line))

    lines = []

    lines.append("# M2 Spot-Check — Retrieval Faithfulness\n")
    lines.append("> **How to view formulas:** paste this file into "
                 "[https://markdownlivepreview.com/](https://markdownlivepreview.com/) "
                 "and all math will render automatically.\n")
    lines.append("> **How to fill in:** open `spotcheck_M2_professor.csv` in Google Sheets "
                 "and enter your verdict in the **YOUR\\_VERDICT** column for each row ID shown below.\n")
    lines.append(
        "> **SUPPORTED** — the presupposition is a claim that can be directly derived from Context C.  \n"
        "> **NOT SUPPORTED** — the claim is absent from or contradicts Context C.\n"
    )
    lines.append("---\n")

    # Assign row IDs the same way the CSV does
    csv_row_id = 1
    for item in items:
        presups  = item.get("m2_presuppositions", [])
        verdicts = item.get("m2_verdicts", [])   # kept internally but NOT shown
        state    = item.get("cognitive_state", "")
        chunk    = item.get("chunk_text", "").strip()
        response = item.get("response", "").strip()

        n_rows = max(len(presups), 1)
        row_range = (f"rows {csv_row_id}–{csv_row_id + n_rows - 1}"
                     if n_rows > 1 else f"row {csv_row_id}")

        lines.append(f"## Item — *{state}* &nbsp;·&nbsp; {row_range}\n")

        lines.append("**Context C**\n")
        lines.append(f"{chunk}\n")

        lines.append("**Tutor Response R**\n")
        lines.append(f"{response}\n")

        if not presups:
            lines.append(
                f"> **Row {csv_row_id}** — No presuppositions extracted (vacuous response). "
                "Mark `N/A` in YOUR\\_VERDICT.\n"
            )
            csv_row_id += 1
        else:
            lines.append("**Presuppositions — enter your verdict in the CSV**\n")
            lines.append("| Row ID | Presupposition | YOUR\\_VERDICT *(fill in CSV)* |")
            lines.append("|--------|----------------|-------------------------------|")
            for p_idx, presup in enumerate(presups):
                lines.append(f"| {csv_row_id} | {presup} | |")
                csv_row_id += 1
            lines.append("")

        lines.append("---\n")

    M2_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved M2 Markdown → {M2_OUTPUT}  ({csv_row_id - 1} rows)")


# ── M3 ────────────────────────────────────────────────────────────────────────

def build_m3():
    items = []
    with open(M3_INPUT) as f:
        for line in f:
            items.append(json.loads(line))

    lines = []

    lines.append("# M3 Spot-Check — Pedagogical Alignment\n")
    lines.append("> **How to view formulas:** paste this file into "
                 "[https://markdownlivepreview.com/](https://markdownlivepreview.com/) "
                 "and all math will render automatically.\n")
    lines.append("> **How to fill in:** open `spotcheck_M3_professor.csv` in Google Sheets "
                 "and enter your scores in **YOUR\\_P**, **YOUR\\_O**, **YOUR\\_E** for each row ID.\n")
    lines.append(
        "> **Scoring rubric (0–3 per dimension)**\n"
        ">\n"
        "> | Score | Perception *(reads student state)* | Orchestration *(manages response)* | Elicitation *(draws student out)* |\n"
        "> |-------|-----------------------------------|-----------------------------------|-----------------------------------|\n"
        "> | 0 | Ignores cognitive state | Directly gives answer | Closed yes/no or rhetorical |\n"
        "> | 1 | Acknowledges but misreads | Hints but gives too much | Leads toward one answer |\n"
        "> | 2 | Correctly identifies state | Scaffolds appropriately | Open, invites reasoning |\n"
        "> | 3 | Identifies + adapts strategy | Fully withholds, guides only | Probes deeper, extends thinking |\n"
    )
    lines.append("---\n")

    for idx, item in enumerate(items):
        profile = item.get("profile", {})
        state   = item.get("cognitive_state", "")
        concept = profile.get("target_concept", "")
        chunk   = item.get("chunk_text", "").strip()
        utt     = item.get("utterance", "").strip()
        resp    = item.get("response", "").strip()
        row_id  = idx + 1

        lines.append(f"## Row {row_id} — *{state}* &nbsp;·&nbsp; {concept}\n")

        lines.append("**Context C**\n")
        lines.append(f"{chunk}\n")

        lines.append("**Student Utterance**\n")
        lines.append(f"{utt}\n")

        lines.append("**Tutor Response**\n")
        lines.append(f"{resp}\n")

        lines.append("**Enter your scores in the CSV for row " + str(row_id) + "**\n")
        lines.append("| Dimension | YOUR Score *(0–3)* |")
        lines.append("|-----------|-------------------|")
        lines.append("| Perception | |")
        lines.append("| Orchestration | |")
        lines.append("| Elicitation | |")
        lines.append("| **Total** | |")
        lines.append("")

        lines.append("---\n")

    M3_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved M3 Markdown → {M3_OUTPUT}  ({len(items)} rows)")


if __name__ == "__main__":
    build_m2()
    build_m3()
    print("\nDone. Send professors:")
    print("  • The .md file — paste into https://markdownlivepreview.com/ to read with rendered math")
    print("  • The matching .csv — import into Google Sheets to fill in verdicts/scores")
