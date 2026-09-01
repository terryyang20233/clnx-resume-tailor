"""Fictional sample resume bank. Replace with your own data before using.

Every name, school, job, and project below is invented. Do not commit real
contact info, transcripts, or a full personal dump if this repository is
public. Each bullet is a candidate line: the tailor scores them against a
CLNx posting and keeps a one-page subset. LaTeX is allowed in strings.
"""

HEADING = {
    "name": r"Alex Rivera",
    "phone": r"+1 (555) 010-0199",
    "email": r"alex.rivera@example.com",
    "linkedin": r"https://www.linkedin.com/in/example",
    "linkedin_text": r"linkedin.com/in/example",
    "github": r"https://github.com/example",
    "github_text": r"github.com/example",
    "site": r"https://example.com",
    "site_text": r"example.com",
}

EDUCATION = [
    {
        "id": "northbridge",
        "school": r"Northbridge Polytechnic",
        "location": r"Harbor City",
        "degree": r"B.Sc.\ in Applied Computing",
        "dates": r"Sept. 2024 -- Present",
        "bullets": [
            r"Coursework in databases, technical writing, and introductory statistics",
        ],
        "always": True,
    },
]

EXPERIENCE = [
    {
        "id": "archives",
        "title": r"Student Records Aide",
        "dates": r"May 2025 -- Aug. 2026",
        "org": r"Northbridge Campus Archives",
        "location": r"Harbor City",
        "roles": [
            {
                "id": "catalog",
                "title": r"Cataloguing",
                "dates": r"May 2026 -- Aug. 2026",
                "bullets": [
                    r"Entered 400+ folder labels into a shared spreadsheet and flagged duplicate accession numbers",
                    r"Wrote short scope notes so student workers could find boxes without opening every lid",
                    r"Checked out reading-room materials and logged returns the same afternoon",
                ],
            },
            {
                "id": "digitize",
                "title": r"Digitization",
                "dates": r"May 2025 -- Aug. 2025",
                "bullets": [
                    r"Scanned faded flyers at 300\,dpi and exported PDFs into a dated folder tree",
                    r"Ran a weekly checksum script so the backup disk matched the working copy",
                ],
            },
        ],
    },
    {
        "id": "cafe",
        "title": r"Shift Lead",
        "dates": r"Sept. 2024 -- Apr. 2025",
        "org": r"Maple \& Bean Cafe",
        "location": r"Harbor City",
        "roles": [
            {
                "id": "cafe-main",
                "title": None,
                "dates": None,
                "bullets": [
                    r"Opened three weekday mornings: counted the till, restocked cups, and posted the sandwich board",
                    r"Trained two new baristas on the register and the closing checklist",
                ],
            }
        ],
    },
]

PROJECTS = [
    {
        "id": "lostfound",
        "heading": r"\textbf{Campus Lost-and-Found} $|$ \emph{HTML, SQLite}",
        "dates": r"Jan. 2025 -- Apr. 2025",
        "bullets": [
            r"Built a tiny web form so staff can log umbrellas, cards, and water bottles by building",
            r"Added a search page that filters by date and location without a login",
        ],
    },
    {
        "id": "recipes",
        "heading": r"\textbf{Recipe Scaler} $|$ \emph{Python}",
        "dates": r"June 2024 -- Aug. 2024",
        "bullets": [
            r"Scaled ingredient lists for 2--12 servings and printed a grocery checklist",
        ],
    },
]

LEADERSHIP = [
    {
        "id": "games",
        "title": r"Treasurer, Board Game Society",
        "dates": r"Sept. 2024 -- Present",
        "org": r"Northbridge Polytechnic",
        "location": r"Harbor City",
        "bullets": [
            r"Tracked dues in a shared ledger and ordered replacement cards twice a term",
        ],
    },
]

VOLUNTEERING = [
    {
        "id": "bookstore",
        "title": r"Weekend Shelf Volunteer",
        "dates": r"Oct. 2024 -- June 2025",
        "org": r"Harbor City Community Bookstore",
        "location": r"Harbor City",
        "bullets": [
            r"Shelved donations and printed price stickers, 3 hours most Saturdays",
        ],
    },
]

AWARDS = [
    {
        "id": "writing",
        "heading": r"\textbf{First-Year Writing Prize} $|$ \emph{Northbridge Polytechnic}",
        "dates": r"2025",
    },
]

CERTS = [
    {
        "id": "sheets",
        "heading": r"\textbf{Spreadsheet Fundamentals} $|$ \emph{Contoso Learn}",
        "dates": r"Jan. 2025",
    },
]

SKILL_LINES = [
    {"id": "prog", "label": r"Programming", "value": r"Python, SQL, HTML, \LaTeX"},
    {"id": "data", "label": r"Data \& Records", "value": r"Excel, SQLite, CSV cleanup"},
    {"id": "tools", "label": r"Developer Tools", "value": r"Git, VS Code"},
    {"id": "lang", "label": r"Spoken Languages", "value": r"English; Spanish"},
]

INTERESTS = r"Cooking; Crossword puzzles; Community radio"
