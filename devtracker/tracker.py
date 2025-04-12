"""
Session tracking logic for DevTracker.
"""
from datetime import datetime, timedelta
from .storage import Storage

class Tracker:
    def __init__(self):
        self.storage = Storage()
        self.current_session = self.storage.get_current_session()
        self.current_break = None
        self._cleanup_stale_sessions()
        self._load_current_break()

    def _load_current_break(self):
        """Load the current break from the session if it exists."""
        if self.current_session and self.current_session.get("breaks"):
            last_break = self.current_session["breaks"][-1]
            if "end_time" not in last_break:
                self.current_break = last_break

    def _cleanup_stale_sessions(self):
        """Clean up any stale sessions that are more than 24 hours old."""
        if self.current_session:
            session_start = datetime.fromisoformat(self.current_session["start_time"])
            if datetime.now() - session_start > timedelta(hours=24):
                # Session is too old, clear it
                self.current_session = None
                self.storage.save_session(None)

    def start_session(self, task):
        """Start a new development session with a task description."""
        if self.current_session:
            # Check if the current session is actually active
            if "end_time" in self.current_session:
                # Session is already ended, clear it
                self.current_session = None
                self.storage.save_session(None)
            else:
                raise RuntimeError("A session is already in progress")
        
        self.current_session = {
            "start_time": datetime.now().isoformat(),
            "task": task,
            "breaks": []
        }
        self.storage.save_session(self.current_session)

    def stop_session(self):
        """Stop the current development session."""
        if not self.current_session:
            raise RuntimeError("No active session to stop")
        
        if self.current_break:
            self.end_break()
        
        self.current_session["end_time"] = datetime.now().isoformat()
        self.storage.save_session(self.current_session)
        self.current_session = None

    def start_break(self, reason):
        """Start a break during the current session with a reason."""
        if not self.current_session:
            raise RuntimeError("No active session")
        if self.current_break:
            raise RuntimeError("A break is already in progress")
        
        self.current_break = {
            "start_time": datetime.now().isoformat(),
            "reason": reason
        }
        # Update the current session with the new break
        self.current_session["breaks"].append(self.current_break)
        self.storage.save_session(self.current_session)

    def end_break(self):
        """End the current break."""
        if not self.current_break:
            raise RuntimeError("No active break")
        
        self.current_break["end_time"] = datetime.now().isoformat()
        # Update the break in the current session
        for break_ in self.current_session["breaks"]:
            if break_.get("start_time") == self.current_break["start_time"]:
                break_.update(self.current_break)
                break
        self.current_break = None
        self.storage.save_session(self.current_session)

    def get_status(self):
        """Get the current session status."""
        if not self.current_session:
            return "No active session"
        
        status = f"Session in progress - Task: {self.current_session.get('task', 'No task specified')}"
        if self.current_break:
            status += f"\nOn break: {self.current_break.get('reason', 'No reason specified')}"
        
        return status 