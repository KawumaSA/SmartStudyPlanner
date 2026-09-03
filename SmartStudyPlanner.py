# Smart Study Planner
# This program helps a student log and review study sessions.

import os

# Global list to store all sessions (each session is a dictionary)
sessions = []
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "study_log.txt")

def classify_session(duration):
    """Classifying a session based on duration in minutes."""
    if duration < 30:
        return "Short"
    elif 30<= duration <=90:
        return "Medium"
    else:
        return "Long"

def format_duration(duration):
    """Format a duration without a trailing .0 for whole numbers."""
    return f"{duration:g}"

def add_session():
    """Asking user for session details and add to the list."""
    print("\n--- Add a Study Session ---")
    subject = input("Subject name: ").strip()
    topic = input("Topic covered: ").strip()
    date = input("Date or day label: ").strip()

    # Loop until a valid duration is entered
    while True:
        try:
            duration = float(input("Duration (in minutes): "))
            if duration > 0:
                break  # valid positive number
            else:
                print("Duration must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Create a dictionary for the session
    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }
    sessions.append(session)
    print("Session added successfully!")

def view_sessions():
    """Display all sessions in a neatly formatted table."""
    print("\n--- All Study Sessions ---")
    if len(sessions) == 0:
        print("No sessions recorded yet.")
        return

    # Print header with fixed column widths
    header = f"{'Subject':<15} {'Topic':<20} {'Date':<12} {'Duration':>8}   Classification"
    print(header)
    print("-" * len(header))

    for session in sessions:
        classification = classify_session(session["duration"])
        # Use fixed widths for columns
        print(f"{session['subject']:<15} {session['topic']:<20} {session['date']:<12} "
              f"{session['duration']:>8} min   {classification}")

def search_by_subject(subject):
    """Show sessions for a particular subject (case-insensitive)."""
    subject = subject.strip()
    print(f"\n--- Sessions for '{subject}' ---")
    found = False
    total_time = 0  # minutes

    # Loop through sessions, compare subject lowercased
    for session in sessions:
        if session["subject"].lower() == subject.lower():
            found = True
            total_time += session["duration"]
            classification = classify_session(session["duration"])
            print(f"Topic: {session['topic']}, Date: {session['date']}, "
                  f"Duration: {session['duration']} min ({classification})")

    if not found:
        print(f"No sessions found for subject '{subject}'.")
    else:
        print(f"Total time spent on {subject}: {total_time} minutes")

def study_statistics():
    """Compute and display overall study statistics."""
    print("\n--- Study Statistics ---")
    if len(sessions) == 0:
        print("No data to show statistics.")
        return

    # Total minutes
    total_minutes = sum(s["duration"] for s in sessions)
    total_hours = total_minutes / 60

    # Dictionary: subject (lowercase) -> total minutes, also keep original name
    subject_times = {}
    subject_original = {}  # store first seen original case for display
    for s in sessions:
        subj_key = s["subject"].lower()
        if subj_key not in subject_times:
            subject_times[subj_key] = 0
            subject_original[subj_key] = s["subject"]
        subject_times[subj_key] += s["duration"]

    # Find subject with least total time (weakest area)
    weakest_key = min(subject_times, key=subject_times.get)
    weakest_subject = subject_original[weakest_key]
    weakest_minutes = subject_times[weakest_key]

    # Find longest single session
    longest_session = max(sessions, key=lambda s: s["duration"])

    # Print results
    print(f"Total study time: {total_hours:.2f} hours")
    print("\nHours per subject:")
    for key, mins in subject_times.items():
        print(f"  {subject_original[key]}: {mins/60:.2f} hours")
    print(f"\nWeakest area (least total time): {weakest_subject} ({weakest_minutes} minutes)")
    print(f"Longest session: {longest_session['topic']} on {longest_session['date']} "
          f"for {longest_session['duration']} minutes")

def save_sessions():
    """Save all sessions to a text file."""
    try:
        with open(LOG_FILE, "w") as file:
            for s in sessions:
                # Write each session as a line: subject|topic|date|duration
                line = f"{s['subject']}|{s['topic']}|{s['date']}|{s['duration']}\n"
                file.write(line)
        print(f"Sessions saved to {LOG_FILE}")
    except Exception as e:
        print(f"Error saving file: {e}")

def load_sessions():
    """Load sessions from file if it exists."""
    global sessions
    sessions = []  # start fresh
    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|")
                if len(parts) == 4:
                    subject, topic, date, duration_str = parts
                    try:
                        duration = float(duration_str)
                    except ValueError:
                        continue  # skip bad line
                    session = {
                        "subject": subject,
                        "topic": topic,
                        "date": date,
                        "duration": duration
                    }
                    sessions.append(session)
        print(f"Loaded {len(sessions)} sessions from file.")
    except FileNotFoundError:
        print(f"No existing study log found at {LOG_FILE}. Starting fresh.")
    except Exception as e:
        print(f"Error loading file: {e}")

def main():
    """Main menu loop."""
    # Load existing sessions when program starts
    load_sessions()

    while True:
        print("\n===== Smart Study Planner =====")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions()
        elif choice == "3":
            subject = input("Enter subject name to search: ")
            search_by_subject(subject)
        elif choice == "4":
            study_statistics()
        elif choice == "5":
            save_sessions()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

# Guard the entry point
if __name__ == "__main__":
    main()