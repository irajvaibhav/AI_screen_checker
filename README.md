# AI Resume Screening & Automation System

**Live Deployment URL:** [aiscreenchecker-55zqmtiijsz4hcjcgfqgp4.streamlit.app](https://aiscreenchecker-55zqmtiijsz4hcjcgfqgp4.streamlit.app/)

A premium, interactive recruiting dashboard built for **Interviewkit.AI** to automate candidate screening, scoring, and recruiter outreach. 

This application runs on a **hybrid processing model** (Live Gemini LLM Mode + Local Heuristic Matcher) ensuring that the system is fully functional for custom resume uploads out-of-the-box. The Gemini API Key is securely configured via Streamlit Secrets.

---

## 🚀 How to Run Locally

### 1. Prerequisites
Make sure you have Python 3.8 or higher installed on your computer.

### 2. Install Dependencies
Open your terminal (PowerShell, Command Prompt, or Git Bash), navigate to this project folder, and run:
```bash
pip install -r requirements.txt
```

### 3. Start the Dashboard
Run the Streamlit server:
```bash
streamlit run app.py
```
This will automatically open the application in your default web browser at `http://localhost:8501`.

---

## ⚙️ Configuration & Features

1. **Google Gemini API Key:**
   - Configured securely using Streamlit Secrets. Live AI mode runs automatically on the deployed link.
   - If the key is missing, the app gracefully falls back to a **Local Heuristic Keyword Parser** so it continues to screen custom files without crashing.
2. **Zapier / Make.com Webhook URL (Optional):**
   - Paste a webhook URL from Make.com or Zapier in the sidebar. Clicking **"Automate Outreach"** on any candidate card will trigger a real HTTP POST request with candidate data to run automated email campaigns.
3. **Candidate Presentation Mode:**
   - Navigate to the **Presentation Mode** tab to view candidate evaluations in a slide format, optimized for presenting shortlist profiles to hiring managers.

---

## ☁️ How to Deploy Online for Free

You can deploy this Python application live on **Streamlit Community Cloud** in under 3 minutes:

1. **Push your code to GitHub:**
   - Create a new repository on GitHub (e.g., `AI_screen_checker`).
   - Push files: `app.py`, `mock_data.py`, `requirements.txt`, `.python-version`, and `.gitignore`.
2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
   - Click **"New App"**, choose your repository, branch, and select `app.py` as the main file.
   - Click **"Deploy"**. Your live URL will be ready in seconds!
3. **API Key Setup:**
   - Go to the app settings in the Streamlit Cloud Dashboard, navigate to the **Secrets** tab, and enter:
     ```toml
     GEMINI_API_KEY = "your_actual_api_key"
     ```

---

## 💡 Product Thinking & Design Choices
*(You can submit this section in your application form)*

### Objective & System Design
I designed this system to act as a highly practical recruiter workflow tool, prioritizing **reliability**, **security**, and **seamless user experience (UX)**. 

To address the constraint of **"Do not over-engineer"**, I selected **Python + Streamlit**. This stack allows the application to handle multiple PDF parsing, sorting leaderboards, and data visualization in a single, robust codebase with zero backend latency or cold-start loading issues.

### Key Engineering Decisions
* **API Configuration:** The Gemini API key is handled securely using Streamlit Secrets, ensuring it is kept safe and private from public view on GitHub while running automatically in production.
* **Hybrid Core Parser:** If the API key is missing or encounters a rate limit, the system falls back to a regex-based keyword matching engine. This ensures the app is fully functional for *any* custom uploaded resume from the first click, avoiding frustrating error screens.
* **End-to-End Automation:** The webhook integration connects the AI screening results directly with corporate low-code tools (Zapier/Make.com) to automate the actual outreach email delivery, illustrating system thinking.
