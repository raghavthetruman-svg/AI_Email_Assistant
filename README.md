# AI Email Assistant — Multi-Agent Email Automation

## Project Overview

The AI Email Assistant is a Python-based application that uses Large Language Models (LLMs) and specialised AI agents to automate email analysis and reply preparation.

The application integrates with Gmail to retrieve emails, identify messages that require attention, and generate professional reply drafts.

It uses two specialised agents:

- **Reader Agent:** Analyses incoming emails and determines whether an action or response is required.
- **Writer Agent:** Generates professional email replies based on the content and context of the original email.

The application is built using Python and Streamlit, with Groq providing access to the LLM and the Gmail API handling email retrieval and draft creation.

**Important:** The application creates email drafts for human review. It does not automatically send emails.

---

## Key Features

### 1. Manual Email Reply Generation

- Accepts email content through a text input.
- Uses the Writer Agent to understand the email.
- Generates a relevant and professional reply.
- Allows the user to review the generated response.

### 2. Gmail Integration

- Connects to Gmail using Google OAuth authentication.
- Retrieves the first email from the inbox.
- Generates a contextual reply.
- Saves the response as a Gmail draft.

### 3. Reader Agent — Email Classification

- Retrieves inbox emails within the configured Gmail date-search window.
- Analyses the sender, subject, date, and email body.
- Classifies each email into one of two categories:

| Category | Description |
|---|---|
| Action Required | Emails requiring a response, review, approval, information, or another action |
| No Action Required | Newsletters, general announcements, informational notifications, and routine updates |

- Provides a reason for each classification.

### 4. Multi-Agent Workflow — Reader + Writer

- Passes retrieved emails to the Reader Agent.
- Identifies emails classified as Action Required.
- Passes only those emails to the Writer Agent.
- Generates contextual replies.
- Saves generated replies as Gmail drafts.
- Displays classification results and generated drafts in the application.

---

## System Architecture

```text
                 GMAIL INBOX
                      |
                      v
              GMAIL INTEGRATION
                      |
                      v
                 READER AGENT
                      |
              Email Classification
                      |
             +--------+--------+
             |                 |
             v                 v
       ACTION REQUIRED    NO ACTION REQUIRED
             |                 |
             v                 v
        WRITER AGENT          SKIP
             |
             v
       REPLY GENERATION
             |
             v
        GMAIL DRAFTS
             |
             v
       HUMAN REVIEW
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | User interface |
| Groq API | LLM inference |
| OpenAI Python SDK | Communication with Groq's OpenAI-compatible API |
| Gmail API | Email retrieval and draft creation |
| Google OAuth 2.0 | Secure Gmail authentication |
| python-dotenv | Environment variable management |

---

## Project Structure

```text
AI_Email_Assistant/
│
├── app.py
│   Main Streamlit application and Writer Agent
│
├── gmail_service.py
│   Gmail authentication, email retrieval and draft creation
│
├── reader_agent.py
│   Email classification logic
│
├── test_reader.py
│   Standalone test for the Reader Agent
│
├── .env
│   Groq API key (not committed to GitHub)
│
├── credentials.json
│   Google OAuth credentials (not committed to GitHub)
│
├── token.json
│   Gmail authentication token (not committed to GitHub)
│
├── .gitignore
│   Excludes sensitive files and local environment files
│
└── .venv/
    Python virtual environment (not committed to GitHub)
```

---

## Installation and Setup

### Prerequisites

- Python installed
- Git installed
- VS Code or another Python development environment
- A Groq API key
- A Google Cloud project with the Gmail API enabled

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Email_Assistant
```

### Step 2: Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install streamlit openai python-dotenv
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 4: Configure environment variables

Create a `.env` file in the project root folder:

```text
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Use your own Groq API key. Do not commit this file to GitHub.

### Step 5: Configure Gmail API

1. Create a project in Google Cloud Console.
2. Enable the Gmail API.
3. Configure the OAuth consent screen.
4. Create an OAuth client ID for a Desktop application.
5. Download the OAuth credentials.
6. Place the downloaded file in the project root folder and name it `credentials.json`.
7. On the first Gmail connection, complete the Google authorisation process.

The application creates `token.json` after successful authentication.

### Step 6: Run the application

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

---

## Application Interface

The application contains three main tabs:

1. **Manual Email:** Generate replies from pasted email content.
2. **Gmail Integration:** Retrieve an inbox email and save a generated reply as a Gmail draft.
3. **Reader + Writer Agents:** Classify inbox emails and generate drafts for emails requiring action.

---

## Security and Limitations

- API keys and OAuth credentials are stored locally and excluded from version control.
- Email content is treated as untrusted input by the agents.
- The application creates drafts rather than automatically sending emails.
- The current Gmail retrieval function processes up to 100 messages per request.
- Gmail date-search operators use date boundaries, so the configured search window is approximate rather than an exact rolling 24-hour filter.
- The Reader Agent classifies emails individually, making processing time dependent on the number of emails and API response times.
- Generated replies should be reviewed before sending.

---

## Future Enhancements

Potential improvements include:

- Improved date and timezone filtering.
- Gmail pagination for larger inboxes.
- Better handling of duplicate and failed drafts.
- User-editable replies before saving drafts.
- Support for additional email categories and prioritisation.
- More advanced multi-agent orchestration and workflow monitoring.

---

## Project Objective

This project demonstrates how specialised AI agents can collaborate to automate a practical business workflow.

By separating email understanding from email response generation, the application demonstrates a simple multi-agent architecture in which individual agents perform specialised tasks and work together through a coordinated Python application.
