#!/usr/bin/env python3
"""
Simple test script to verify File Organizer can run locally.
Run this script to test if all dependencies are properly installed.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing File Organizer dependencies...")
    
    try:
        # Test PyQt6 import
        print("✓ Testing PyQt6...", end=" ")
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        print("OK")
        
        # Test standard library imports
        print("✓ Testing Python standard library...", end=" ")
        import pathlib
        import mimetypes
        import logging
        import csv
        import json
        import dataclasses
        import shutil
        print("OK")
        
        # Test application modules
        print("✓ Testing application modules...", end=" ")
        from file_organizer import FileOrganizerMainWindow
        from file_analyzer import FileAnalyzer
        from export_manager import ExportManager
        print("OK")
        
        print("\n✅ All dependencies are available!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\nPlease install missing dependencies:")
        print("pip install PyQt6")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def test_app_creation():
    """Test if the application can be created without errors."""
    try:
        print("✓ Testing application creation...", end=" ")
        
        # Import modules
        from PyQt6.QtWidgets import QApplication
        from file_organizer import FileOrganizerMainWindow
        
        # Create QApplication instance
        app = QApplication([])
        
        # Try to create main window
        main_window = FileOrganizerMainWindow()
        
        print("OK")
        print("✅ Application can be created successfully!")
        
        # Clean up
        app.quit()
        return True
        
    except Exception as e:
        print(f"\n❌ Application creation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("File Organizer - Local Setup Test")
    print("=" * 40)
    
    if not test_imports():
        sys.exit(1)
    
    if not test_app_creation():
        sys.exit(1)
    
    print("\n🎉 All tests passed! You can run the application with:")
    print("python main.py")

if __name__ == "__main__":
    main()