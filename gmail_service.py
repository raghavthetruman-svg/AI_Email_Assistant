
import os
import base64

from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import parseaddr

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ==================================================
# 1. GMAIL PERMISSIONS
# ==================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


# ==================================================
# 2. AUTHENTICATE WITH GOOGLE
# ==================================================

def authenticate_gmail():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES,
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES,
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=creds,
    )

    return service


# ==================================================
# 3. EXTRACT EMAIL BODY
# ==================================================

def extract_email_body(payload):

    mime_type = payload.get("mimeType", "")

    if mime_type == "text/plain":

        data = payload.get("body", {}).get("data")

        if data:
            decoded = base64.urlsafe_b64decode(data)

            return decoded.decode(
                "utf-8",
                errors="replace",
            )

    for part in payload.get("parts", []):

        body = extract_email_body(part)

        if body:
            return body

    return ""


# ==================================================
# 4. CONVERT GMAIL MESSAGE INTO EMAIL DATA
# ==================================================

def _headers_to_dict(payload):

    headers = payload.get("headers", [])

    wanted = {
        "from",
        "to",
        "subject",
        "date",
        "message-id",
        "references",
    }

    return {
        header["name"].lower(): header["value"]
        for header in headers
        if header.get("name", "").lower() in wanted
    }


def _build_email_record(message_id, email_data):

    payload = email_data.get("payload", {})

    headers = _headers_to_dict(payload)

    body = extract_email_body(payload)

    if not body:
        body = email_data.get("snippet", "")

    return {

        "id": message_id,

        "thread_id": email_data.get("threadId"),

        "sender": headers.get(
            "from",
            "Unknown",
        ),

        "recipient": headers.get(
            "to",
            "",
        ),

        "subject": headers.get(
            "subject",
            "No Subject",
        ),

        "date": headers.get(
            "date",
            "",
        ),

        "message_id_header": headers.get(
            "message-id",
            "",
        ),

        "references": headers.get(
            "references",
            "",
        ),

        "body": body,
    }


# ==================================================
# 5. FETCH THE FIRST EMAIL FROM INBOX
# ==================================================

def fetch_first_email():

    service = authenticate_gmail()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=1,
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return None

    message_id = messages[0]["id"]

    email_data = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full",
    ).execute()

    return _build_email_record(
        message_id,
        email_data,
    )


# ==================================================
# 6. CREATE A REPLY DRAFT IN GMAIL
# ==================================================

def create_reply_draft(email_data, reply_text):

    service = authenticate_gmail()

    message = EmailMessage()

    # Identify the sender's actual email address
    sender_email = parseaddr(
        email_data.get("sender", "")
    )[1]

    if not sender_email:

        raise ValueError(
            "Could not identify the sender's email address."
        )

    # Prepare the reply subject
    original_subject = email_data.get(
        "subject",
        "No Subject",
    )

    if original_subject.lower().startswith("re:"):
        reply_subject = original_subject

    else:
        reply_subject = "Re: " + original_subject

    message["To"] = sender_email

    message["Subject"] = reply_subject

    # Maintain the original email conversation thread
    message_id_header = email_data.get(
        "message_id_header",
        "",
    )

    if message_id_header:

        message["In-Reply-To"] = message_id_header

        references = email_data.get(
            "references",
            "",
        )

        if references:

            message["References"] = (
                references + " " + message_id_header
            )

        else:

            message["References"] = message_id_header

    message.set_content(reply_text)

    # Encode email for Gmail API
    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    draft_message = {
        "raw": encoded_message,
    }

    thread_id = email_data.get("thread_id")

    if thread_id:
        draft_message["threadId"] = thread_id

    # Save draft in Gmail
    draft = service.users().drafts().create(
        userId="me",
        body={
            "message": draft_message,
        },
    ).execute()

    return draft["id"]


# ==================================================
# 7. FETCH EMAILS FROM THE SELECTED DATE WINDOW
# ==================================================

def fetch_todays_emails():

    service = authenticate_gmail()

    # Get current local time
    now = datetime.now().astimezone()

    # Calculate the previous 24 hours
    start_time = now - timedelta(hours=24)

    # Convert dates into Gmail search format
    start_date = start_time.strftime("%Y/%m/%d")

    end_date = (
        now + timedelta(days=1)
    ).strftime("%Y/%m/%d")

    query = f"after:{start_date} before:{end_date}"

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        q=query,
        maxResults=100,
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:

        email_data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full",
        ).execute()

        email_record = _build_email_record(
            message["id"],
            email_data,
        )

        emails.append(email_record)

    return emails
