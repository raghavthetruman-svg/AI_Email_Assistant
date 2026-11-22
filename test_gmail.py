
from gmail_service import fetch_first_email

print("Connecting to Gmail...")

email = fetch_first_email()

if email:

    print("\nGMAIL CONNECTION SUCCESSFUL!")

    print("\nSender:", email["sender"])

    print("Subject:", email["subject"])

    print("Date:", email["date"])

    print("\nEmail Body:")
    print(email["body"])

else:

    print("No emails found in your inbox.")
