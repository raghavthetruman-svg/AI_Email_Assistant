
from gmail_service import fetch_todays_emails
from reader_agent import classify_email


print("\nConnecting to Gmail...")

# Step 1: Fetch emails received today
emails = fetch_todays_emails()

print(f"\nTotal emails received: {len(emails)}")

# Step 2: Check whether any emails were found
if not emails:
    print("\nNo emails found for the selected date.")
    
else:
    print("\nReader Agent is analysing emails...\n")

    results = []

    # Step 3: Classify each email individually
    for index, email in enumerate(emails, start=1):

        print(
            f"Processing email {index} of {len(emails)}: "
            f"{email['subject']}",
            flush=True
        )

        try:
            result = classify_email(email)
            results.append(result)

            print(
                f"Completed: {result['category']}",
                flush=True
            )

        except Exception as e:
            print(
                f"Error processing email {index}: {e}",
                flush=True
            )

    # Step 4: Display classification results
    print("\n" + "=" * 60)
    print("EMAIL CLASSIFICATION RESULTS")
    print("=" * 60)

    for result in results:

        print("\nSender:", result["sender"])
        print("Subject:", result["subject"])
        print("Category:", result["category"])
        print("Reason:", result["reason"])

        print("-" * 60)

    # Step 5: Separate emails into two categories
    action_required = [
        email for email in results
        if email["category"] == "Action Required"
    ]

    no_action = [
        email for email in results
        if email["category"] == "No Action Required"
    ]

    # Step 6: Display final summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    print("Total emails processed:", len(results))
    print("Action Required:", len(action_required))
    print("No Action Required:", len(no_action))

    print("\nReader Agent execution completed.")
