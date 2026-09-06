"""
SMART STUDY PLANNER

A console-based Python program that allows a student to:
1. Add study sessions
2. View all sessions
3. Search sessions by subject
4. View study statistics
5. Save and exit

The program stores data in study_log.txt so that sessions
are available when the program is run again.
"""

import json
import os
from collections import defaultdict

FILE_NAME = "study_log.txt"


# ---------------------------------------------------------
# 1. CLASSIFY STUDY SESSION
# ---------------------------------------------------------

def classify_session(duration):
    """
    Classifies a study session according to its duration.

    Under 30 minutes  -> Short
    30 to 90 minutes  -> Medium
    Over 90 minutes   -> Long
    """

    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


# ---------------------------------------------------------
# 2. ADD STUDY SESSION
# ---------------------------------------------------------

def add_session(sessions):
    """
    Prompts the user for study session information,
    validates the duration and stores the session
    as a dictionary in the sessions list.
    """

    print("\n========== ADD STUDY SESSION ==========")

    # Get subject
    subject = input("Enter subject name: ").strip()

    while subject == "":
        print("Subject name cannot be empty.")
        subject = input("Enter subject name: ").strip()

    # Get topic
    topic = input("Enter topic covered: ").strip()

    while topic == "":
        print("Topic cannot be empty.")
        topic = input("Enter topic covered: ").strip()

    # Get date/day
    date = input("Enter date/day label: ").strip()

    while date == "":
        print("Date/day label cannot be empty.")
        date = input("Enter date/day label: ").strip()

    # Validate duration
    while True:
        try:
            duration = int(input("Enter duration in minutes: "))

            if duration <= 0:
                print("Duration must be a positive number.")
            else:
                break

        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Create session dictionary
    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    # Add dictionary to list
    sessions.append(session)

    print("\nStudy session added successfully!")


# ---------------------------------------------------------
# 3. VIEW ALL STUDY SESSIONS
# ---------------------------------------------------------

def view_sessions(sessions):
    """
    Displays all recorded study sessions in a table.
    The classification is automatically calculated.
    """

    print("\n================ ALL STUDY SESSIONS ================")

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    # Table headings
    print(
        f"{'No.':<5}"
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date/Day':<15}"
        f"{'Minutes':<10}"
        f"{'Class':<10}"
    )

    print("-" * 85)

    # Display every session
    for number, session in enumerate(sessions, start=1):

        classification = classify_session(
            session["duration"]
        )

        print(
            f"{number:<5}"
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<10}"
            f"{classification:<10}"
        )


# ---------------------------------------------------------
# 4. SEARCH BY SUBJECT
# ---------------------------------------------------------

def search_by_subject(sessions, subject):
    """
    Searches for study sessions belonging to a subject.

    The search is case-insensitive.
    For example:
        python
        Python
        PYTHON

    will all match Python.
    """

    search_subject = subject.strip().lower()

    if search_subject == "":
        print("Subject cannot be empty.")
        return

    # Find matching sessions
    matching_sessions = []

    for session in sessions:

        if session["subject"].strip().lower() == search_subject:
            matching_sessions.append(session)

    print("\n================ SEARCH RESULTS ================")

    # No sessions found
    if not matching_sessions:
        print("No sessions found for that subject.")
        return

    # Display matching sessions
    total_minutes = 0

    for number, session in enumerate(matching_sessions, start=1):

        classification = classify_session(
            session["duration"]
        )

        print(
            f"{number}. "
            f"Subject: {session['subject']} | "
            f"Topic: {session['topic']} | "
            f"Date: {session['date']} | "
            f"Duration: {session['duration']} minutes | "
            f"Class: {classification}"
        )

        total_minutes += session["duration"]

    # Convert minutes to hours
    total_hours = total_minutes / 60

    print(
        f"\nTotal time spent on "
        f"{matching_sessions[0]['subject']}: "
        f"{total_hours:.2f} hours"
    )


# ---------------------------------------------------------
# 5. STUDY STATISTICS
# ---------------------------------------------------------

