"""
ADULT Decode Real Reminder System - AUTOMATIC MODE
Runs automatically without confirmation for scheduled tasks.
"""

import os
import pandas as pd
from outlook_email_adult import send_email

FILE = "ADULT_Decode_Tracker.xlsx"
SHEET = "Decode Tasks"


# Multiple recipients can be separated with semicolons.
EMAILS = {
    "Rashid": "rashid@emory.edu",
    "Drs. Andrew/Aziz": "amosera@emory.edu;saaziz2@emory.edu",
    "Seyi": "obalog2@emory.edu",
    "Pathology Team": "adaram2@emory.edu",
    "Drs. Bassey": "ibassey@emory.edu",
    "Data Team": "skamar3@emory.edu",
    # IMPORTANT: replace this with the Adult SME/panelist email addresses.
    "SMEs": "",
}


def get_person_name(assigned_person):
    if assigned_person == "SMEs":
        return "Adult Decode SMEs"
    if "/" in assigned_person:
        first_person = assigned_person.split("/")[0].strip()
        if first_person.startswith("Drs."):
            first_person = "Dr. " + first_person.replace("Drs.", "", 1).strip()
        return first_person
    if "Team" in assigned_person:
        return assigned_person
    return assigned_person


def create_email_body(row):
    person_name = get_person_name(row["ASSIGNED PERSON"])
    activity_date = row["DATE"].strftime("%d %B %Y")
    decode_date = row["DECODE DATE"].strftime("%d %B %Y")

    return f"""Dear {person_name},

This is a reminder from the CHAMPS ADULT Decode Management System.

Activity:
{row['ACTIVITY']}

Assigned Person:
{row['ASSIGNED PERSON']}

Scheduled Date:
{activity_date}

Adult Decode Date:
{decode_date} ({row['DECODE CYCLE']})

Current Status:
{row['STATUS']}

Please ensure this activity is completed according to the ADULT Decode schedule.

Best Regards,
CHAMPS Data Management Team
"""


def send_reminders():
    print("=" * 64)
    print("ADULT Decode Reminder System - AUTOMATIC MODE")
    print("=" * 64)

    if not os.path.exists(FILE):
        print(f"File not found: {FILE}")
        print(f"Current directory: {os.getcwd()}")
        return

    try:
        df = pd.read_excel(FILE, sheet_name=SHEET)
        print(f"Loaded {len(df)} activities from {FILE}")
    except Exception as exc:
        print(f"Error loading tracker: {exc}")
        return

    df["DATE"] = pd.to_datetime(df["DATE"]).dt.normalize()
    df["DECODE DATE"] = pd.to_datetime(df["DECODE DATE"]).dt.normalize()
    today = pd.Timestamp.today().normalize()

    due_today = df[
        (df["DATE"] == today)
        & (df["STATUS"] == "Pending")
        & (df["REMINDER SENT"] == "No")
    ]

    print(f"Today: {today.strftime('%Y-%m-%d')}")
    print(f"Activities due today: {len(due_today)}")

    if due_today.empty:
        print("No reminders need to be sent today.")
        return

    emails_sent = 0
    failed_emails = 0
    no_email_configured = 0

    for index, row in due_today.iterrows():
        assigned_person = row["ASSIGNED PERSON"]
        recipient = EMAILS.get(assigned_person, "").strip()

        print("-" * 64)
        print(f"Activity ID: {row.get('ID', 'Task')}")
        print(f"Task: {row['ACTIVITY']}")
        print(f"Assigned to: {assigned_person}")
        print(f"Decode date: {row['DECODE DATE'].strftime('%d %B %Y')}")

        if not recipient:
            print(f"No email configured for '{assigned_person}'")
            no_email_configured += 1
            failed_emails += 1
            continue

        subject = f"ADULT Decode Reminder: {row['ACTIVITY']}"
        body = create_email_body(row)

        try:
            print(f"Sending to: {recipient}")
            send_email(recipient, subject, body)
            df.loc[index, "REMINDER SENT"] = "Yes"
            emails_sent += 1
            print("Reminder sent successfully")
        except Exception as exc:
            failed_emails += 1
            print(f"Failed to send reminder: {exc}")

    if emails_sent > 0:
        try:
            df.to_excel(FILE, sheet_name=SHEET, index=False)
            print(f"Updated tracker: {emails_sent} reminder(s) marked as sent")
        except Exception as exc:
            print(f"Error saving tracker: {exc}")

    print("=" * 64)
    print("REMINDER CHECK COMPLETED")
    print(f"Emails sent: {emails_sent}")
    print(f"Failed: {failed_emails}")
    if no_email_configured:
        print(f"No email configured: {no_email_configured}")
    print("=" * 64)


if __name__ == "__main__":
    send_reminders()
