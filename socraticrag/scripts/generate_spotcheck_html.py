"""
Generate professor spot-check HTML viewer files for M2 and M3 human validation.

The HTML files render LaTeX math via MathJax. Each item shows the row_id(s)
from the companion CSV so the professor can fill verdicts/scores in Google Sheets.

Outputs:
  data/spotcheck_M2_viewer.html
  data/spotcheck_M3_viewer.html

Usage:
  python3 scripts/generate_spotcheck_html.py
"""

import json
import html
from pathlib import Path

M2_INPUT  = Path("data/m2_spot_check.jsonl")
M3_INPUT  = Path("data/m3_spot_check.jsonl")
M2_OUTPUT = Path("data/spotcheck_M2_viewer.html")
M3_OUTPUT = Path("data/spotcheck_M3_viewer.html")

# ── HTML shell ────────────────────────────────────────────────────────────────

HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script>
  window.MathJax = {{
    tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']] }},
    options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre'] }}
  }};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
  body {{ font-family: Georgia, serif; max-width: 900px; margin: 40px auto; padding: 0 20px;
         background: #fafafa; color: #222; line-height: 1.6; }}
  h1 {{ font-size: 1.4em; border-bottom: 2px solid #333; padding-bottom: 8px; }}
  .intro {{ background: #fff8e1; border-left: 4px solid #f9a825; padding: 14px 18px;
            border-radius: 4px; margin-bottom: 32px; font-size: 0.95em; }}
  .intro h2 {{ margin: 0 0 8px; font-size: 1.05em; color: #5d4037; }}
  .card {{ background: #fff; border: 1px solid #ddd; border-radius: 6px;
           margin-bottom: 28px; padding: 20px 24px; box-shadow: 0 1px 3px rgba(0,0,0,.06); }}
  .card-header {{ display: flex; gap: 12px; align-items: baseline; margin-bottom: 14px;
                  flex-wrap: wrap; }}
  .row-badge {{ background: #1565c0; color: #fff; font-family: monospace; font-size: 0.82em;
                padding: 2px 8px; border-radius: 3px; white-space: nowrap; }}
  .tag {{ background: #e8eaf6; color: #283593; font-size: 0.8em; padding: 2px 8px;
          border-radius: 3px; font-family: sans-serif; }}
  .tag.model {{ background: #e8f5e9; color: #1b5e20; }}
  .section-label {{ font-family: sans-serif; font-size: 0.75em; font-weight: 700;
                    text-transform: uppercase; letter-spacing: .06em; color: #888;
                    margin: 14px 0 4px; }}
  .context-box {{ background: #f5f5f5; border-left: 3px solid #90caf9;
                  padding: 10px 14px; border-radius: 3px; font-size: 0.93em; }}
  .response-box {{ background: #f9f9f9; border-left: 3px solid #a5d6a7;
                   padding: 10px 14px; border-radius: 3px; font-size: 0.93em; }}
  .utterance-box {{ background: #fff3e0; border-left: 3px solid #ffcc80;
                    padding: 10px 14px; border-radius: 3px; font-size: 0.93em; }}
  .presup-list {{ margin: 0; padding-left: 0; list-style: none; }}
  .presup-item {{ display: flex; gap: 10px; align-items: flex-start; padding: 6px 0;
                  border-bottom: 1px solid #eee; font-size: 0.93em; }}
  .presup-item:last-child {{ border-bottom: none; }}
  .presup-num {{ font-family: monospace; font-size: 0.85em; color: #888;
                 min-width: 28px; padding-top: 1px; }}
  .verdict {{ font-family: monospace; font-size: 0.78em; padding: 2px 7px;
              border-radius: 3px; white-space: nowrap; margin-left: auto; flex-shrink: 0; }}
  .verdict.SUPPORTED {{ background: #e8f5e9; color: #2e7d32; }}
  .verdict.NOT_SUPPORTED {{ background: #ffebee; color: #c62828; }}
  .verdict.VACUOUS {{ background: #eeeeee; color: #757575; }}
  .scores-row {{ display: flex; gap: 16px; margin-top: 6px; flex-wrap: wrap; }}
  .score-box {{ background: #f3e5f5; border-radius: 4px; padding: 6px 14px;
                text-align: center; font-family: sans-serif; }}
  .score-box .label {{ font-size: 0.7em; color: #6a1b9a; text-transform: uppercase;
                       letter-spacing: .05em; }}
  .score-box .value {{ font-size: 1.3em; font-weight: 700; color: #4a148c; }}
  .score-total {{ background: #e8eaf6; }}
  .score-total .label {{ color: #1a237e; }}
  .score-total .value {{ color: #0d47a1; }}
  .csv-note {{ font-family: sans-serif; font-size: 0.78em; color: #777;
               margin-top: 10px; font-style: italic; }}
</style>
</head>
<body>
"""

HTML_FOOT = "</body></html>\n"


def e(text):
    """HTML-escape a string."""
    return html.escape(str(text), quote=False)


# ── M2 ────────────────────────────────────────────────────────────────────────

def build_m2():
    items = []
    with open(M2_INPUT) as f:
        for line in f:
            items.append(json.loads(line))

    _verdict_labels = {"ENTAILED": "SUPPORTED", "NOT_ENTAILED": "NOT SUPPORTED"}

    # Assign row_ids the same way generate_spotcheck_csv.py does
    row_id = 1
    for item in items:
        item["_row_ids"] = []
        presups  = item.get("m2_presuppositions", [])
        if not presups:
            item["_row_ids"].append(row_id)
            row_id += 1
        else:
            for _ in presups:
                item["_row_ids"].append(row_id)
                row_id += 1

    parts = []
    parts.append(HTML_HEAD.format(title="SocraticRAG – M2 Spot-Check Viewer"))
    parts.append("<h1>M2 Spot-Check — Retrieval Faithfulness Viewer</h1>\n")
    parts.append("""<div class="intro">
<h2>How to use this file</h2>
<p>This viewer renders the math in the Context and Response columns so you can read them properly.
Open <strong>spotcheck_M2_professor.csv</strong> in Google Sheets alongside this page.
For each presupposition, enter <code>SUPPORTED</code> or <code>NOT SUPPORTED</code> in the
<strong>YOUR_VERDICT</strong> column of the matching <strong>row_id</strong>.</p>
<p><strong>SUPPORTED</strong>: the claim made by the presupposition can be directly derived from Context C.<br>
<strong>NOT SUPPORTED</strong>: the claim is absent from or contradicts Context C.</p>
</div>\n""")

    for item in items:
        presups  = item.get("m2_presuppositions", [])
        verdicts = item.get("m2_verdicts", [])
        row_ids  = item["_row_ids"]
        model    = item.get("model", "")
        state    = item.get("cognitive_state", "")
        chunk    = item.get("chunk_text", "")
        response = item.get("response", "")

        if not presups:
            row_label = f"Row {row_ids[0]}"
            presup_html = '<p style="color:#888;font-style:italic">(No presuppositions extracted — vacuous response. Mark YOUR_VERDICT as N/A in the CSV.)</p>'
        else:
            row_label = f"Rows {row_ids[0]}–{row_ids[-1]}" if len(row_ids) > 1 else f"Row {row_ids[0]}"
            li_items = []
            for p_idx, (presup, verdict) in enumerate(zip(presups, verdicts)):
                rid = row_ids[p_idx]
                label = _verdict_labels.get(verdict, verdict)
                vclass = label.replace(" ", "_") if label in ("SUPPORTED", "NOT SUPPORTED") else "VACUOUS"
                li_items.append(
                    f'<li class="presup-item">'
                    f'<span class="presup-num">#{p_idx+1} <small>(row {rid})</small></span>'
                    f'<span>{e(presup)}</span>'
                    f'<span class="verdict {vclass}">{e(label)}</span>'
                    f'</li>'
                )
            presup_html = '<ul class="presup-list">' + "".join(li_items) + "</ul>"

        parts.append(f"""<div class="card">
  <div class="card-header">
    <span class="row-badge">{e(row_label)}</span>
    <span class="tag model">{e(model)}</span>
    <span class="tag">{e(state)}</span>
  </div>

  <div class="section-label">Context C</div>
  <div class="context-box">{e(chunk)}</div>

  <div class="section-label">Tutor Response R</div>
  <div class="response-box">{e(response)}</div>

  <div class="section-label">Presuppositions &amp; Our Verdict → Your Verdict in CSV</div>
  {presup_html}
  <p class="csv-note">Fill YOUR_VERDICT in the CSV for each row number above.</p>
</div>
""")

    parts.append(HTML_FOOT)

    with open(M2_OUTPUT, "w", encoding="utf-8") as f:
        f.write("".join(parts))

    print(f"Saved M2 viewer → {M2_OUTPUT}  ({len(items)} items)")


# ── M3 ────────────────────────────────────────────────────────────────────────

def build_m3():
    items = []
    with open(M3_INPUT) as f:
        for line in f:
            items.append(json.loads(line))

    parts = []
    parts.append(HTML_HEAD.format(title="SocraticRAG – M3 Spot-Check Viewer"))
    parts.append("<h1>M3 Spot-Check — Pedagogical Alignment Viewer</h1>\n")
    parts.append("""<div class="intro">
<h2>How to use this file</h2>
<p>This viewer renders the math so you can read the Context, Student Utterance, and Tutor Response properly.
Open <strong>spotcheck_M3_professor.csv</strong> in Google Sheets alongside this page.
For each row, enter your scores (0–3) in <strong>YOUR_PERCEPTION</strong>,
<strong>YOUR_ORCHESTRATION</strong>, and <strong>YOUR_ELICITATION</strong>.</p>
<table style="border-collapse:collapse;font-family:sans-serif;font-size:0.86em;margin-top:8px;width:100%">
<tr style="background:#e8eaf6">
  <th style="padding:6px 10px;text-align:left">Score</th>
  <th style="padding:6px 10px;text-align:left">Perception<br><small>Reads student state</small></th>
  <th style="padding:6px 10px;text-align:left">Orchestration<br><small>Manages response</small></th>
  <th style="padding:6px 10px;text-align:left">Elicitation<br><small>Draws student out</small></th>
</tr>
<tr><td style="padding:5px 10px;border-top:1px solid #ddd"><strong>0</strong></td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Ignores cognitive state</td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Directly gives answer/solution</td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Closed yes/no or rhetorical</td></tr>
<tr style="background:#fafafa"><td style="padding:5px 10px;border-top:1px solid #ddd"><strong>1</strong></td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Acknowledges but misreads</td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Hints but gives too much</td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Leads toward one answer</td></tr>
<tr><td style="padding:5px 10px;border-top:1px solid #ddd"><strong>2</strong></td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Correctly identifies state</td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Scaffolds appropriately</td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Open, invites reasoning</td></tr>
<tr style="background:#fafafa"><td style="padding:5px 10px;border-top:1px solid #ddd"><strong>3</strong></td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Identifies + adapts strategy</td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Fully withholds, guides only</td>
    <td style="padding:5px 10px;border-top:1px solid #ddd">Probes deeper, extends thinking</td></tr>
</table>
</div>\n""")

    for idx, item in enumerate(items):
        row_id  = idx + 1
        profile = item.get("profile", {})
        model   = item.get("model", "")
        state   = item.get("cognitive_state", "")
        concept = profile.get("target_concept", "")
        chunk   = item.get("chunk_text", "")
        utt     = item.get("utterance", "")
        resp    = item.get("response", "")
        p = item.get("m3_perception", "")
        o = item.get("m3_orchestration", "")
        el = item.get("m3_elicitation", "")
        total = item.get("m3_total", "")

        parts.append(f"""<div class="card">
  <div class="card-header">
    <span class="row-badge">Row {row_id}</span>
    <span class="tag model">{e(model)}</span>
    <span class="tag">{e(state)}</span>
    <span class="tag" style="background:#fce4ec;color:#880e4f">concept: {e(concept)}</span>
  </div>

  <div class="section-label">Context C</div>
  <div class="context-box">{e(chunk)}</div>

  <div class="section-label">Student Utterance U</div>
  <div class="utterance-box">{e(utt)}</div>

  <div class="section-label">Tutor Response R</div>
  <div class="response-box">{e(resp)}</div>

  <div class="section-label">Our Scores (for reference)</div>
  <div class="scores-row">
    <div class="score-box"><div class="label">Perception</div><div class="value">{e(str(p))}</div></div>
    <div class="score-box"><div class="label">Orchestration</div><div class="value">{e(str(o))}</div></div>
    <div class="score-box"><div class="label">Elicitation</div><div class="value">{e(str(el))}</div></div>
    <div class="score-box score-total"><div class="label">Total</div><div class="value">{e(str(total))}</div></div>
  </div>
  <p class="csv-note">Enter YOUR_PERCEPTION, YOUR_ORCHESTRATION, YOUR_ELICITATION in CSV row {row_id}.</p>
</div>
""")

    parts.append(HTML_FOOT)

    with open(M3_OUTPUT, "w", encoding="utf-8") as f:
        f.write("".join(parts))

    print(f"Saved M3 viewer → {M3_OUTPUT}  ({len(items)} items)")


if __name__ == "__main__":
    build_m2()
    build_m3()
    print("\nDone. Send professors:")
    print("  • The HTML viewer (open in browser — math renders automatically)")
    print("  • The matching CSV (import into Google Sheets — fill YOUR_* columns)")
