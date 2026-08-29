# CLNx Resume Tailor

Chrome extension plus a local Python server that turns a University of Toronto [CLNx](https://clnx.utoronto.ca) work-study posting into a one-page PDF resume.

```
CLNx posting  →  Chrome extension  →  127.0.0.1:18765  →  applications/<id>-<slug>/
                                                              job.json  job.md
                                                              resume.tex  resume.pdf
                                                              selection.json
```

The selector is keyword overlap against a local bullet bank (`resume_data.py`), then `pdflatex` with greedy shrinking until the PDF is one page.

This repo is the **tool**. Put your own contact info and bullets in `resume_data.py`. Do not commit real applications, transcripts, or a full personal resume dump if the repo is public.

## Requirements

- Python 3.10+
- [MacTeX](https://www.tug.org/mactex/) or another TeX distribution with `pdflatex` (and optionally `pdfinfo`)
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

## What gets written

Each run creates `applications/<posting-id>-<title-slug>/`:

| File | Purpose |
|------|---------|
| `job.json` | Raw fields scraped from CLNx |
| `job.md` | Same posting as markdown |
| `resume.tex` / `resume.pdf` | Tailored one-pager |
| `selection.json` | Which bank items were kept and why |

Generated PDFs are gitignored.

## Privacy

- The HTTP server listens on `127.0.0.1` only. Job text never leaves your machine unless you push `applications/`.
- Keep `applications/` and a filled-in `resume_data.py` out of public remotes if they contain personal data.

## License

MIT. LaTeX section macros in `preamble.tex` follow [Jake Gutierrez / sb2nov resume](https://github.com/sb2nov/resume) (MIT).
