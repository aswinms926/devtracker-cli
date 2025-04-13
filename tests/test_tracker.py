"""
Tests for the tracker module.
"""
import pytest
from datetime import datetime
from devtracker_cli.tracker import Tracker

def test_start_session():
    tracker = Tracker()
    tracker.start_session()
    assert tracker.current_session is not None
    assert "start_time" in tracker.current_session
    assert "breaks" in tracker.current_session

def test_start_session_when_active():
    tracker = Tracker()
    tracker.start_session()
    with pytest.raises(RuntimeError):
        tracker.start_session()

def test_stop_session():
    tracker = Tracker()
    tracker.start_session()
    tracker.stop_session()
    assert tracker.current_session is None

def test_stop_session_when_inactive():
    tracker = Tracker()
    with pytest.raises(RuntimeError):
        tracker.stop_session()

def test_break_management():
    tracker = Tracker()
    tracker.start_session()
    tracker.start_break()
    assert tracker.current_break is not None
    tracker.end_break()
    assert tracker.current_break is None
    assert len(tracker.current_session["breaks"]) == 1 