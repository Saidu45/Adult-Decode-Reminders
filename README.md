# Adult Decode Reminder System

## Overview

The **Adult Decode Reminder System** is a Python and Streamlit-based application designed to manage and track activities associated with the CHAMPS Adult Decode process.

Adult Decode sessions are scheduled **twice every month**:

* **Second Friday of the month**
* **Last Friday of the month**

The system automatically calculates activities before and after each decode session, provides a dashboard for monitoring them, and supports automated email reminders.

## Adult Decode Schedule

For every Adult Decode date, the system schedules the following activities:

| Timeline                | Activity                                           |
| ----------------------- | -------------------------------------------------- |
| 9 weeks before Decode   | Send request for Network Pathology Report          |
| 3 weeks before Decode   | Notify Data Team to generate case packets          |
| 2 weeks before Decode   | Send case packets to Subject Matter Experts (SMEs) |
| Monday of Decode week   | Send stakeholder memo for Dr. Ike's signature      |
| Tuesday before Decode   | SMEs submit Decode Reports                         |
| Wednesday before Decode | Rashid sends consensus document to panelists/SMEs  |
| Friday                  | Adult Decode                                       |
| Monday after Decode     | Send Service Completion Form to Dr. Bassey         |
| Monday after Decode     | Upload Decode Report to REDCap                     |
| Monday after Decode     | Send Decode results to the Surveillance Team       |

> **Note:** The Network Pathology Report request is scheduled 9 weeks before Decode because it is required 6 weeks before case-packet generation, while case-packet generation occurs 3 weeks before Decode.

## Features

* Automatically identifies the **second and last Friday** of every month.
* Generates Adult Decode schedules for the current and following year.
* Separates **Second Friday** and **Last Friday** Decode cycles.
* Tracks activities as **Pending, Completed, or Delayed**.
* Tracks whether reminders have been sent.
* Provides a Streamlit dashboard for monitoring Decode activities.
* Supports automated email reminders for activities due on a particular day.
* Displays upcoming Adult Decode sessions and the number of days remaining.
* Preserves existing task status when the tracker is regenerated.

## Project Structure

```text
Adult-Decode-Reminders/
│
├── adult_dashboard.py
├── adult_reminder.py
├── outlook_email_adult.py
├── ADULT Decode Reminder Generator.py
├── ADULT_Decode_Tracker.xlsx
├── requirements.txt
├── .gitignore
└── README.md
```

### `ADULT Decode Reminder Generator.py`

Generates the Adult Decode schedule and creates/updates:

```text
ADULT_Decode_Tracker.xlsx
```

It calculates both monthly Decode cycles and all activities associated with each Decode date.

### `ADULT_Decode_Tracker.xlsx`

Stores the generated Decode activities, including:

* Activity ID
* Activity Date
* Decode Date
* Year
* Decode Month
* Decode Cycle
* Assigned Person
* Activity
* Status
* Reminder Sent

### `adult_dashboard.py`

Provides the Streamlit web dashboard used to:

* View scheduled activities
* Monitor pending activities
* Identify overdue activities
* View completed activities
* Filter activities by Decode cycle, month, or responsible person
* Update activity status
* View upcoming Adult Decode dates

### `adult_reminder.py`

Checks the tracker for activities due on the current date.

When an activity is:

```text
DATE = Today
STATUS = Pending
REMINDER SENT = No
```

the system sends an email reminder to the responsible person and updates the tracker to show that the reminder was sent.

### `outlook_email_adult.py`

Contains the email functionality used by the reminder system to send automated notifications.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Adult-Decode-Reminders
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The `requirements.txt` should contain:

```text
streamlit
pandas
openpyxl
python-dotenv
```

## Generate the Adult Decode Tracker

Run:

```bash
python "ADULT Decode Reminder Generator.py"
```

This generates or updates:

```text
ADULT_Decode_Tracker.xlsx
```

## Run the Dashboard Locally

Start the Streamlit dashboard with:

```bash
streamlit run adult_dashboard.py
```

The dashboard will open in your web browser.

## Streamlit Deployment

When deploying through Streamlit Community Cloud, use:

```text
Branch: main
Main file path: adult_dashboard.py
```

Ensure that `ADULT_Decode_Tracker.xlsx` and `requirements.txt` are committed to the repository.

## Email Configuration

Email credentials should **never be stored directly in the Python scripts or committed to GitHub**.

Use environment variables or Streamlit Secrets for sensitive credentials.

For local development, credentials can be stored in a `.env` file.

The `.env` file should be excluded from Git using:

```text
.env
```

in `.gitignore`.

## Important

The system was developed to improve coordination and timely completion of activities surrounding the **CHAMPS Adult Decode process**.

It helps ensure that important activities involving the Data Team, Network Pathology Team, SMEs, panelists, Surveillance Team, and other responsible personnel are completed according to the Adult Decode schedule.
