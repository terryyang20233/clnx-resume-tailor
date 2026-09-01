# CLNx Resume Tailor

**English** | [中文](README.zh-CN.md)

Chrome extension plus a local Python server that turns a University of Toronto [CLNx](https://clnx.utoronto.ca) work-study posting into a tailored one-page PDF resume.

This is an **unofficial personal tool**. It is not affiliated with, endorsed by, or supported by the University of Toronto or CLNx.

```
CLNx posting  →  Chrome extension  →  127.0.0.1:18765  →  applications/<id>-<slug>/
                                                              job.json  job.md
                                                              resume.tex  resume.pdf
                                                              selection.json
```

The selector ranks bullets from a local bank (`resume_data.py`) by keyword overlap with the posting, then compiles with `pdflatex` and greedily drops the least relevant blocks until the PDF is one page.

The committed `resume_data.py` is a **fictional sample** (Alex Rivera / example.com). Put your own heading and bullets there. Do not commit real applications, transcripts, or a full personal dump if the repo is public.

## Requirements

- Python 3.10+
- [MacTeX](https://www.tug.org/mactex/) or [TeX Live](https://tug.org/texlive/) with `pdflatex` (and optionally `pdfinfo`)
- Chrome (unpacked extension)
- A CLNx login (the extension only runs on `https://clnx.utoronto.ca/*`)

## Setup

1. Clone this repository.
2. Replace the sample person in `resume_data.py` with your heading, education, experience, projects, and skills. Strings may contain LaTeX.
3. Start the local server (binds to loopback only):

   ```bash
   python3 server.py
   ```

4. In Chrome: `chrome://extensions` → Developer mode → Load unpacked → select the `extension/` folder.
5. Open a CLNx work-study posting (`#postingDiv`). Click **Create 1-page resume**.

From the listing table (`#postingsTable`) the panel only helps you open a posting. Tailoring needs the full description page.

## CLI (no extension)

```bash
python3 tailor.py examples/sample-job.json
```

`examples/sample-job.json` is a made-up posting, not a real CLNx job.

## What gets written

Each run creates `applications/<posting-id>-<title-slug>/`:

| File | Purpose |
|------|---------|
| `job.json` | Raw fields scraped from the posting page |
| `job.md` | Same posting as markdown |
| `resume.tex` / `resume.pdf` | Tailored one-pager |
| `selection.json` | Which bank items were kept and why |

`applications/` is gitignored (except `.gitkeep`). Generated PDFs stay on your machine unless you add them yourself.

## Privacy

- The HTTP server listens on `127.0.0.1` only. Job text is not sent to any remote API.
- CORS is limited to `https://clnx.utoronto.ca` (and Chrome extension origins). Arbitrary websites cannot call the local server from the browser.
- Keep `applications/` and a filled-in `resume_data.py` out of public remotes if they contain personal data.

## License

MIT. LaTeX section macros in `preamble.tex` follow [Jake Gutierrez / sb2nov resume](https://github.com/sb2nov/resume) (MIT).
