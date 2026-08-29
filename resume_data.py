"""Replace this file with your own resume bank.

Each bullet is a candidate line. The tailor scores bullets against a CLNx
posting and keeps a one-page subset. LaTeX is allowed in strings.
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
        "id": "uoft",
        "school": r"University of Toronto",
        "location": r"Toronto, ON",
        "degree": r"B.A.Sc.\ in Engineering Science",
        "dates": r"Sept. 2026 -- Present",
        "bullets": [
            r"Dean's List; coursework in robotics, signals, and computing",
        ],
        "always": True,
    },
]

EXPERIENCE = [
    {
        "id": "lab",
        "title": r"Research Assistant",
        "dates": r"May 2025 -- Aug. 2026",
        "org": r"Example Robotics Lab",
        "location": r"Toronto, ON",
        "roles": [
            {
                "id": "vision",
                "title": r"Perception",
                "dates": r"May 2026 -- Aug. 2026",
                "bullets": [
                    r"Trained a YOLO detector for thin obstacles in aerial imagery and evaluated transfer to onboard video",
                    r"Labeled 200+ images and added edge-aware augmentation for blur and low light",
                    r"Wrote ROS~2 nodes to publish detections at 20\,Hz for a downstream planner",
                ],
            },
            {
                "id": "sim",
                "title": r"Simulation",
                "dates": r"May 2025 -- Aug. 2025",
                "bullets": [
                    r"Built a Gazebo software-in-the-loop stack sharing one capture core with the live graph",
                    r"Unit-tested intercept timing under $v_{\max}$ and $a_{\max}$ constraints",
                ],
            },
        ],
    },
    {
        "id": "tutor",
        "title": r"Instructor",
        "dates": r"July 2025 -- July 2026",
        "org": r"Example Academy",
        "location": r"Toronto, ON",
        "roles": [
            {
                "id": "tutor-main",
                "title": None,
                "dates": None,
                "bullets": [
                    r"Led weekly small-group sessions of about 10 students through homework and contest strategies",
                    r"Ran question-driven recitations and assigned targeted practice on weak topics",
                ],
            }
        ],
    },
]

PROJECTS = [
    {
        "id": "patrol",
        "heading": r"\textbf{Patrol Robot} $|$ \emph{YOLO, SLAM, LiDAR}",
        "dates": r"June 2024 -- Apr. 2025",
        "bullets": [
            r"Built a patrol robot that detects fire in real time and alerts an operator",
            r"Used vision--LiDAR SLAM for mapping, navigation, and dynamic obstacle avoidance",
        ],
    },
    {
        "id": "site",
        "heading": r"\textbf{Personal Site} $|$ \emph{Astro, TypeScript}",
        "dates": r"June 2026 -- Present",
        "bullets": [
            r"Notes site on robotics and computer vision, deployed as a static app",
        ],
    },
]

LEADERSHIP = [
    {
        "id": "club",
        "title": r"President, Robotics Club",
        "dates": r"Sept. 2024 -- June 2026",
        "org": r"Example Secondary School",
        "location": r"Toronto, ON",
        "bullets": [
            r"Coordinated build seasons, outreach, and match-day software reliability",
        ],
    },
]

VOLUNTEERING = [
    {
        "id": "tutor-vol",
        "title": r"Tutor",
        "dates": r"Nov. 2024 -- June 2026",
        "org": r"Community Program",
        "location": r"Toronto, ON",
        "bullets": [
            r"Tutored newcomers in English conversation, 3+ hours per week",
        ],
    },
]

AWARDS = [
    {
        "id": "dean",
        "heading": r"\textbf{Dean's List} $|$ \emph{University of Toronto}",
        "dates": r"2026",
    },
]

CERTS = [
    {
        "id": "ml",
        "heading": r"\textbf{Machine Learning Specialization} $|$ \emph{DeepLearning.AI}",
        "dates": r"June 2026",
    },
]

SKILL_LINES = [
    {"id": "prog", "label": r"Programming", "value": r"Python, C++, Java, MATLAB, \LaTeX"},
    {"id": "ai", "label": r"AI \& Robotics", "value": r"PyTorch, YOLO, OpenCV, ROS~2, Gazebo"},
    {"id": "tools", "label": r"Developer Tools", "value": r"Git, VS Code"},
    {"id": "lang", "label": r"Spoken Languages", "value": r"English; French"},
]

INTERESTS = r"Hiking; Tennis; Aerial photography"
