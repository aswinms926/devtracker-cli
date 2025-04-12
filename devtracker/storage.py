"""
Storage handling for DevTracker sessions.
"""
import json
import os
from pathlib import Path

class Storage:
    def __init__(self):
        self.data_dir = Path.home() / ".devtracker"
        self.sessions_file = self.data_dir / "sessions.json"
        self.current_session_file = self.data_dir / "current_session.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Ensure the data directory exists."""
        self.data_dir.mkdir(exist_ok=True)
        if not self.sessions_file.exists():
            self.sessions_file.write_text("[]")
        if not self.current_session_file.exists():
            self.current_session_file.write_text("null")

    def save_session(self, session):
        """Save a session to the storage file."""
        if session is None:
            # Clear current session
            self._write_current_session(None)
            return

        if session.get("end_time"):
            # If session is complete, add it to sessions history
            sessions = self.load_sessions()
            sessions.append(session)
            self._write_sessions(sessions)
            # Clear current session
            self._write_current_session(None)
        else:
            # If session is in progress, save as current session
            self._write_current_session(session)

    def load_sessions(self):
        """Load all sessions from the storage file."""
        try:
            return json.loads(self.sessions_file.read_text())
        except json.JSONDecodeError:
            return []

    def get_current_session(self):
        """Get the current active session."""
        try:
            session = json.loads(self.current_session_file.read_text())
            return session if session != "null" else None
        except json.JSONDecodeError:
            return None

    def clear_all_sessions(self):
        """Clear all historical session data."""
        self._write_sessions([])
        self._write_current_session(None)

    def _write_sessions(self, sessions):
        """Write sessions to the storage file."""
        self.sessions_file.write_text(json.dumps(sessions, indent=2))

    def _write_current_session(self, session):
        """Write current session to file."""
        self.current_session_file.write_text(json.dumps(session, indent=2)) 