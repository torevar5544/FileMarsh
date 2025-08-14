"""
File Organizer - Main Window Implementation
Comprehensive desktop application for file organization and analysis.
"""

import os
import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QGroupBox, QPushButton, QLabel, QLineEdit, QFileDialog,
    QTreeWidget, QTreeWidgetItem, QProgressBar, QStatusBar,
    QMessageBox, QSplitter, QTextEdit, QTableWidget, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon

from file_analyzer import FileAnalyzer, AnalysisWorker
from statistics_widget import StatisticsWidget
from export_manager import ExportManager, ExportWorker
from styles import AppStyles
from utils import format_file_size, get_file_icon

logger = logging.getLogger(__name__)

class FileOrganizerMainWindow(QMainWindow):
    """Main application window for the File Organizer."""
    
    def __init__(self):
        super().__init__()
        self.file_analyzer = FileAnalyzer()
        self.export_manager = ExportManager()
        self.current_analysis = None
        self.analysis_worker = None
        self.export_worker = None
        
        self.init_ui()
        self.apply_styles()
        
        logger.info("File Organizer Main Window initialized")
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("File Organizer - Comprehensive File Analysis & Organization")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create toolbar section
        toolbar_widget = self.create_toolbar()
        main_layout.addWidget(toolbar_widget)
        
        # Create main content area with splitter
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # Left panel - Folder selection and file tree
        left_panel = self.create_left_panel()
        content_splitter.addWidget(left_panel)
        
        # Right panel - Tabbed interface for statistics and export
        right_panel = self.create_right_panel()
        content_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        content_splitter.setSizes([500, 900])
        
        # Create status bar
        self.create_status_bar()
        
    def create_toolbar(self):
        """Create the main toolbar."""
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        
        # Folder selection group
        folder_group = QGroupBox("Folder Selection")
        folder_layout = QHBoxLayout(folder_group)
        
        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setPlaceholderText("Select a folder to analyze...")
        self.folder_path_edit.setReadOnly(True)
        folder_layout.addWidget(self.folder_path_edit)
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.browse_button)
        
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.start_analysis)
        self.analyze_button.setEnabled(False)
        folder_layout.addWidget(self.analyze_button)
        
        toolbar_layout.addWidget(folder_group)
        
        # Progress section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        progress_layout.addWidget(self.progress_label)
        
        toolbar_layout.addWidget(progress_group)
        
        return toolbar_widget
    
    def create_left_panel(self):
        """Create the left panel with file tree."""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # File tree group
        tree_group = QGroupBox("File Structure")
        tree_layout = QVBoxLayout(tree_group)
        
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["Name", "Type", "Size", "Path"])
        self.file_tree.setAlternatingRowColors(True)
        tree_layout.addWidget(self.file_tree)
        
        left_layout.addWidget(tree_group)
        
        # Log output
        log_group = QGroupBox("Operation Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        left_layout.addWidget(log_group)
        
        return left_widget
    
    def create_right_panel(self):
        """Create the right panel with tabbed interface."""
        self.tab_widget = QTabWidget()
        
        # Statistics tab
        self.statistics_widget = StatisticsWidget()
        self.tab_widget.addTab(self.statistics_widget, "Statistics")
        
        # Export tab
        export_widget = self.create_export_tab()
        self.tab_widget.addTab(export_widget, "Export")
        
        return self.tab_widget
    
    def create_export_tab(self):
        """Create the export tab."""
        export_widget = QWidget()
        export_layout = QVBoxLayout(export_widget)
        
        # Export settings group
        settings_group = QGroupBox("Export Settings")
        settings_layout = QVBoxLayout(settings_group)
        
        # Export destination
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Export Destination:"))
        
        self.export_path_edit = QLineEdit()
        self.export_path_edit.setPlaceholderText("Select export destination...")
        self.export_path_edit.setText(os.path.join(os.getcwd(), "exported_files"))
        dest_layout.addWidget(self.export_path_edit)
        
        self.export_browse_button = QPushButton("Browse")
        self.export_browse_button.clicked.connect(self.browse_export_destination)
        dest_layout.addWidget(self.export_browse_button)
        
        settings_layout.addLayout(dest_layout)
        
        # Export options
        options_layout = QHBoxLayout()
        options_layout.addWidget(QLabel("Operation:"))
        
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Copy Files", "Move Files"])
        options_layout.addWidget(self.operation_combo)
        
        self.preserve_structure_button = QPushButton("Preserve Folder Structure: ON")
        self.preserve_structure_button.setCheckable(True)
        self.preserve_structure_button.setChecked(True)
        self.preserve_structure_button.clicked.connect(self.toggle_preserve_structure)
        options_layout.addWidget(self.preserve_structure_button)
        
        settings_layout.addLayout(options_layout)
        
        # Export buttons
        button_layout = QHBoxLayout()
        
        self.export_all_button = QPushButton("Export All Files")
        self.export_all_button.clicked.connect(self.export_all_files)
        self.export_all_button.setEnabled(False)
        button_layout.addWidget(self.export_all_button)
        
        self.export_selected_button = QPushButton("Export by Type")
        self.export_selected_button.clicked.connect(self.export_by_type)
        self.export_selected_button.setEnabled(False)
        button_layout.addWidget(self.export_selected_button)
        
        settings_layout.addLayout(button_layout)
        
        export_layout.addWidget(settings_group)
        
        # Export progress
        progress_group = QGroupBox("Export Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.export_progress_bar = QProgressBar()
        self.export_progress_bar.setVisible(False)
        progress_layout.addWidget(self.export_progress_bar)
        
        self.export_progress_label = QLabel("")
        self.export_progress_label.setVisible(False)
        progress_layout.addWidget(self.export_progress_label)
        
        export_layout.addWidget(progress_group)
        export_layout.addStretch()
        
        return export_widget
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add permanent widgets to status bar
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        self.file_count_label = QLabel("Files: 0")
        self.status_bar.addPermanentWidget(self.file_count_label)
        
        self.total_size_label = QLabel("Total Size: 0 B")
        self.status_bar.addPermanentWidget(self.total_size_label)
    
    def apply_styles(self):
        """Apply application styles."""
        self.setStyleSheet(AppStyles.get_main_style())
    
    def browse_folder(self):
        """Open folder browser dialog."""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to Analyze",
            os.path.expanduser("~")
        )
        
        if folder_path:
            self.folder_path_edit.setText(folder_path)
            self.analyze_button.setEnabled(True)
            self.log_message(f"Selected folder: {folder_path}")
    
    def browse_export_destination(self):
        """Open export destination browser dialog."""
        export_path = QFileDialog.getExistingDirectory(
            self,
            "Select Export Destination",
            os.path.dirname(self.export_path_edit.text())
        )
        
        if export_path:
            self.export_path_edit.setText(export_path)
            self.log_message(f"Export destination: {export_path}")
    
    def toggle_preserve_structure(self):
        """Toggle preserve folder structure option."""
        if self.preserve_structure_button.isChecked():
            self.preserve_structure_button.setText("Preserve Folder Structure: ON")
        else:
            self.preserve_structure_button.setText("Preserve Folder Structure: OFF")
    
    def start_analysis(self):
        """Start folder analysis in background thread."""
        folder_path = self.folder_path_edit.text()
        if not folder_path or not os.path.exists(folder_path):
            QMessageBox.warning(self, "Warning", "Please select a valid folder.")
            return
        
        # Disable UI elements during analysis
        self.analyze_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.export_all_button.setEnabled(False)
        self.export_selected_button.setEnabled(False)
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_label.setText("Analyzing files...")
        
        # Clear previous results
        self.file_tree.clear()
        self.statistics_widget.clear_data()
        
        # Start analysis worker
        self.analysis_worker = AnalysisWorker(folder_path, self.file_analyzer)
        self.analysis_worker.progress.connect(self.update_analysis_progress)
        self.analysis_worker.finished.connect(self.analysis_finished)
        self.analysis_worker.error.connect(self.analysis_error)
        self.analysis_worker.start()
        
        self.log_message(f"Starting analysis of: {folder_path}")
    
    def update_analysis_progress(self, message, current, total):
        """Update analysis progress."""
        self.progress_label.setText(message)
        if total > 0:
            self.progress_bar.setRange(0, total)
            self.progress_bar.setValue(current)
        
        self.status_label.setText(message)
    
    def analysis_finished(self, analysis_result):
        """Handle analysis completion."""
        self.current_analysis = analysis_result
        
        # Hide progress
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        
        # Re-enable UI elements
        self.analyze_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.export_all_button.setEnabled(True)
        self.export_selected_button.setEnabled(True)
        
        # Update file tree
        self.populate_file_tree(analysis_result)
        
        # Update statistics
        self.statistics_widget.update_statistics(analysis_result)
        
        # Update status bar
        total_files = sum(len(files) for files in analysis_result.files_by_type.values())
        total_size = analysis_result.total_size
        
        self.file_count_label.setText(f"Files: {total_files:,}")
        self.total_size_label.setText(f"Total Size: {format_file_size(total_size)}")
        self.status_label.setText("Analysis complete")
        
        self.log_message(f"Analysis complete. Found {total_files:,} files ({format_file_size(total_size)})")
    
    def analysis_error(self, error_message):
        """Handle analysis error."""
        # Hide progress
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        
        # Re-enable UI elements
        self.analyze_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        
        # Show error message
        QMessageBox.critical(self, "Analysis Error", f"Analysis failed:\n{error_message}")
        self.log_message(f"Analysis error: {error_message}")
        self.status_label.setText("Analysis failed")
    
    def populate_file_tree(self, analysis_result):
        """Populate the file tree with analysis results."""
        self.file_tree.clear()
        
        # Create type-based root nodes
        type_nodes = {}
        for file_type in analysis_result.files_by_type:
            type_node = QTreeWidgetItem(self.file_tree)
            type_node.setText(0, file_type.title())
            type_node.setText(1, "Folder")
            type_node.setText(2, f"{len(analysis_result.files_by_type[file_type])} files")
            type_nodes[file_type] = type_node
        
        # Add files to type nodes
        for file_type, files in analysis_result.files_by_type.items():
            type_node = type_nodes[file_type]
            
            for file_info in files[:100]:  # Limit display for performance
                file_item = QTreeWidgetItem(type_node)
                file_item.setText(0, file_info.name)
                file_item.setText(1, file_info.type)
                file_item.setText(2, format_file_size(file_info.size))
                file_item.setText(3, str(file_info.path))
        
        # Expand type nodes
        self.file_tree.expandAll()
        
        # Resize columns
        for i in range(4):
            self.file_tree.resizeColumnToContents(i)
    
    def export_all_files(self):
        """Export all analyzed files."""
        if not self.current_analysis:
            QMessageBox.warning(self, "Warning", "Please analyze a folder first.")
            return
        
        self.start_export(export_all=True)
    
    def export_by_type(self):
        """Export files by selected types."""
        if not self.current_analysis:
            QMessageBox.warning(self, "Warning", "Please analyze a folder first.")
            return
        
        # For now, export all types - could add type selection dialog
        self.start_export(export_all=True)
    
    def start_export(self, export_all=True, selected_types=None):
        """Start file export operation."""
        export_path = self.export_path_edit.text()
        if not export_path:
            QMessageBox.warning(self, "Warning", "Please select an export destination.")
            return
        
        # Get export settings
        move_files = self.operation_combo.currentText() == "Move Files"
        preserve_structure = self.preserve_structure_button.isChecked()
        
        # Disable UI during export
        self.export_all_button.setEnabled(False)
        self.export_selected_button.setEnabled(False)
        
        # Show progress
        self.export_progress_bar.setVisible(True)
        self.export_progress_label.setVisible(True)
        self.export_progress_bar.setRange(0, 0)
        self.export_progress_label.setText("Preparing export...")
        
        # Start export worker
        self.export_worker = ExportWorker(
            self.current_analysis,
            export_path,
            move_files,
            preserve_structure,
            self.export_manager
        )
        self.export_worker.progress.connect(self.update_export_progress)
        self.export_worker.finished.connect(self.export_finished)
        self.export_worker.error.connect(self.export_error)
        self.export_worker.start()
        
        self.log_message(f"Starting export to: {export_path}")
    
    def update_export_progress(self, message, current, total):
        """Update export progress."""
        self.export_progress_label.setText(message)
        if total > 0:
            self.export_progress_bar.setRange(0, total)
            self.export_progress_bar.setValue(current)
    
    def export_finished(self, exported_count, skipped_count):
        """Handle export completion."""
        # Hide progress
        self.export_progress_bar.setVisible(False)
        self.export_progress_label.setVisible(False)
        
        # Re-enable UI
        self.export_all_button.setEnabled(True)
        self.export_selected_button.setEnabled(True)
        
        # Show completion message
        message = f"Export complete!\nExported: {exported_count} files\nSkipped: {skipped_count} files"
        QMessageBox.information(self, "Export Complete", message)
        
        self.log_message(f"Export complete. Exported: {exported_count}, Skipped: {skipped_count}")
    
    def export_error(self, error_message):
        """Handle export error."""
        # Hide progress
        self.export_progress_bar.setVisible(False)
        self.export_progress_label.setVisible(False)
        
        # Re-enable UI
        self.export_all_button.setEnabled(True)
        self.export_selected_button.setEnabled(True)
        
        # Show error message
        QMessageBox.critical(self, "Export Error", f"Export failed:\n{error_message}")
        self.log_message(f"Export error: {error_message}")
    
    def log_message(self, message):
        """Add message to log."""
        self.log_text.append(f"[{QTimer().singleShot.__class__.__name__}] {message}")
        logger.info(message)
    
    def closeEvent(self, event):
        """Handle application close."""
        # Stop any running workers
        if self.analysis_worker and self.analysis_worker.isRunning():
            self.analysis_worker.terminate()
            self.analysis_worker.wait()
        
        if self.export_worker and self.export_worker.isRunning():
            self.export_worker.terminate()
            self.export_worker.wait()
        
        event.accept()
