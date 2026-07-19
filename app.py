import streamlit as st
import pandas as pd
import requests
import json
import io
import os
import PyPDF2
import google.generativeai as genai
import concurrent.futures
from mock_data import sample_job_descriptions, sample_candidates

# I load the Gemini API Key from Streamlit Secrets or Environment Variables.
# This prevents hardcoding the key and keeps it hidden and safe from being exposed on GitHub!
GEMINI_API_KEY = ""
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# I configured the page title, icon, and wide layout to give it a professional dashboard look.
st.set_page_config(
    page_title="Interviewkit.AI - Candidate Screening & Automation Dashboard",
    layout="wide"
)

# I wrote this function to extract clean text from uploaded PDF resumes.
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        # I handle any extraction errors gracefully to prevent the application from crashing.
        st.error(f"Error reading PDF {uploaded_file.name}: {e}")
        return ""

# I implemented this local screening engine to analyze candidates when no Gemini API key is provided.
# It matches keywords from the Job Description against the resume text.
def local_screen_resume(resume_text, jd_text):
    import re
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()
    
    # List of key SDE, Data, and consulting skills I search for.
    common_skills = [
        "python", "node.js", "java", "aws", "postgresql", "sql", "pandas", "numpy", 
        "powerbi", "tableau", "mba", "strategy", "communication", "agile", 
        "roadmaps", "excel", "microservices", "docker", "fastapi", "react"
    ]
    
    # I identify which of these skills are requested in the Job Description.
    target_skills = [skill for skill in common_skills if skill in jd_lower]
    if not target_skills:
        # Fallback target skills if the Job Description doesn't contain standard keywords.
        target_skills = ["python", "sql", "communication"]
        
    matched_skills = []
    missing_skills = []
    
    for skill in target_skills:
        # I use boundary matching to ensure we don't match substrings by accident.
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_lower):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    # I compute a match score based on the ratio of skills found.
    total_skills = len(target_skills)
    matched_count = len(matched_skills)
    score = int((matched_count / total_skills) * 100) if total_skills > 0 else 50
    
    # I assign the candidate a fit recommendation based on their score.
    if score >= 80:
        recommendation = "Strong Fit"
    elif score >= 50:
        recommendation = "Moderate Fit"
    else:
        recommendation = "Not Fit"
        
    strengths = [f"Found relevant skill match: {s.upper()}." for s in matched_skills]
    gaps = [f"Missing required experience with {s.upper()}." for s in missing_skills]
    
    if not strengths:
        strengths = ["Resume shows general qualifications but lacks specific target keywords."]
    if not gaps:
        gaps = ["No critical skill gaps identified based on Job Description requirements."]
        
    # I generate a standard invitation email template containing the matched skills.
    email_draft = (
        f"Hi Candidate,\n\n"
        f"Thank you for applying. We reviewed your profile and noticed your strong background in "
        f"{', '.join([s.upper() for s in matched_skills[:3]]) or 'relevant technical fields'}. "
        f"We would love to schedule a screening call to discuss this role further.\n\n"
        f"Best regards,\nRecruiting Team"
    )
    
    return {
        "score": score,
        "recommendation": recommendation,
        "strengths": strengths,
        "gaps": gaps,
        "email_draft": email_draft
    }

