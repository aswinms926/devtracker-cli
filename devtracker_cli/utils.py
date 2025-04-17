
from datetime import datetime, timedelta

def format_duration(duration):
    
    if isinstance(duration, timedelta):
        seconds = duration.total_seconds()
    else:
        seconds = duration
        
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if remaining_seconds > 0 or not parts:
        parts.append(f"{remaining_seconds}s")
    
    return " ".join(parts)

def parse_iso_datetime(iso_string):
    
    return datetime.fromisoformat(iso_string)

def calculate_session_duration(session):
    
    start_time = parse_iso_datetime(session["start_time"])
    end_time = parse_iso_datetime(session["end_time"]) if "end_time" in session else datetime.now()
    
    # Total session duration including breaks
    total_duration = end_time - start_time
    
    # Subtract break durations
    break_duration = timedelta()
    if "breaks" in session:
        for break_ in session["breaks"]:
            break_start = parse_iso_datetime(break_["start_time"])
            break_end = parse_iso_datetime(break_["end_time"]) if "end_time" in break_ else datetime.now()
            break_duration += break_end - break_start
    
    # Actual coding time = total time - break time
    coding_duration = total_duration - break_duration
    return coding_duration, break_duration

def calculate_break_duration(session):
     
    total_break_duration = 0
    for break_ in session.get("breaks", []):
        break_start = parse_iso_datetime(break_["start_time"])
        break_end = parse_iso_datetime(break_.get("end_time", datetime.now().isoformat()))
        total_break_duration += (break_end - break_start).total_seconds()
    return total_break_duration

def generate_summary(sessions):
    
    total_coding_duration = timedelta()
    total_break_duration = timedelta()
    total_breaks = 0
    
    for session in sessions:
        coding_duration, break_duration = calculate_session_duration(session)
        total_coding_duration += coding_duration
        total_break_duration += break_duration
        total_breaks += len(session.get("breaks", []))
    
     
    total_time = total_coding_duration + total_break_duration
    
    
    
    efficiency = (total_coding_duration.total_seconds() / total_time.total_seconds() * 100) if total_time.total_seconds() > 0 else 0
    
    return {
        "total_sessions": len(sessions),
        "total_duration": format_duration(total_coding_duration),
        "total_break_duration": format_duration(total_break_duration),
        "total_breaks": total_breaks,
        "efficiency": f"{efficiency:.1f}%"
    } 