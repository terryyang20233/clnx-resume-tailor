#!/usr/bin/env python3
"""Select a one-page subset of resume_data.py from a CLNx job posting."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import resume_data as data

ROOT = Path(__file__).resolve().parent
PREAMBLE = (ROOT / "preamble.tex").read_text(encoding="utf-8")
APPLICATIONS = ROOT / "applications"

STOP = {
    "a", "an", "the", "and", "or", "of", "to", "in", "for", "with", "on", "at", "by",
    "from", "as", "is", "are", "was", "be", "this", "that", "these", "those", "you",
    "your", "will", "our", "we", "they", "their", "it", "its", "into", "about",
    "through", "during", "including", "here", "what", "get", "need", "love", "role",
    "must", "can", "may", "not", "no", "more", "than", "per", "week", "hours",
    "position", "posting", "study", "work", "job", "student", "students", "please",
    "using", "used", "use", "also", "such", "other", "any", "all", "both", "each",
    "have", "has", "had", "do", "does", "done", "make", "made", "able", "ability",
    "required", "requirements", "essential", "asset", "while", "without", "under",
    "within", "between", "over", "after", "before", "further", "desired", "available",
}

FIELD_WEIGHT = {
    "Work Study Position Title": 4.0,
    "Position Type": 3.0,
    "Skills": 3.5,
    "Qualifications": 3.0,
    "Position Description": 2.5,
    "Department / Unit Overview": 1.8,
    "Department / Unit": 1.5,
    "Division": 1.2,
    "Organization": 1.0,
}

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z+#]+")


def strip_tex(text: str) -> str:
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    return text


def tokens(text: str) -> list[str]:
    out = []
    for raw in TOKEN_RE.findall(text.lower()):
        if raw in STOP or len(raw) < 3:
            continue
        if raw.endswith("ing") and len(raw) > 6:
            raw = raw[:-3]
        elif raw.endswith("tion") and len(raw) > 7:
            raw = raw[:-4]
        elif raw.endswith("ers") and len(raw) > 5:
            raw = raw[:-1]
        elif raw.endswith("ies") and len(raw) > 5:
            raw = raw[:-3] + "y"
        elif raw.endswith("s") and not raw.endswith("ss") and len(raw) > 4:
            raw = raw[:-1]
        out.append(raw)
    return out


def job_weights(job: dict) -> dict[str, float]:
    fields = job.get("fields") or {}
    heading = job.get("heading") or ""
    title = fields.get("Work Study Position Title") or heading
    weights: dict[str, float] = {}

    def add(text: str, w: float) -> None:
        for tok in tokens(text):
            weights[tok] = weights.get(tok, 0.0) + w

    add(heading, 3.0)
    add(title, 4.0)
    for key, value in fields.items():
        add(str(value), FIELD_WEIGHT.get(key, 0.8))
    return weights


def score_text(text: str, weights: dict[str, float]) -> float:
    plain = strip_tex(text)
    seen = tokens(plain)
    if not seen:
        return 0.0
    total = sum(weights.get(tok, 0.0) for tok in seen)
    uniq = {tok for tok in seen if tok in weights}
    return total + 1.5 * len(uniq)


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return text[:60] or "job"


def posting_id(job: dict) -> str:
    heading = job.get("heading") or ""
    m = re.match(r"(\d+)", heading)
    if m:
        return m.group(1)
    fields = job.get("fields") or {}
    return str(fields.get("id") or job.get("id") or "job")


def latex_items(bullets: list[str]) -> str:
    lines = ["      \\resumeItemListStart"]
    for b in bullets:
        lines.append(f"        \\resumeItem{{{b}}}")
    lines.append("      \\resumeItemListEnd")
    return "\n".join(lines)


def pick_bullets(bullets: list[str], weights: dict[str, float], k: int) -> tuple[list[str], float]:
    ranked = sorted(((score_text(b, weights), i, b) for i, b in enumerate(bullets)), reverse=True)
    chosen = [b for _, _, b in ranked[:k] if ranked]
    chosen.sort(key=lambda b: bullets.index(b))
    best = ranked[0][0] if ranked else 0.0
    return chosen, best


def select(job: dict) -> dict:
    weights = job_weights(job)

    edu = []
    for item in data.EDUCATION:
        bullets, _ = pick_bullets(item["bullets"], weights, 1)
        edu.append({**item, "bullets": bullets})

    exp_blocks = []
    for job_exp in data.EXPERIENCE:
        roles_out = []
        best = 0.0
        for role in job_exp["roles"]:
            bullets, role_score = pick_bullets(role["bullets"], weights, 2)
            header = " ".join(
                x for x in [job_exp["title"], job_exp["org"], role.get("title") or ""] if x
            )
            role_score += 0.35 * score_text(header, weights)
            if role_score <= 0:
                continue
            roles_out.append({**role, "bullets": bullets, "score": role_score})
            best = max(best, role_score)
        if roles_out:
            roles_out.sort(key=lambda r: r["score"], reverse=True)
            exp_blocks.append({**job_exp, "roles": roles_out, "score": best})
    exp_blocks.sort(key=lambda x: x["score"], reverse=True)

    projects = []
    for p in data.PROJECTS:
        bullets, bscore = pick_bullets(p["bullets"], weights, 2)
        score = bscore + 0.4 * score_text(p["heading"], weights)
        if score > 0:
            projects.append({**p, "bullets": bullets, "score": score})
    projects.sort(key=lambda x: x["score"], reverse=True)

    def rank_simple(items: list[dict], extra: str = "") -> list[dict]:
        out = []
        for item in items:
            blob = " ".join(
                [item.get("title") or "", item.get("org") or "", item.get("heading") or "", extra]
                + item.get("bullets", [])
            )
            sc = score_text(blob, weights)
            if sc > 0:
                bullets = item.get("bullets")
                if bullets:
                    kept, _ = pick_bullets(bullets, weights, 1)
                    item = {**item, "bullets": kept}
                out.append({**item, "score": sc})
        out.sort(key=lambda x: x["score"], reverse=True)
        return out

    leadership = rank_simple(data.LEADERSHIP)
    volunteering = rank_simple(data.VOLUNTEERING)
    awards = rank_simple(data.AWARDS)
    certs = rank_simple(data.CERTS)

    skill_lines = []
    for line in data.SKILL_LINES:
        sc = score_text(f"{line['label']} {line['value']}", weights)
        # Spoken languages: keep if communication / language / chinese / english in JD
        if sc > 0 or line["id"] == "lang" and score_text("communication english chinese language", weights) > 0:
            skill_lines.append({**line, "score": sc})
    if not skill_lines:
        skill_lines = [{**data.SKILL_LINES[0], "score": 0}]

    interests_score = score_text(data.INTERESTS, weights)

    # Greedy fill by relevance; education always in.
    plan = {
        "education": edu,
        "experience": exp_blocks[:2],
        "projects": projects[:1],
        "leadership": leadership[:2],
        "volunteering": volunteering[:1],
        "awards": awards[:2],
        "certs": certs[:1],
        "skills": skill_lines[:3] if len(skill_lines) > 1 else skill_lines,
        "interests": data.INTERESTS if interests_score >= 8 else None,
        "weights_top": sorted(weights.items(), key=lambda kv: kv[1], reverse=True)[:40],
        "scores": {
            "experience": [(x["id"], round(x["score"], 2)) for x in exp_blocks],
            "projects": [(x["id"], round(x["score"], 2)) for x in projects],
            "leadership": [(x["id"], round(x["score"], 2)) for x in leadership],
            "volunteering": [(x["id"], round(x["score"], 2)) for x in volunteering],
        },
    }

    # Drop weak tails: require some absolute score so unrelated clubs vanish.
    plan["experience"] = [x for x in plan["experience"] if x["score"] >= 4]
    if not plan["experience"] and exp_blocks:
        plan["experience"] = exp_blocks[:1]
    plan["projects"] = [x for x in plan["projects"] if x["score"] >= 5]
    plan["leadership"] = [x for x in plan["leadership"] if x["score"] >= 4][:2]
    plan["volunteering"] = [x for x in plan["volunteering"] if x["score"] >= 4][:1]
    plan["awards"] = [x for x in plan["awards"] if x["score"] >= 3][:2]
    plan["certs"] = [x for x in plan["certs"] if x["score"] >= 4][:1]
    return plan


def render(plan: dict) -> str:
    h = data.HEADING
    parts = [
        PREAMBLE,
        rf"\hypersetup{{pdftitle={{{h['name']} --- Resume}}, pdfauthor={{{h['name']}}}}}",
        r"\begin{document}",
        r"\begin{center}",
        rf"    \textbf{{\Huge {h['name']}}} \\ \vspace{{1pt}}",
        rf"    \small {h['phone']} $|$",
        rf"    \href{{mailto:{h['email']}}}{{\underline{{{h['email']}}}}} $|$",
        rf"    \href{{{h['linkedin']}}}{{\underline{{{h['linkedin_text']}}}}} $|$",
        rf"    \href{{{h['github']}}}{{\underline{{{h['github_text']}}}}} \\",
        rf"    \href{{{h['site']}}}{{\underline{{{h['site_text']}}}}}",
        r"\end{center}",
        "",
        r"\section{Education}",
        r"  \resumeSubHeadingListStart",
    ]
    for item in plan["education"]:
        parts.append(rf"    \resumeSubheading")
        parts.append(rf"      {{{item['school']}}}{{{item['location']}}}")
        parts.append(rf"      {{{item['degree']}}}{{{item['dates']}}}")
        if item.get("bullets"):
            parts.append(latex_items(item["bullets"]))
    parts += [r"  \resumeSubHeadingListEnd", ""]

    if plan["experience"]:
        parts += [r"\section{Experience}", r"  \resumeSubHeadingListStart", ""]
        for exp in plan["experience"]:
            parts.append(r"    \resumeSubheading")
            parts.append(rf"      {{{exp['title']}}}{{{exp['dates']}}}")
            parts.append(rf"      {{{exp['org']}}}{{{exp['location']}}}")
            for role in exp["roles"]:
                if role.get("title"):
                    parts.append(r"    \resumeSubSubheading")
                    parts.append(rf"      {{{role['title']}}}{{{role['dates']}}}")
                if role.get("bullets"):
                    parts.append(latex_items(role["bullets"]))
            parts.append("")
        parts.append(r"  \resumeSubHeadingListEnd")
        parts.append("")

    if plan["projects"]:
        parts += [r"\section{Projects}", r"    \resumeSubHeadingListStart"]
        for p in plan["projects"]:
            parts.append(r"      \resumeProjectHeading")
            parts.append(rf"          {{{p['heading']}}}{{{p['dates']}}}")
            if p.get("bullets"):
                parts.append(latex_items(p["bullets"]))
        parts += [r"    \resumeSubHeadingListEnd", ""]

    if plan["leadership"]:
        parts += [r"\section{Leadership \& Extracurriculars}", r"  \resumeSubHeadingListStart", ""]
        for item in plan["leadership"]:
            parts.append(r"    \resumeSubheading")
            parts.append(rf"      {{{item['title']}}}{{{item['dates']}}}")
            parts.append(rf"      {{{item['org']}}}{{{item['location']}}}")
            if item.get("bullets"):
                parts.append(latex_items(item["bullets"]))
            parts.append("")
        parts.append(r"  \resumeSubHeadingListEnd")
        parts.append("")

    if plan["volunteering"]:
        parts += [r"\section{Volunteering}", r"  \resumeSubHeadingListStart", ""]
        for item in plan["volunteering"]:
            parts.append(r"    \resumeSubheading")
            parts.append(rf"      {{{item['title']}}}{{{item['dates']}}}")
            parts.append(rf"      {{{item['org']}}}{{{item['location']}}}")
            if item.get("bullets"):
                parts.append(latex_items(item["bullets"]))
            parts.append("")
        parts.append(r"  \resumeSubHeadingListEnd")
        parts.append("")

    if plan["awards"]:
        parts += [r"\section{Honours \& Awards}", r"    \resumeSubHeadingListStart"]
        for item in plan["awards"]:
            parts.append(r"      \resumeProjectHeading")
            parts.append(rf"          {{{item['heading']}}}{{{item['dates']}}}")
        parts += [r"    \resumeSubHeadingListEnd", ""]

    if plan["certs"]:
        parts += [r"\section{Certifications}", r"    \resumeSubHeadingListStart"]
        for item in plan["certs"]:
            parts.append(r"      \resumeProjectHeading")
            parts.append(rf"          {{{item['heading']}}}{{{item['dates']}}}")
        parts += [r"    \resumeSubHeadingListEnd", ""]

    if plan["skills"]:
        parts.append(r"\section{Technical Skills}")
        parts.append(r" \begin{itemize}[leftmargin=0.15in, label={}]")
        parts.append(r"    \small{\item{")
        skill_tex = " \\\\\n".join(
            rf"     \textbf{{{s['label']}}}{{: {s['value']}}}" for s in plan["skills"]
        )
        parts.append(skill_tex)
        parts.append(r"    }}")
        parts.append(r" \end{itemize}")
        parts.append("")

    if plan.get("interests"):
        parts.append(r"\section{Interests}")
        parts.append(r" \begin{itemize}[leftmargin=0.15in, label={}]")
        parts.append(r"    \small{\item{")
        parts.append(rf"     {plan['interests']}")
        parts.append(r"    }}")
        parts.append(r" \end{itemize}")
        parts.append("")

    parts += [r"\end{document}", ""]
    return "\n".join(parts)


def pdf_pages(pdf_path: Path) -> int:
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        out = subprocess.check_output([pdfinfo, str(pdf_path)], text=True)
        for line in out.splitlines():
            if line.lower().startswith("pages:"):
                return int(line.split(":")[1].strip())
    tex = pdf_path.with_suffix(".log")
    if tex.exists():
        log = tex.read_text(encoding="utf-8", errors="ignore")
        if "[2]" in log or "Output written on" in log and "pages" in log:
            m = re.search(r"Output written on .* \((\d+) page", log)
            if m:
                return int(m.group(1))
    return 1


def compile_tex(tex_path: Path) -> Path:
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=tex_path.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    return tex_path.with_suffix(".pdf")


def shrink(plan: dict) -> bool:
    """Drop the least relevant optional block. Return False if nothing left to drop."""
    optional = []
    if plan.get("interests"):
        optional.append(("interests", 0))
    if plan.get("certs"):
        optional.append(("certs", plan["certs"][-1]["score"]))
    if plan.get("awards"):
        optional.append(("awards", plan["awards"][-1]["score"]))
    if len(plan.get("volunteering") or []) >= 1:
        optional.append(("volunteering", plan["volunteering"][-1]["score"]))
    if len(plan.get("leadership") or []) >= 1:
        optional.append(("leadership", plan["leadership"][-1]["score"]))
    if len(plan.get("projects") or []) >= 1:
        optional.append(("projects", plan["projects"][-1]["score"]))
    if len(plan.get("skills") or []) > 2:
        optional.append(("skills", plan["skills"][-1].get("score", 0)))
    if len(plan.get("experience") or []) >= 2:
        optional.append(("experience", plan["experience"][-1]["score"]))
    # Trim extra bullets in last experience role
    for exp in reversed(plan.get("experience") or []):
        for role in reversed(exp["roles"]):
            if len(role.get("bullets") or []) > 1:
                role["bullets"] = role["bullets"][:1]
                return True
    if not optional:
        return False
    optional.sort(key=lambda x: x[1])
    key = optional[0][0]
    if key == "interests":
        plan["interests"] = None
    elif key == "skills":
        plan["skills"] = plan["skills"][:-1]
    else:
        plan[key] = plan[key][:-1]
    return True


def job_markdown(job: dict) -> str:
    fields = job.get("fields") or {}
    lines = [f"# {job.get('heading') or fields.get('Work Study Position Title')}", ""]
    if job.get("url"):
        lines.append(f"Source: {job['url']}")
        lines.append("")
    for k, v in fields.items():
        lines.append(f"## {k}")
        lines.append("")
        lines.append(str(v).strip())
        lines.append("")
    return "\n".join(lines)


def tailor(job: dict) -> dict:
    APPLICATIONS.mkdir(exist_ok=True)
    pid = posting_id(job)
    title = (job.get("fields") or {}).get("Work Study Position Title") or job.get("heading") or "job"
    folder = APPLICATIONS / f"{pid}-{slugify(strip_tex(title))}"
    folder.mkdir(parents=True, exist_ok=True)

    (folder / "job.json").write_text(json.dumps(job, indent=2, ensure_ascii=False), encoding="utf-8")
    (folder / "job.md").write_text(job_markdown(job), encoding="utf-8")

    plan = select(job)
    tex_path = folder / "resume.tex"
    pdf_path = folder / "resume.pdf"
    pages = None
    for _ in range(12):
        tex_path.write_text(render(plan), encoding="utf-8")
        compile_tex(tex_path)
        pages = pdf_pages(pdf_path)
        if pages <= 1:
            break
        if not shrink(plan):
            break

    (folder / "selection.json").write_text(
        json.dumps(
            {
                "pages": pages,
                "scores": plan.get("scores"),
                "kept": {
                    "experience": [x["id"] for x in plan.get("experience") or []],
                    "projects": [x["id"] for x in plan.get("projects") or []],
                    "leadership": [x["id"] for x in plan.get("leadership") or []],
                    "volunteering": [x["id"] for x in plan.get("volunteering") or []],
                    "awards": [x["id"] for x in plan.get("awards") or []],
                    "certs": [x["id"] for x in plan.get("certs") or []],
                    "skills": [x["id"] for x in plan.get("skills") or []],
                    "interests": bool(plan.get("interests")),
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return {
        "ok": True,
        "pages": pages,
        "folder": str(folder.relative_to(ROOT)),
        "pdf": str(pdf_path.relative_to(ROOT)) if pdf_path.exists() else None,
        "tex": str(tex_path.relative_to(ROOT)),
        "title": title,
        "id": pid,
        "kept": json.loads((folder / "selection.json").read_text(encoding="utf-8"))["kept"],
    }


if __name__ == "__main__":
    import sys

    job = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(tailor(job), indent=2))
