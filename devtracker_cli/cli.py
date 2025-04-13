"""
Command-line interface for DevTracker.
"""
import click
from datetime import datetime
from .tracker import Tracker
from .storage import Storage
from .utils import format_duration, generate_summary

# Try to import visualization modules
try:
    from .visualization import plot_daily_productivity, plot_pie_chart, plot_weekly_heatmap
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

@click.group()
def cli():
    """DevTracker - Track your development time."""
    pass

@cli.command()
@click.argument('task', required=True)
def start(task):
    """Start a new development session with a task description."""
    tracker = Tracker()
    try:
        tracker.start_session(task)
        click.echo(f"Development session started for task: {task}")
    except RuntimeError as e:
        click.echo(f"Error: {str(e)}")
        click.echo("\nTo force start a new session, use:")
        click.echo("devtracker clear")
        click.echo("devtracker start \"your task\"")

@cli.command()
def clear():
    """Clear all session history and current session state."""
    storage = Storage()
    storage.clear_all_sessions()
    click.echo("All session history has been cleared. You can now start a new session.")

@cli.command()
def stop():
    """Stop the current development session."""
    tracker = Tracker()
    try:
        tracker.stop_session()
        click.echo("Development session stopped!")
    except RuntimeError as e:
        click.echo(f"Error: {str(e)}")

@cli.command(name='break')
@click.argument('reason', required=True)
def break_time(reason):
    """Start a break during the current session with a reason."""
    tracker = Tracker()
    try:
        tracker.start_break(reason)
        click.echo(f"Break started: {reason}")
    except RuntimeError as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
def resume():
    """Resume the current session after a break."""
    tracker = Tracker()
    try:
        tracker.end_break()
        click.echo("Break ended!")
    except RuntimeError as e:
        click.echo("No active break to resume from.")

@cli.command()
def status():
    """Show current session status."""
    tracker = Tracker()
    status = tracker.get_status()
    click.echo(status)

@cli.command()
def log():
    """Show today's session and break logs with summary."""
    storage = Storage()
    sessions = storage.load_sessions()
    today = datetime.now().date().isoformat()
    
    click.echo(f"\nToday's Log ({today}):")
    click.echo("=" * 50)
    
    today_sessions = [s for s in sessions if datetime.fromisoformat(s["start_time"]).date().isoformat() == today]
    summary = generate_summary(today_sessions)
    
    for session in today_sessions:
        task = session.get('task')
        if not task:  # Skip sessions without tasks
            continue
            
        click.echo(f"\nTask: {task}")
        start_time = datetime.fromisoformat(session['start_time'])
        click.echo(f"Start Time: {start_time.strftime('%H:%M:%S')}")
        
        if "end_time" in session:
            end_time = datetime.fromisoformat(session['end_time'])
            click.echo(f"End Time: {end_time.strftime('%H:%M:%S')}")
            duration = end_time - start_time
            click.echo(f"Duration: {format_duration(duration)}")
        else:
            click.echo("Status: In Progress")
            current_duration = datetime.now() - start_time
            click.echo(f"Current Duration: {format_duration(current_duration)}")
        
        if session.get("breaks"):
            click.echo("\nBreaks:")
            total_break_time = 0
            for break_ in session["breaks"]:
                reason = break_.get('reason')
                if not reason:  # Skip breaks without reasons
                    continue
                    
                break_start = datetime.fromisoformat(break_['start_time'])
                click.echo(f"\n- {reason}")
                click.echo(f"  Start: {break_start.strftime('%H:%M:%S')}")
                
                if 'end_time' in break_:
                    break_end = datetime.fromisoformat(break_['end_time'])
                    click.echo(f"  End: {break_end.strftime('%H:%M:%S')}")
                    break_duration = break_end - break_start
                    click.echo(f"  Duration: {format_duration(break_duration)}")
                    total_break_time += break_duration.total_seconds()
                else:
                    click.echo("  Status: In Progress")
                    current_break_duration = datetime.now() - break_start
                    click.echo(f"  Current Duration: {format_duration(current_break_duration)}")
                    total_break_time += current_break_duration.total_seconds()
            
            if total_break_time > 0:
                click.echo(f"\nTotal Break Time: {format_duration(total_break_time)}")
        
        click.echo("=" * 50)
    
    # Add summary section
    click.echo("\nToday's Summary:")
    click.echo("=" * 50)
    click.echo(f"Total Sessions: {summary['total_sessions']}")
    click.echo(f"Total Coding Time: {summary['total_duration']}")
    click.echo(f"Total Break Time: {summary['total_break_duration']}")
    click.echo(f"Total Breaks: {summary['total_breaks']}")
    click.echo(f"Efficiency: {summary['efficiency']}")
    click.echo("=" * 50)

@cli.command()
def summary():
    """Show today's coding vs break time summary."""
    storage = Storage()
    sessions = storage.load_sessions()
    today = datetime.now().date().isoformat()
    
    today_sessions = [s for s in sessions if datetime.fromisoformat(s["start_time"]).date().isoformat() == today]
    summary = generate_summary(today_sessions)
    
    click.echo(f"\nToday's Summary ({today}):")
    click.echo("=" * 50)
    click.echo(f"Total Sessions: {summary['total_sessions']}")
    click.echo(f"Total Coding Time: {summary['total_duration']}")
    click.echo(f"Total Break Time: {summary['total_break_duration']}")
    click.echo(f"Total Breaks: {summary['total_breaks']}")
    click.echo(f"Efficiency: {summary['efficiency']}")
    click.echo("=" * 50)

@cli.command(name='daily')
@click.option('--days', '-d', type=int, default=7, help='Number of days to show (default: 7)')
@click.option('--output', '-o', type=click.Path(), help='Save the chart to a file')
def daily_chart(days, output):
    """Show daily productivity chart for the last N days."""
    if not VISUALIZATION_AVAILABLE:
        click.echo("Error: Visualization features require matplotlib and numpy.")
        click.echo("Please install them with: pip install matplotlib numpy")
        return
    
    storage = Storage()
    sessions = storage.get_daily_sessions(days)
    plot_daily_productivity(sessions, days, output)

@cli.command(name='pie')
@click.option('--days', '-d', type=int, default=7, help='Number of days to show (default: 7)')
@click.option('--output', '-o', type=click.Path(), help='Save the chart to a file')
def time_distribution(days, output):
    """Show pie chart of coding vs break time for the last N days."""
    if not VISUALIZATION_AVAILABLE:
        click.echo("Error: Visualization features require matplotlib and numpy.")
        click.echo("Please install them with: pip install matplotlib numpy")
        return
    
    storage = Storage()
    sessions = storage.get_daily_sessions(days)
    plot_pie_chart(sessions, days, output)

@cli.command(name='heatmap')
@click.option('--weeks', '-w', type=int, default=1, help='Number of weeks to show (default: 1)')
@click.option('--output', '-o', type=click.Path(), help='Save the chart to a file')
def weekly_heatmap(weeks, output):
    """Show weekly activity heatmap for the last N weeks."""
    if not VISUALIZATION_AVAILABLE:
        click.echo("Error: Visualization features require matplotlib and numpy.")
        click.echo("Please install them with: pip install matplotlib numpy")
        return
    
    storage = Storage()
    sessions = storage.get_weekly_sessions(weeks)
    plot_weekly_heatmap(sessions, weeks, output)

if __name__ == "__main__":
    cli() 