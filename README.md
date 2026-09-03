# Smart Study Planner

A command-line Python app for recording and reviewing study sessions.

## Run

Requirements: Python 3.x. No external packages are needed.

From this folder, run:

```bash
python SmartStudyPlanner.py
```

The app loads existing sessions from `study_log.txt` when it starts. Enter a menu number and press **Enter**. Choose `2` to display all sessions, or choose `5` to save and exit.

## Menu

| Option | Action |
|---|---|
| 1 | Add a study session |
| 2 | View all sessions |
| 3 | Search by subject |
| 4 | View study statistics |
| 5 | Save and exit |

Each session contains a subject, topic, date or day label, and positive duration in minutes. Sessions are classified as **Short** (under 30 minutes), **Medium** (30-90 minutes), or **Long** (over 90 minutes).

## Storage

Sessions are stored in `study_log.txt`, one record per line using this format:

```text
subject|topic|date|duration
```

The file is overwritten when option `5` is selected. The current implementation expects four pipe-separated fields per valid record.
