# I defined these sample job descriptions to represent SDE, Data Analyst, and Consulting roles.
# Each job has a clear ID, title, and key requirements text.
sample_job_descriptions = [
    {
        "id": "sde",
        "title": "Software Development Engineer (SDE)",
        "description": "We are looking for an SDE to build and scale backend services. You will design APIs, work with AWS, and optimize PostgreSQL databases. Requirements: 3+ years experience with Python, Node.js, or Java, experience with AWS (S3, EC2), and strong understanding of database indexing and SQL."
    },
    {
        "id": "data_analyst",
        "title": "Data Analyst",
        "description": "Looking for a Data Analyst to transform raw database queries into business insights. You will create charts, build reports, and present dashboards. Requirements: Proficiency in Python (Pandas/NumPy), strong SQL query optimization skills, and experience building dashboards in PowerBI or Tableau."
    },
    {
        "id": "consultant",
        "title": "Management Consultant",
        "description": "Seeking a Management Consultant to advise corporate clients on strategy, operational efficiency, and technology transformation. Requirements: MBA from a top-tier institution, strong slide presentation skills, business analysis experience, and excellent verbal and written communication."
    }
]

# I grouped the candidate evaluation results by their target job ID.
# This serves as our offline database, letting the recruiter test the dashboard instantly without needing a Gemini key.
# I used common Indian names and gave each candidate a realistic set of skills, strengths, and weaknesses.
sample_candidates = {
    "sde": [
        {
            "id": "aarav_mehta",
            "name": "Aarav Mehta",
            "role": "Backend Developer",
            "score": 92,
            "recommendation": "Strong Fit",
            "strengths": [
                "Has 4 years of experience with Python/Node.js, writing clean APIs.",
                "Demonstrated deep knowledge of AWS deployment (EC2, Lambda, S3).",
                "Expert in PostgreSQL database query optimization and index design."
            ],
            "gaps": [
                "Limited experience with frontend frameworks like React or Vue.",
                "No prior experience with Docker container orchestration."
            ],
            "email_draft": "Hi Aarav,\n\nI was highly impressed by your backend experience, particularly your work optimizing PostgreSQL databases and AWS cloud architecture. We would love to invite you for a technical interview next week.\n\nBest regards,\nRecruiting Team",
            "resume_text": "Aarav Mehta - Backend Engineer\nEmail: aarav.mehta@email.com | Location: Bengaluru, India\n\nEXPERIENCE:\n- Senior Developer at TechStack India (3 years): Built REST APIs using Python/FastAPI. Managed postgres indexing which reduced query latency by 35%.\n- Software Engineer at AppBuilders (1.5 years): Configured AWS infrastructure (EC2, S3, RDS) and deployed backend microservices.\n\nSKILLS:\nPython, Node.js, PostgreSQL, AWS, Git, System Design."
        },
        {
            "id": "neha_verma",
            "name": "Neha Verma",
            "role": "Fullstack Developer",
            "score": 75,
            "recommendation": "Moderate Fit",
            "strengths": [
                "Strong understanding of Node.js backend development and REST APIs.",
                "Solid foundations in JavaScript and clean code principles."
            ],
            "gaps": [
                "AWS experience is limited to basic hosting; lacks cloud infrastructure depth.",
                "PostgreSQL query optimization skills are basic."
            ],
            "email_draft": "Hi Neha,\n\nThank you for applying. We noticed your strong Node.js experience and would like to schedule a brief screening call to discuss our SDE opening.\n\nBest regards,\nRecruiting Team",
            "resume_text": "Neha Verma - Fullstack Developer\nEmail: neha.verma@email.com | Location: Delhi NCR, India\n\nEXPERIENCE:\n- Software Engineer at WebSolutions (2 years): Maintained Node.js APIs and integrated third-party payment gateways. Assisted with basic AWS deployments.\n\nSKILLS:\nJavaScript, Node.js, Express, React, MongoDB, SQL, Git."
        },
        {
            "id": "karan_kapoor",
            "name": "Karan Kapoor",
            "role": "Operations Analyst",
            "score": 28,
            "recommendation": "Not Fit",
            "strengths": [
                "Familiar with basic Excel reporting and team coordination."
            ],
            "gaps": [
                "Lacks essential backend languages like Python, Node.js, or Java.",
                "No experience working with database management or AWS cloud systems.",
                "Does not meet the coding requirements for the SDE engineering role."
            ],
            "email_draft": "Hi Karan,\n\nThank you for your interest in the SDE role. After reviewing your resume, we feel your background in Operations doesn't quite match the coding requirements we need right now. We will keep your resume on file for operations openings.\n\nBest regards,\nRecruiting Team",
            "resume_text": "Karan Kapoor - Operations Specialist\nEmail: karan.kapoor@email.com | Location: Mumbai, India\n\nEXPERIENCE:\n- Operations Associate at LogiCorp (3 years): Optimized delivery schedules and tracked KPIs using Microsoft Excel.\n- Coordinator at EventPlanners (1 year): Handled vendor outreach and logistical planning.\n\nSKILLS:\nExcel, Vendor Management, Team Leadership, Operational Analytics."
        }
    ],
    "data_analyst": [
        {
            "id": "priya_sharma",
            "name": "Priya Sharma",
            "role": "Data Analyst",
            "score": 95,
            "recommendation": "Strong Fit",
            "strengths": [
                "Excellent SQL skills; writes complex CTE queries and database aggregations.",
                "Highly proficient in Python scripting (Pandas, NumPy, Matplotlib).",
                "Built over 15 executive dashboards in PowerBI with clean data models."
            ],
            "gaps": [
                "No experience with cloud data lakes like Snowflake or BigQuery.",
                "Has not worked with real-time streaming tools like Kafka."
            ],
            "email_draft": "Hi Priya,\n\nYour profile caught our attention due to your excellent work building PowerBI dashboards and writing advanced SQL queries. We would love to discuss our Data Analyst role with you.\n\nBest regards,\nRecruiting Team",
            "resume_text": "Priya Sharma - Data Analyst\nEmail: priya.sharma@email.com | Location: Pune, India\n\nEXPERIENCE:\n- Data Analyst at AnalyticsHub (2.5 years): Structured data warehouses and built interactive dashboards using PowerBI. Optimized SQL query runtimes by 20%.\n- Analyst Intern at InfoMetrics (6 months): Used Python Pandas to clean client datasets and generated monthly PDF summaries.\n\nSKILLS:\nSQL, Python (Pandas/NumPy), PowerBI, Excel, Tableau."
        },
        {
            "id": "neha_verma",
            "name": "Neha Verma",
            "role": "Fullstack Developer",
            "score": 64,
            "recommendation": "Moderate Fit",
            "strengths": [
                "Familiar with standard SQL querying (joins, groupings).",
                "Excellent general-purpose Python programming skills."
            ],
            "gaps": [
                "Lacks dedicated business dashboard experience (PowerBI/Tableau).",
                "Has primarily worked on web applications rather than data-centric analytics."
            ],
            "email_draft": "Hi Neha,\n\nWe saw your background in web development. Since we need data-centric dashboarding, we would like to schedule an exploratory call to see if your analytical skills align with our goals.\n\nBest regards,\nRecruiting Team",
            "resume_text": "Neha Verma - Fullstack Developer\nEmail: neha.verma@email.com | Location: Delhi NCR, India\n\nEXPERIENCE:\n- Software Engineer at WebSolutions (2 years): Handled backend database scripts and configured SQL queries for web metrics dashboards.\n\nSKILLS:\nJavaScript, Node.js, Express, React, MongoDB, SQL, Git."
        }
    ],
    "consultant": [
        {
            "id": "ananya_iyer",
            "name": "Ananya Iyer",
            "role": "Business Consultant",
            "score": 94,
            "recommendation": "Strong Fit",
            "strengths": [
                "Top-tier MBA graduate with outstanding strategic analysis skills.",
                "Excellent communication and slide design skills (expert in PowerPoint).",
                "Led client workshops that optimized business operations by 15%."
            ],
            "gaps": [
                "Lacks deep technical background in coding or script writing.",
                "Prior experience has focused more on operations than financial modeling."
            ],
            "email_draft": "Hi Ananya,\n\nYour management consulting background and MBA credentials look perfect for this role. We would love to schedule a case interview next week.\n\nBest regards,\nRecruiting Team",
            "resume_text": "Ananya Iyer - Business Consultant\nEmail: ananya.iyer@email.com | Location: Hyderabad, India\n\nEXPERIENCE:\n- Strategy Consultant at ApexAdvisory (3 years): Advised clients on process re-engineering and prepared executive presentation decks.\n- Business Intern at GrowthCorp (6 months): Conducted competitor research and industry gap analysis.\n\nEDUCATION:\n- MBA, Indian Institute of Management (IIM) (2023)\n\nSKILLS:\nBusiness Analysis, Strategy, Slide Presentations, Financial Modeling, Client Relations."
        },
        {
            "id": "rohan_deshmukh",
            "name": "Rohan Deshmukh",
            "role": "Associate Product Manager",
            "score": 72,
            "recommendation": "Moderate Fit",
            "strengths": [
                "Strong understanding of product planning, Agile, and customer workflows.",
                "Great communication and stakeholder presentation skills."
            ],
            "gaps": [
                "Lacks formal consulting experience advising external corporate clients.",
                "Limited exposure to corporate operational strategy audits."
            ],
            "email_draft": "Hi Rohan,\n\nYour product management experience shows strong business thinking. We would love to speak with you regarding how your skills align with our management consulting team.\n\nBest regards,\nRecruiting Team",
            "resume_text": "Rohan Deshmukh - Product Manager\nEmail: rohan.deshmukh@email.com | Location: Bengaluru, India\n\nEXPERIENCE:\n- Associate PM at InnovateTech (2 years): Gathered user feedback and coordinated roadmaps. Designed slides to align teams on goals.\n- Business Analyst (1 year): Analyzed product metrics and generated user reports.\n\nSKILLS:\nProduct Roadmap, Agile, Stakeholder Management, Jira, PowerPoint."
        }
    ]
}
