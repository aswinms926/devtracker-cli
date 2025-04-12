# DevTracker

A simple command-line tool to track your development time and breaks.

## Features

- Start and stop development sessions
- Track breaks during sessions
- View detailed session logs
- Get daily summaries of coding time vs break time
- Calculate efficiency metrics
- Clear session history when needed

## Installation

```bash
pip install devtracker
```

## Basic Commands

- `devtracker start "task description"` - Start a new development session
- `devtracker stop` - Stop the current session
- `devtracker break "reason"` - Start a break during the current session
- `devtracker resume` - Resume the current session after a break
- `devtracker status` - Show current session status
- `devtracker log` - Show today's session logs and summary
- `devtracker clear` - Clear all session history and current session state

## Example Workflow

```bash
# Start a new session
devtracker start "Implementing user authentication"

# Take a break
devtracker break "Lunch break"

# Resume work
devtracker resume

# Stop the session
devtracker stop

# View today's logs and summary
devtracker log
```

## Log Output

The `log` command shows detailed information about your sessions:

```
Today's Log (2024-04-12):
==================================================
Task: Implementing user authentication
Start Time: 10:00:00
End Time: 12:30:00
Duration: 2h 30m

Breaks:
- Lunch break
  Start: 12:00:00
  End: 13:00:00
  Duration: 1h 0m

Total Break Time: 1h 0m
==================================================

Today's Summary:
==================================================
Total Sessions: 1
Total Coding Time: 2h 30m
Total Break Time: 1h 0m
Total Breaks: 1
Efficiency: 71.4%
==================================================
```

## Troubleshooting

If you encounter the "session already in progress" error, use:
```bash
devtracker clear
```
Then start a new session with:
```bash
devtracker start "your task"
```

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Testing

Run the tests with:

```bash
pytest
```

## Data Storage

Session data is stored in your home directory:
- `~/.devtracker/sessions.json` - Historical session data
- `~/.devtracker/current_session.json` - Active session data

## License

MIT License 

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
    task: str
    start_time: datetime
    end_time: datetime = None
    breaks: list = None 

from setuptools import setup, find_packages

setup(
    name="devtracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "devtracker=devtracker.cli:cli",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A command-line tool to track your development time and breaks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/devtracker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 