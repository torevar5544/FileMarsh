# File Organizer Desktop Application

## Overview

File Organizer is a comprehensive PyQt6-based desktop application designed for analyzing, organizing, and managing files across directory structures. The application provides detailed file analysis capabilities, statistical reporting, and intelligent export functionality to help users understand and organize their file systems efficiently.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **GUI Framework**: PyQt6 with widget-based architecture
- **Main Window Pattern**: Central QMainWindow with tabbed interface design
- **Widget Composition**: Modular widget classes (StatisticsWidget, custom components)
- **Styling System**: Centralized CSS-like styling through AppStyles class
- **Threading**: QThread implementation for non-blocking file operations

### Core Components
- **FileAnalyzer**: Core analysis engine that classifies files by type, MIME type, and extension
- **ExportManager**: Handles file organization and export operations with structure preservation options
- **StatisticsWidget**: Multi-tab statistical analysis interface with export capabilities
- **Utils Module**: Common utility functions for file size formatting and icon management

### Data Architecture
- **FileInfo Dataclass**: Structured file metadata storage (path, size, type, MIME type, extension)
- **AnalysisResult Dataclass**: Comprehensive analysis results with file categorization and error tracking
- **Type Classification System**: MIME type and extension-based file categorization into predefined categories (images, videos, audio, documents, archives, executables)

### Processing Architecture
- **Worker Thread Pattern**: Separate QThread workers for analysis and export operations
- **Signal-Slot Communication**: PyQt signal system for thread-safe UI updates
- **Progress Tracking**: Built-in progress reporting for long-running operations
- **Error Handling**: Comprehensive error collection and reporting system

### File Organization Strategy
- **Type-Based Classification**: Files categorized into logical groups (images, videos, audio, documents, archives, executables, unknown)
- **Structure Preservation**: Optional preservation of original directory hierarchy during export
- **Flexible Export Destinations**: User-configurable export paths with automatic directory creation

### User Interface Design
- **Multi-Tab Interface**: Separate views for overview, file types, and extensions
- **Real-Time Statistics**: Live updates during analysis operations
- **Export Integration**: Built-in export functionality with multiple format support
- **Responsive Layout**: Splitter-based layouts for flexible window management

## External Dependencies

### Core Framework
- **PyQt6**: Complete GUI framework providing widgets, threading, and signal systems
- **Python Standard Library**: 
  - `pathlib` for cross-platform path handling
  - `mimetypes` for MIME type detection
  - `logging` for application logging
  - `csv` and `json` for data export formats
  - `dataclasses` for structured data representation

### File System Operations
- **Built-in Modules**: Uses Python's standard `os`, `shutil`, and `pathlib` for file system operations
- **No External File System Dependencies**: Self-contained file analysis and organization

### Logging and Monitoring
- **Python Logging Module**: File and console logging with configurable levels
- **Log Directory Management**: Automatic log directory creation and management

### Platform Considerations
- **Cross-Platform Compatibility**: PyQt6 ensures compatibility across Windows, macOS, and Linux
- **High-DPI Support**: Built-in high-DPI scaling attributes for modern displays
- **Platform-Specific Fonts**: Conditional font selection (Segoe UI for Windows, Ubuntu for others)