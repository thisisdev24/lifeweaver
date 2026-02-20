from ics import Calendar, Event
from datetime import datetime, timedelta
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SANDBOX = os.path.join(ROOT, "sandbox")
os.makedirs(SANDBOX, exist_ok=True)


def create_calendar_draft(title="Quick sync", minutes=15):
    c = Calendar()
    e = Event()
    e.name = title
    e.begin = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    e.duration = {"minutes": minutes}
    c.events.add(e)
    path = os.path.join(SANDBOX, "draft_event.ics")
    with open(path, "w") as f:
        f.writelines(c)
    return path