def study_statistics(sessions):
    """
    Calculates and displays:
    - Total hours studied overall
    - Total hours per subject
    - Subject with the least study time
    - Longest study session
    """

    print("\n================ STUDY STATISTICS ================")

    if not sessions:
        print("No study sessions are available.")
        return

    # Calculate total minutes
    total_minutes = 0

    for session in sessions:
        total_minutes += session["duration"]

    total_hours = total_minutes / 60

    print(
        f"\nTotal hours studied overall: "
        f"{total_hours:.2f} hours"
    )

    # -------------------------------------------------
    # Calculate study time per subject
    # -------------------------------------------------

    subject_totals = defaultdict(int)

    for session in sessions:

        subject = session["subject"]

        subject_totals[subject] += session["duration"]

    print("\nTotal hours studied per subject:")

    for subject, minutes in subject_totals.items():

        hours = minutes / 60

        print(
            f"- {subject}: {hours:.2f} hours"
        )

    # -------------------------------------------------
    # Find subject with least study time
    # -------------------------------------------------

    weakest_subject = min(
        subject_totals,
        key=subject_totals.get
    )

    weakest_hours = (
        subject_totals[weakest_subject] / 60
    )

    print(
        f"\nSubject with least total study time "
        f"(weakest area): {weakest_subject}"
    )

    print(
        f"Time spent: {weakest_hours:.2f} hours"
    )

    # -------------------------------------------------
    # Find longest session
    # -------------------------------------------------

    longest_session = max(
        sessions,
        key=lambda session: session["duration"]
    )

    classification = classify_session(
        longest_session["duration"]
    )

    print("\nSingle longest session:")

    print(
        f"Subject: {longest_session['subject']}"
    )

    print(
        f"Topic: {longest_session['topic']}"
    )

    print(
        f"Date: {longest_session['date']}"
    )

    print(
        f"Duration: "
        f"{longest_session['duration']} minutes"
    )

    print(
        f"Classification: {classification}"
    )


# ---------------------------------------------------------
# 6. SAVE SESSIONS
# ---------------------------------------------------------

def save_sessions(sessions):
    """
    Saves all study sessions to study_log.txt.

    Each session is stored as a JSON object on its
    own line.
    """

    try:

        with open(
            FILE_NAME,
            "w",
            encoding="utf-8"
        ) as file:

            for session in sessions:

                file.write(
                    json.dumps(session) + "\n"
                )

        print(
            f"\nSessions successfully saved to "
            f"{FILE_NAME}"
        )

    except OSError as error:

        print(
            f"Error saving sessions: {error}"
        )


# ---------------------------------------------------------
# 7. LOAD SESSIONS
# ---------------------------------------------------------

def load_sessions():
    """
    Loads previously saved sessions from study_log.txt.

    If the file does not exist, an empty list is returned.
    This prevents the program from crashing on the first run.
    """

    sessions = []

    # Check whether the file exists
    if not os.path.exists(FILE_NAME):

        return sessions

    try:

        with open(
            FILE_NAME,
            "r",
            encoding="utf-8"
        ) as file:

            for line_number, line in enumerate(
                file,
                start=1
            ):

                line = line.strip()

                if line == "":
                    continue

                try:

                    session = json.loads(line)

                    # Validate loaded data
                    if (
                        isinstance(session, dict)
                        and "subject" in session
                        and "topic" in session
                        and "date" in session
                        and "duration" in session
                        and isinstance(
                            session["duration"],
                            int
                        )
                        and session["duration"] > 0
                    ):

                        sessions.append(session)

                    else:

                        print(
                            f"Invalid record on line "
                            f"{line_number}. Skipped."
                        )

                except json.JSONDecodeError:

                    print(
                        f"Could not read line "
                        f"{line_number}. Skipped."
                    )

    except OSError as error:

        print(
            f"Error loading sessions: {error}"
        )

    return sessions


# ---------------------------------------------------------
# 8. DISPLAY MENU
# ---------------------------------------------------------

def display_menu():
    """
    Displays the main program menu.
    """

    print("\n")
    print("=" * 50)
    print("             SMART STUDY PLANNER")
    print("=" * 50)

    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")

    print("=" * 50)


# ---------------------------------------------------------
# 9. MAIN FUNCTION
# ---------------------------------------------------------

def main():
    """
    Main function that controls the entire program.
    """

    # Load existing sessions when program starts
    sessions = load_sessions()

    if sessions:

        print(
            f"Loaded {len(sessions)} existing "
            f"study session(s)."
        )

    else:

        print(
            "No existing study sessions found."
        )

    # Keep displaying menu until user exits
    while True:

        display_menu()

        choice = input(
            "Enter your choice (1-5): "
        ).strip()

        # ---------------------------------------------
        # OPTION 1: ADD SESSION
        # ---------------------------------------------

        if choice == "1":

            add_session(sessions)

        # ---------------------------------------------
        # OPTION 2: VIEW SESSIONS
        # ---------------------------------------------

        elif choice == "2":

            view_sessions(sessions)

        # ---------------------------------------------
        # OPTION 3: SEARCH SUBJECT
        # ---------------------------------------------

        elif choice == "3":

            subject = input(
                "Enter subject to search: "
            )

            search_by_subject(
                sessions,
                subject
            )

        # ---------------------------------------------
        # OPTION 4: STATISTICS
        # ---------------------------------------------

        elif choice == "4":

            study_statistics(sessions)

        # ---------------------------------------------
        # OPTION 5: SAVE AND EXIT
        # ---------------------------------------------

        elif choice == "5":

            save_sessions(sessions)

            print(
                "Thank you for using "
                "Smart Study Planner!"
            )

            break

        # ---------------------------------------------
        # INVALID OPTION
        # ---------------------------------------------

        else:

            print(
                "\nInvalid menu choice."
                " Please select a number from 1 to 5."
            )


# ---------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
