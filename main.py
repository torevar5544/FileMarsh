#!/usr/bin/env python3
"""
File Organizer - Main Entry Point
A comprehensive desktop application for file organization and analysis.
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from file_organizer import FileOrganizerMainWindow

def setup_logging():
    """Setup application logging configuration."""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'file_organizer.log')),
            logging.StreamHandler()
        ]
    )

def main():
    """Main application entry point."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting File Organizer Application")
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("File Organizer")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("FileOrg")
    
    # Set application-wide font
    font = QFont("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10)
    app.setFont(font)
    
    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    
    try:
        # Create and show main window
        main_window = FileOrganizerMainWindow()
        main_window.show()
        
        # Start event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
