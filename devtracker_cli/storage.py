"""
Storage handling for DevTracker sessions.
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class Storage:
    def __init__(self):
        self.data_dir = Path.home() / ".devtracker"
        self.sessions_file = self.data_dir / "sessions.json"
        self.current_session_file = self.data_dir / "current_session.json"
        self._ensure_data_dir()
        self._ensure_files()

    def _ensure_data_dir(self):
        """Ensure the data directory exists."""
        self.data_dir.mkdir(exist_ok=True)

    def _ensure_files(self):
        """Ensure the data files exist with proper initial content."""
        if not self.sessions_file.exists():
            self.sessions_file.write_text('[]')
        if not self.current_session_file.exists():
            self.current_session_file.write_text('null')

    def load_sessions(self, start_date=None, end_date=None):
        """Load sessions with optional date filtering."""
        sessions = json.loads(self.sessions_file.read_text())
        
        if start_date or end_date:
            filtered_sessions = []
            for session in sessions:
                session_date = datetime.fromisoformat(session["start_time"]).date()
                if start_date and session_date < start_date:
                    continue
                if end_date and session_date > end_date:
                    continue
                filtered_sessions.append(session)
            return filtered_sessions
        
        return sessions

    def get_weekly_sessions(self, weeks=1):
        """Get sessions for the last N weeks."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(weeks=weeks)
        return self.load_sessions(start_date=start_date, end_date=end_date)

    def get_daily_sessions(self, days=1):
        """Get sessions for the last N days."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        return self.load_sessions(start_date=start_date, end_date=end_date)

    def save_session(self, session):
        """Save a session to the sessions file."""
        sessions = self.load_sessions()
        if session is None:
            self.current_session_file.write_text('null')
            return
        
        # If session doesn't have an ID, assign one
        if "id" not in session:
            session["id"] = str(len(sessions) + 1)
            sessions.append(session)
        else:
            # Update existing session
            for i, s in enumerate(sessions):
                if s["id"] == session["id"]:
                    sessions[i] = session
                    break
            else:
                # If session not found, add it
                sessions.append(session)
        
        self.sessions_file.write_text(json.dumps(sessions, indent=2))
        self.current_session_file.write_text(json.dumps(session, indent=2))

    def clear_all_sessions(self):
        """Clear all session data."""
        self.sessions_file.write_text('[]')
        self.current_session_file.write_text('null') 