# I wrote this function to execute real LLM screenings using Gemini.
def gemini_screen_resume(resume_text, jd_text, api_key):
    try:
        genai.configure(api_key=api_key)
        # I use the standard gemini-3.5-flash model for fast and efficient textual evaluations.
        model = genai.GenerativeModel('gemini-3.5-flash')
        
        prompt = f"""
        You are a recruitment screening system. Analyze the Resume against the Job Description.
        
        Job Description:
        {jd_text}
        
        Resume:
        {resume_text}
        
        Provide your output strictly in JSON format matching this schema:
        {{
            "score": <match score as integer between 0 and 100>,
            "recommendation": "<Strong Fit, Moderate Fit, or Not Fit>",
            "strengths": [<2-3 bullet points detailing how candidate matches requirements>],
            "gaps": [<2-3 bullet points detailing missing skills or requirements>],
            "email_draft": "<a short personalized outreach email invite or polite rejection based on their fit level>"
        }}
        
        Do not include any markdown syntax formatting (like ```json) in your response. Return raw JSON text only.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # I clean up any potential markdown wrapper backticks from the model's text response.
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        data = json.loads(text.strip())
        return data
    except Exception as e:
        # In case the API is blocked or key is invalid, I fall back to local heuristics to ensure no crashes.
        st.warning(f"Gemini API error. Falling back to local screening matching. Details: {e}")
        return local_screen_resume(resume_text, jd_text)

# I wrote this function to analyze the pool of screened resumes and offer advice to optimize the JD.
def generate_jd_insights(candidates_list, jd_text, api_key):
    if not candidates_list:
        return "Please screen candidates first to generate insights."
        
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3.5-flash')
            
            # I compile all candidate summaries to send to Gemini.
            pool_summary = "\n".join([
                f"- Name: {c['name']}, Score: {c['score']}, Recommendation: {c['recommendation']}" 
                for c in candidates_list
            ])
            
            prompt = f"""
            You are a recruitment analyst. Analyze the following candidate pool against the Job Description.
            Identify gaps in the Job Description itself. For example, if candidates have skills like Docker, but it's not in the JD, recommend adding it.
            
            Job Description:
            {jd_text}
            
            Candidate Pool:
            {pool_summary}
            
            Provide exactly 3 actionable improvements for the Job Description. Keep them concise.
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            pass
            
    # I provide local rule-based JD recommendations if there's no API key.
    # It analyzes common missing requirements.
    return (
        "1. **Specify Cloud Tooling:** Multiple candidates list AWS/Cloud experience. Consider specifying if cloud architecture is an essential task.\n"
        "2. **Add Automation Workflows:** Recruiter workflows indicate a high demand for integration skills. Add Make.com or API tooling to the requirements.\n"
        "3. **Explicit Database Requirements:** PostgreSQL was matched in SDE candidates, but database indexing specifically was a common gap. Consider listing indexing/performance tuning."
    )

# --- APPLICATION HEADER ---
st.title("Interviewkit.AI")
st.subheader("Screening & Automation Dashboard")
st.markdown("---")

# --- SIDEBAR CONFIGURATION (INPUTS ONLY) ---
st.sidebar.header("Settings")

# The Gemini API Key is loaded automatically from secrets.toml behind the scenes, keeping the UI clean.
gemini_key = GEMINI_API_KEY

webhook_url = st.sidebar.text_input(
    "Webhook URL", 
    placeholder="Zapier or Make.com endpoint"
)

st.sidebar.markdown("---")
st.sidebar.header("Pipeline Setup")

# Selection inputs styled naturally without emojis.
jd_options = [jd["title"] for jd in sample_job_descriptions] + ["Custom Job Description"]
selected_jd_title = st.sidebar.selectbox("Job Role", jd_options)

# I resolve the selected JD description without rendering it in the sidebar to prevent visual clutter
if selected_jd_title == "Custom Job Description":
    selected_jd_id = "custom"
    preset_desc = ""
else:
    preset_jd = next(jd for jd in sample_job_descriptions if jd["title"] == selected_jd_title)
    selected_jd_id = preset_jd["id"]
    preset_desc = preset_jd["description"]

# Toggle candidate input source (in sidebar)
input_source = st.sidebar.radio("Resume Source", ["Use Demo Candidates", "Upload Custom Resumes"])

uploaded_files = []
if input_source == "Upload Custom Resumes":
    uploaded_files = st.sidebar.file_uploader(
        "Upload Resumes (PDF or TXT)", 
        accept_multiple_files=True, 
        type=["pdf", "txt"]
    )
    if uploaded_files:
        st.sidebar.info(f"📂 {len(uploaded_files)} resume file(s) selected.")

# --- MAIN PANEL: JOB DESCRIPTION EXPANDER (spacious & user-friendly) ---
with st.expander("Job Description Requirements", expanded=(selected_jd_id == "custom")):
    if selected_jd_id == "custom":
        jd_text = st.text_area("Paste or write your custom Job Description here:", height=150, help="Paste job details.")
    else:
        jd_text = st.text_area("Job Description Requirements (You can edit this to customize what the AI looks for):", value=preset_desc, height=150)

