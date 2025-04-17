import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from .utils import parse_iso_datetime, calculate_session_duration

def plot_daily_productivity(sessions, days=7, output_file=None):
    
   
    daily_data = {}
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    
    current_date = start_date
    while current_date <= end_date:
        daily_data[current_date] = {"coding": timedelta(), "break": timedelta()}
        current_date += timedelta(days=1)
    
    
    for session in sessions:
        date = parse_iso_datetime(session["start_time"]).date()
        if date in daily_data:
            coding_duration, break_duration = calculate_session_duration(session)
            daily_data[date]["coding"] += coding_duration
            daily_data[date]["break"] += break_duration

    
    dates = sorted(daily_data.keys())
    coding_hours = [daily_data[date]["coding"].total_seconds() / 3600 for date in dates]
    break_hours = [daily_data[date]["break"].total_seconds() / 3600 for date in dates]


    plt.figure(figsize=(12, 6))
    plt.bar(dates, coding_hours, label='Coding Time', color='#2ecc71')
    plt.bar(dates, break_hours, bottom=coding_hours, label='Break Time', color='#e74c3c')

    plt.title(f'Daily Productivity (Last {days} Days)')
    plt.xlabel('Date')
    plt.ylabel('Hours')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
    plt.close()

def format_time(seconds):
   
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:  # Show seconds if it's the only non-zero value
        parts.append(f"{secs}s")
    return " ".join(parts)

def plot_pie_chart(sessions, days=7, output_file=None):
    
    total_coding = timedelta()
    total_break = timedelta()
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    for session in sessions:
        session_date = parse_iso_datetime(session["start_time"]).date()
        if start_date <= session_date <= end_date:
            coding_duration, break_duration = calculate_session_duration(session)
            total_coding += coding_duration
            total_break += break_duration

    # Get total seconds
    coding_seconds = total_coding.total_seconds()
    break_seconds = total_break.total_seconds()

   
    coding_label = f"Coding Time\n{format_time(coding_seconds)}"
    break_label = f"Break Time\n{format_time(break_seconds)}"

   
    plt.figure(figsize=(10, 8))
    plt.pie([coding_seconds, break_seconds],
            labels=[coding_label, break_label],
            colors=['#2ecc71', '#e74c3c'],
            autopct=lambda pct: f'{pct:.1f}%',
            startangle=90)
    plt.title(f'Time Distribution (Last {days} Days)')
    plt.axis('equal')

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
    plt.close()

def plot_weekly_heatmap(sessions, weeks=1, output_file=None):
   
    week_grid = np.zeros((7, 24 * weeks))
    
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=weeks)
    
    for session in sessions:
        start_time = parse_iso_datetime(session["start_time"])
        if start_time < start_date:
            continue
            
        end_time = parse_iso_datetime(session["end_time"]) if "end_time" in session else datetime.now()
        
        # Calculate week offset
        week_offset = (end_date.date() - start_time.date()).days // 7
        if week_offset >= weeks:
            continue
        
        day = start_time.weekday()
        
        hour_offset = week_offset * 24
        
        for hour in range(start_time.hour, min(end_time.hour + 1, 24)):
            week_grid[day, hour + hour_offset] = 1

    # Create heatmap
    plt.figure(figsize=(12, 6))
    plt.imshow(week_grid, cmap='YlOrRd', aspect='auto')
    
    # Customize the plot
    plt.colorbar(label='Activity')
    plt.title(f'Weekly Activity Heatmap (Last {weeks} Week{"s" if weeks > 1 else ""})')
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    
    
    x_ticks = []
    x_labels = []
    for week in range(weeks):
        for hour in range(0, 24, 3):  # Show every 3 hours
            x_ticks.append(week * 24 + hour)
            x_labels.append(f"{hour:02d}:00")
    plt.xticks(x_ticks, x_labels, rotation=45)
    
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    plt.yticks(range(7), days)

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
    plt.close() 