import json

DATA_FILE = "study_log.txt"

sessions = []

def classify_session(duration):

    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"

def add_session():

    print("\n Add a Study Session ")
    subject = input("Subject name: ").strip()
    topic = input("Topic covered: ").strip()
    date = input("Enter date Date(DD/MM/YYYY): ").strip()
    
    while True:
        
        try:
            duration = int(input("Enter duration in minutes: "))
            if duration > 0:
                break

                print("Duration must be a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)
    print("Study session added successfully. ")

def view_sessions():
    print("\n All Study Sessions ")
    if not sessions:
        print("No study sessions have been recorded. ")
        return
    print("-" * 80)
    print(
            f"{'Subject':<15}"
            f"{'Topic':<25}"
            f"{'Date':<15}"
            f"{'Duraton':<12}"
            f"{'Class'}"
        )
    print("-" * 80)
    for session in sessions:
        classification = classify_session(
            session["duration"]
        )
        print(
            f"{session['subject']:<15}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12}"
            f"{classification}"

        )
        print("-"* 80)

def search_by_subject(subject):
    results = []

    for session in sessions:
        if session["subject"].lower() == subject.lower():
            results.append(session)

    if not results:
        print(f"\nNo sessions found for subject: {subject}")
        return

    total_time = sum(
        session["duration"]
        for session in results
    )

    print(f"\n Sessions for {subject} ")

    print("-" * 80)

    print(
        f"{'Subject':<15}"
        f"{'Topic':<25}"
        f"{'Date':<15}"
        f"{'Duration':<12}"
        f"{'Class'}"
    )

    print("-" * 80)

    for session in results:

        classification = classify_session(
            session["duration"]
        )

        print(
            f"{session['subject']:<15}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12}"
            f"{classification}"
        )

    print("-" * 80)

    print(
        f"Total study time for {subject}: "
        f"{total_time} minutes"
    )

def study_statistics():
    print("\n Study Statistics ")

    if not sessions:
        print("No study sessions available for statistics. ")
        return

    total_minutes = sum(
        session["duration"]
        for session in sessions
    )

    total_hours = total_minutes / 60

    print(f"Total study time: {total_hours:.2f} hours")

    subject_totals = {}

    for session in sessions:

        subject = session["subject"]

        subject_totals[subject] = (
            subject_totals.get(subject, 0)
            + session["duration"]
        )

    print("\nStudy time per subject:")

    for subject, minutes in subject_totals.items():

        print(
            f"{subject}: "
            f"{minutes / 60:.2f} hours"
        )

    weakest_subject = min(
        subject_totals,
        key=subject_totals.get
    )

    print(
        f"\nSubject with least study time: "
        f"{weakest_subject} "
        f"({subject_totals[weakest_subject]} minutes)"
    )

    longest_session = max(
        sessions,
        key=lambda session: session["duration"]
    )

    print(
        f"\nLongest single session: "
        f"{longest_session['subject']} - "
        f"{longest_session['topic']} "
        f"({longest_session['duration']} minutes)"
    )

def save_sessions():
        try:
            with open("study_log.txt","w") as file:
                json.dump(sessions,file,indent= 4)
                print("Study sessions saved successfully. ")
        except OSError as error:
            print(f"Error saving sessions:{error}")

def load_sessions():
    global sessions

    try:
        with open("study_log.txt", "r") as file:
            sessions = json.load(file)

        print("Previous study sessions loaded.")

    except FileNotFoundError:
        sessions = []

        print(
            "No previous study log found. "
            "Starting with an empty list."
        )

    except (json.JSONDecodeError, OSError):
        sessions = []

        print(
            "Could not load the study log. "
            "Starting with an empty list."
        )

def display_menu():

    print("\n===== Smart Study Planner =====")
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save & exit")


def main():
    load_sessions()

    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions()
        elif choice == "3":
            subject = input("Enter subject to search for: ").strip()
            search_by_subject(subject)
        elif choice == "4":
            study_statistics()
        elif choice == "5":
            save_sessions()
            print("Goodbye! Keep up the good study habits.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()