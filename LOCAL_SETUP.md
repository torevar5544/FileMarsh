# File Organizer - Local Setup Guide

## System Requirements

### Python Version
- Python 3.8 or higher
- Recommended: Python 3.11

### Operating System Support
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 20.04+, Fedora 35+, or equivalent)

## Installation Instructions

### 1. Clone or Download the Project
```bash
git clone <your-repo-url>
cd file-organizer
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

#### Essential Dependency (Required)
```bash
pip install PyQt6>=6.4.0
```

#### Or install from the requirements file:
```bash
pip install -r pip_requirements.txt
```

#### Optional Dependencies (for enhanced features)
The application is designed to work with minimal dependencies using Python's standard library. These are optional:
```bash
# For enhanced file type detection
pip install python-magic>=0.4.27

# For advanced data analysis features  
pip install pandas>=1.5.0 numpy>=1.21.0
```

### 4. System-Specific Dependencies

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3-tk libmagic1
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install python3-tkinter file-libs
```

#### macOS
```bash
# Using Homebrew
brew install libmagic
```

#### Windows
- No additional system dependencies required
- PyQt6 includes all necessary components

### 5. Test Your Setup (Optional)
```bash
python test_local.py
```

### 6. Run the Application
```bash
python main.py
```

## Features
- Comprehensive file analysis and organization
- Multiple export formats (CSV, Excel, JSON)
- File statistics and visualization
- Duplicate file detection
- Cross-platform desktop GUI

## Troubleshooting

### Common Issues

#### Qt Platform Plugin Error (Linux)
If you see "qt.qpa.plugin: Could not load the Qt platform plugin":
```bash
sudo apt install libxcb-xinerama0 libxcb-cursor0
```

#### Magic Library Error
If you get errors related to python-magic:
```bash
# Linux
sudo apt install libmagic1
# macOS
brew install libmagic
# Windows - usually works without additional setup
```

#### Permission Errors
Make sure you have read/write permissions in the directories you want to analyze.

## Development Setup

### Additional Development Dependencies
```bash
pip install pytest>=7.0.0
pip install pytest-qt>=4.2.0
pip install black  # Code formatting
pip install flake8  # Linting
```

### Running Tests
```bash
pytest tests/
```

## File Structure
```
file-organizer/
├── main.py                 # Application entry point
├── file_organizer.py       # Main window and UI
├── file_analyzer.py        # File analysis logic
├── export_manager.py       # Export functionality
├── statistics_widget.py    # Statistics display
├── styles.py              # UI styling
├── utils.py               # Utility functions
└── logs/                  # Application logs
```

## Support
For issues or questions, please check the logs in the `logs/` directory for detailed error information.