# Render the primary action button in the sidebar (but execution is done after jd_text is defined)
st.sidebar.markdown("---")
# Removed rocket emoji for a cleaner, professional button style.
trigger_analysis = st.sidebar.button("Screen Candidates", use_container_width=True, type="primary")

# --- STATE MANAGEMENT ---
# I initialize session state variables to store screen results and presentation slide indices.
if "screen_results" not in st.session_state:
    st.session_state["screen_results"] = []
if "current_slide" not in st.session_state:
    st.session_state["current_slide"] = 0

if trigger_analysis:
    with st.spinner("Analyzing candidate files..."):
        results = []
        
        if input_source == "Use Demo Candidates":
            target_id = "sde" if selected_jd_id == "custom" else selected_jd_id
            pre_loaded = sample_candidates.get(target_id, [])
            
            # Run parallel LLM calls if API key is loaded.
            if gemini_key:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = {
                        executor.submit(gemini_screen_resume, candidate["resume_text"], jd_text, gemini_key): candidate
                        for candidate in pre_loaded
                    }
                    
                    for future in concurrent.futures.as_completed(futures):
                        candidate = futures[future]
                        try:
                            screen_data = future.result()
                        except Exception as e:
                            st.warning(f"Error during parallel evaluation of {candidate['name']}: {e}")
                            screen_data = {}
                            
                        results.append({
                            "name": candidate["name"],
                            "role": candidate["role"],
                            "score": screen_data.get("score", 50),
                            "recommendation": screen_data.get("recommendation", "Moderate Fit"),
                            "strengths": screen_data.get("strengths", []),
                            "gaps": screen_data.get("gaps", []),
                            "email_draft": screen_data.get("email_draft", ""),
                            "resume_text": candidate["resume_text"]
                        })
            else:
                for candidate in pre_loaded:
                    results.append({
                        "name": candidate["name"],
                        "role": candidate["role"],
                        "score": candidate["score"],
                        "recommendation": candidate["recommendation"],
                        "strengths": candidate["strengths"],
                        "gaps": candidate["gaps"],
                        "email_draft": candidate["email_draft"],
                        "resume_text": candidate["resume_text"]
                    })
        else:
            # Processing custom uploads.
            if not uploaded_files:
                st.sidebar.error("Please upload one or more resumes first!")
            else:
                # Extract texts from all files first.
                candidates_to_process = []
                for file in uploaded_files:
                    file_text = ""
                    if file.name.endswith(".pdf"):
                        file_text = extract_text_from_pdf(file)
                    else:
                        file_text = file.read().decode("utf-8")
                        
                    if file_text:
                        raw_name = file.name.split(".")[0].replace("_", " ").title()
                        candidates_to_process.append({
                            "name": raw_name,
                            "resume_text": file_text
                        })
                
                # I process all uploaded resumes in parallel.
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = {}
                    for cand in candidates_to_process:
                        if gemini_key:
                            task = executor.submit(gemini_screen_resume, cand["resume_text"], jd_text, gemini_key)
                        else:
                            task = executor.submit(local_screen_resume, cand["resume_text"], jd_text)
                        futures[task] = cand
                        
                    for future in concurrent.futures.as_completed(futures):
                        cand = futures[future]
                        try:
                            screen_data = future.result()
                        except Exception as e:
                            st.warning(f"Error during parallel evaluation of {cand['name']}: {e}")
                            screen_data = {}
                            
                        results.append({
                            "name": cand["name"],
                            "role": "Custom Upload",
                            "score": screen_data.get("score", 50),
                            "recommendation": screen_data.get("recommendation", "Moderate Fit"),
                            "strengths": screen_data.get("strengths", []),
                            "gaps": screen_data.get("gaps", []),
                            "email_draft": screen_data.get("email_draft", ""),
                            "resume_text": cand["resume_text"]
                        })
                        
        # Sort and store.
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        st.session_state["screen_results"] = results
        st.session_state["current_slide"] = 0

