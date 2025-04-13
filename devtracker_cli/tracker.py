"""
Core tracking functionality for DevTracker.
"""
from datetime import datetime
from .storage import Storage
from .utils import parse_iso_datetime

class Tracker:
    def __init__(self):
        self.storage = Storage()
        self.current_session = self._load_current_session()

    def _load_current_session(self):
        """Load the current session from storage."""
        sessions = self.storage.load_sessions()
        for session in sessions:
            if "end_time" not in session:
                return session
        return None

    def start_session(self, task):
        """Start a new development session."""
        if self.current_session:
            raise RuntimeError("A session is already in progress. Use 'devtracker stop' to end it first.")
        
        # Get the next available ID
        sessions = self.storage.load_sessions()
        next_id = str(len(sessions) + 1)
        
        session = {
            "id": next_id,
            "task": task,
            "start_time": datetime.now().isoformat(),
            "breaks": []
        }
        
        self.storage.save_session(session)
        self.current_session = session

    def stop_session(self):
        """Stop the current development session."""
        if not self.current_session:
            raise RuntimeError("No active session to stop.")
        
        self.current_session["end_time"] = datetime.now().isoformat()
        self.storage.save_session(self.current_session)
        self.current_session = None

    def start_break(self, reason):
        """Start a break during the current session."""
        if not self.current_session:
            raise RuntimeError("No active session. Start a session first.")
        
        if self._get_current_break():
            raise RuntimeError("A break is already in progress. Use 'devtracker resume' to end it first.")
        
        break_ = {
            "reason": reason,
            "start_time": datetime.now().isoformat()
        }
        
        if "breaks" not in self.current_session:
            self.current_session["breaks"] = []
        
        self.current_session["breaks"].append(break_)
        self.storage.save_session(self.current_session)

    def end_break(self):
        """End the current break."""
        if not self.current_session:
            raise RuntimeError("No active session.")
        
        current_break = self._get_current_break()
        if not current_break:
            raise RuntimeError("No active break to resume from.")
        
        current_break["end_time"] = datetime.now().isoformat()
        self.storage.save_session(self.current_session)

    def _get_current_break(self):
        """Get the current break if one exists."""
        if not self.current_session or "breaks" not in self.current_session:
            return None
        
        for break_ in self.current_session["breaks"]:
            if "end_time" not in break_:
                return break_
        return None

    def get_status(self):
        """Get the current session status."""
        if not self.current_session:
            return "No active session."
        
        status = f"Session in progress - Task: {self.current_session['task']}"
        
        current_break = self._get_current_break()
        if current_break:
            status += f"\nOn break: {current_break['reason']}"
        
        return status 