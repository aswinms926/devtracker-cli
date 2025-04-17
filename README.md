# DevTracker

[![PyPI version](https://badge.fury.io/py/devtracker-cli.svg)](https://badge.fury.io/py/devtracker-cli)
[![Python Versions](https://img.shields.io/pypi/pyversions/devtracker-cli.svg)](https://pypi.org/project/devtracker-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## Development Time Tracking with Productivity Analytics

• Implemented a CLI-based time tracking system in Python using session management 
  and data persistence to track developers' coding time and breaks

• Built an extensible visualization module using matplotlib to generate productivity 
  insights through daily charts, time distribution, and weekly heatmaps

• Developed a robust storage system for managing session data with support for 
  historical analysis and real-time tracking

---

A powerful command-line tool for developers to track coding time, manage breaks, and visualize productivity patterns.

## Features

✨ **Core Features**
- Track development sessions with task descriptions
- Manage breaks during coding sessions
- View detailed session logs and summaries
- Calculate productivity metrics and efficiency

📊 **Visualization**
- Daily productivity charts
- Time distribution analysis
- Weekly activity heatmaps
- Customizable date ranges

🛠️ **Developer-Friendly**
- Simple command-line interface
- Persistent data storage
- Configurable settings
- Cross-platform support

## Installation

```bash
pip install devtracker-cli
```

## Quick Start

1. Start tracking your coding session:
```bash
devtracker start "Implementing user authentication"
```

2. Take a break:
```bash
devtracker break "Coffee break"
```

3. Resume coding:
```bash
devtracker resume
```

4. End your session:
```bash
devtracker stop
```

## Usage Guide

### Basic Commands

| Command | Description |
|---------|-------------|
| `devtracker start "task"` | Start a new development session |
| `devtracker stop` | Stop the current session |
| `devtracker break "reason"` | Start a break |
| `devtracker resume` | Resume from break |
| `devtracker status` | Show current status |
| `devtracker log` | View today's activity |
| `devtracker clear` | Clear all session data |

### Visualization Commands

| Command | Description | Options |
|---------|-------------|----------|
| `devtracker daily` | Show daily productivity | `-d DAYS`, `-o OUTPUT_FILE` |
| `devtracker pie` | Show time distribution | `-d DAYS`, `-o OUTPUT_FILE` |
| `devtracker heatmap` | Show activity heatmap | `-w WEEKS`, `-o OUTPUT_FILE` |

#### Options
- `-d, --days`: Number of days to analyze (default: 7)
- `-w, --weeks`: Number of weeks to analyze (default: 1)
- `-o, --output`: Save chart to file (e.g., `chart.png`)

### Example Outputs

#### Session Log
```
Today's Log (2024-04-12):
==================================================
Task: Implementing user authentication
Start Time: 10:00:00
End Time: 12:30:00
Duration: 2h 30m

Breaks:
- Coffee break
  Start: 11:00:00
  End: 11:15:00
  Duration: 15m

Total Break Time: 15m
==================================================

Today's Summary:
==================================================
Total Sessions: 1
Total Coding Time: 2h 15m
Total Break Time: 15m
Total Breaks: 1
Efficiency: 90.0%
==================================================
```

## Advanced Usage

### Time Range Analysis
```bash
# View last 14 days of productivity
devtracker daily -d 14

# Analyze last month's time distribution
devtracker pie -d 30

# View last 4 weeks of activity patterns
devtracker heatmap -w 4
```

### Saving Visualizations
```bash
# Save daily chart to file
devtracker daily -o productivity.png

# Export time distribution
devtracker pie -o distribution.png

# Save activity heatmap
devtracker heatmap -o heatmap.png
```

## Data Storage

DevTracker stores all session data locally in:
- Windows: `%USERPROFILE%\.devtracker\`
- Unix/Mac: `~/.devtracker/`

## Troubleshooting

### Common Issues

1. **"Session already in progress" error**
   ```bash
   devtracker clear
   devtracker start "new task"
   ```

2. **"No active break" when resuming**
   - Ensure you started a break using `devtracker break "reason"`
   - Check current status with `devtracker status`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Aswin M S - [GitHub](https://github.com/aswinms926)

## Acknowledgments

- Thanks to all future contributors , feel free to contribute . 
- Inspired by the need for better developer time tracking