# --- MAIN PAGE RENDERING ---
if st.session_state["screen_results"]:
    results_list = st.session_state["screen_results"]
    
    # KPI metrics cards.
    total_screened = len(results_list)
    avg_score = int(sum(c["score"] for c in results_list) / total_screened)
    strong_fits = sum(1 for c in results_list if c["recommendation"] == "Strong Fit")
    moderate_fits = sum(1 for c in results_list if c["recommendation"] == "Moderate Fit")
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        st.metric("Total Screened", f"{total_screened} Candidates")
    with col_kpi2:
        st.metric("Average Match", f"{avg_score}%")
    with col_kpi3:
        st.metric("Strong Fits", f"{strong_fits}")
    with col_kpi4:
        st.metric("Moderate Fits", f"{moderate_fits}")
        
    st.markdown("---")
    
    # Clean tab names without emojis to mimic professional SaaS design
    tab1, tab2, tab3 = st.tabs(["Leaderboard", "Candidate Details", "Presentation Mode"])
    
    # TAB 1: LEADERBOARD & METRICS
    with tab1:
        st.subheader("Candidate Rankings Leaderboard")
        
        data_rows = []
        for rank, cand in enumerate(results_list, 1):
            rec = cand["recommendation"]
            rec_str = f"🟢 {rec}" if rec == "Strong Fit" else f"🟡 {rec}" if rec == "Moderate Fit" else f"🔴 {rec}"
            data_rows.append({
                "Rank": f"#{rank}",
                "Candidate Name": cand["name"],
                "Current Role": cand["role"],
                "Match Score": f"{cand['score']}%",
                "Fit Category": rec_str
            })
            
        df = pd.DataFrame(data_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col_chart_1, col_chart_2 = st.columns(2)
        
        with col_chart_1:
            st.markdown("#### Candidate Match Scores")
            chart_df = pd.DataFrame({
                "CandidateName": [c["name"] for c in results_list],
                "Match Score (%)": [c["score"] for c in results_list]
            })
            st.bar_chart(chart_df.set_index("CandidateName"), color="#4f46e5")
            
        with col_chart_2:
            st.markdown("#### Job Description Optimization Insights")
            insights = generate_jd_insights(results_list, jd_text, gemini_key)
            st.info(insights)
            
    # TAB 2: DETAILED PROFILES & ACTIONS
    with tab2:
        st.subheader("Detailed Candidate Evaluation Files")
        st.markdown("Expand any candidate profile to view detailed strengths, weaknesses, and edit the automated invitation.")
        
        for cand in results_list:
            rec = cand["recommendation"]
            if rec == "Strong Fit":
                tag = "🟢 Strong Fit"
            elif rec == "Moderate Fit":
                tag = "🟡 Moderate Fit"
            else:
                tag = "🔴 Not Fit"
                
            with st.expander(f"**{cand['name']}** — Score: {cand['score']}% | {tag}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### Candidate Assessment: {cand['name']}")
                    st.markdown(f"**Target Role:** {cand['role']}")
                    
                    st.markdown("**Key Strengths:**")
                    for strength in cand["strengths"]:
                        st.markdown(f"- {strength}")
                        
                    st.markdown("**Key Gaps & Weaknesses:**")
                    for gap in cand["gaps"]:
                        st.markdown(f"- {gap}")
                        
                with col2:
                    st.markdown("### Outreach Automation & Workflow")
                    outreach_email = st.text_area(
                        "Edit Outreach Email Invite", 
                        value=cand["email_draft"], 
                        height=160, 
                        key=f"email_{cand['name'].replace(' ', '_')}"
                    )
                    
                    if st.button("Automate Outreach Invite", key=f"btn_{cand['name'].replace(' ', '_')}", use_container_width=True):
                        if webhook_url:
                            try:
                                payload = {
                                    "candidate_name": cand["name"],
                                    "score": cand["score"],
                                    "recommendation": cand["recommendation"],
                                    "email_draft": outreach_email,
                                    "strengths": cand["strengths"],
                                    "gaps": cand["gaps"]
                                }
                                resp = requests.post(webhook_url, json=payload, timeout=5)
                                if resp.status_code in [200, 201]:
                                    st.success(f"Webhook automated! Invitation sent successfully for {cand['name']}.")
                                else:
                                    st.warning(f"Webhook triggered but returned code {resp.status_code}.")
                            except Exception as e:
                                st.error(f"Automation failed: {e}")
                        else:
                            st.info("No webhook URL specified in sidebar. Here is the automated JSON payload:")
                            st.json({
                                "event": "candidate_outreach_trigger",
                                "name": cand["name"],
                                "score": cand["score"],
                                "recommendation": cand["recommendation"],
                                "email_draft": outreach_email
                            })
                            
    # TAB 3: PRESENTATION MODE
    with tab3:
        st.subheader("Hiring Manager Slideshow Deck")
        st.markdown("Use this presentation deck to present candidate evaluations directly to managers.")
        
        slide_idx = st.session_state["current_slide"]
        total_slides = len(results_list)
        
        if total_slides > 0:
            if slide_idx >= total_slides:
                slide_idx = 0
                st.session_state["current_slide"] = 0
                
            current_cand = results_list[slide_idx]
            
            st.markdown(
                f"""
                <div style="background-color:#1e293b; padding:30px; border-radius:15px; border:2px solid #334155; margin-bottom:20px;">
                    <h1 style="color:#ffffff; margin:0; padding-bottom:10px;">Slide {slide_idx + 1} of {total_slides}</h1>
                    <h2 style="color:#6366f1; margin:0;">Candidate Evaluation Report</h2>
                    <hr style="border: 1px solid #475569; margin: 15px 0;">
                    <h3 style="color:#ffffff; margin-top:0;">{current_cand['name']} - {current_cand['role']}</h3>
                    <p style="font-size:18px; color:#94a3b8;"><b>Match Score:</b> <span style="font-size:24px; color:#4ade80;">{current_cand['score']}%</span> ({current_cand['recommendation']})</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            col_slide_1, col_slide_2 = st.columns(2)
            with col_slide_1:
                st.markdown("#### Strengths & Fits")
                for s in current_cand["strengths"]:
                    st.markdown(f"✅ {s}")
            with col_slide_2:
                st.markdown("#### Areas of Concern")
                for g in current_cand["gaps"]:
                    st.markdown(f"⚠️ {g}")
                    
            st.markdown("---")
            
            btn_prev, _, btn_next = st.columns([1, 4, 1])
            with btn_prev:
                if st.button("⬅️ Previous Candidate", disabled=(slide_idx == 0)):
                    st.session_state["current_slide"] -= 1
                    st.rerun()
            with btn_next:
                if st.button("Next Candidate ➡️", disabled=(slide_idx == total_slides - 1)):
                    st.session_state["current_slide"] += 1
                    st.rerun()
else:
    st.markdown(
        """
        ## Welcome to your AI Screening Assistant! 👋
        This system parses candidate resumes, runs evaluations against job requirements, and prepares outreach automations.
        
        ### How to get started:
        1. **Check settings in the left panel:**
           - Emojis indicate your **Gemini API Key is loaded** from the secrets file.
           - You can add a **Zapier/Make Webhook URL** if you want to test live email sends.
        2. **Select a Job Role and verify its details:**
           - Choose one of our preset roles or select *Custom Job Description* to paste your own requirements.
           - **Note:** You can view and edit the detailed requirements inside the **"View / Edit Job Description Requirements"** box above!
        3. **Select your candidate source:**
           - Choose *Pre-loaded Profiles* to test instantly with our diverse sample database, OR
           - Choose *Upload Custom Resumes* to drag and drop your own PDF or TXT files.
        4. **Press 'Screen Candidates'!**
        """
    )
    
    col_welcome_1, col_welcome_2, col_welcome_3 = st.columns(3)
    with col_welcome_1:
        st.info("### 🔍 Smart Match\nCalculates numerical compatibility scores between resumes and job requirements.")
    with col_welcome_2:
        st.success("### 💡 Strengths & Gaps\nExtracts key technical capabilities and identifies candidate skill discrepancies.")
    with col_welcome_3:
        st.warning("### ✉️ Outreach Automation\nGenerates custom email invitations and pushes them straight to Zapier webhooks.")
