"""
Statistics Widget - Display comprehensive file analysis statistics.
"""

import os
import csv
import json
import logging
from pathlib import Path
from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QGroupBox, QPushButton, QLabel, QTabWidget, QHeaderView, QFileDialog,
    QMessageBox, QProgressBar, QSplitter, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from utils import format_file_size

logger = logging.getLogger(__name__)

class StatisticsWidget(QWidget):
    """Widget for displaying file analysis statistics."""
    
    export_requested = pyqtSignal(str, dict)  # format, data
    
    def __init__(self):
        super().__init__()
        self.current_analysis = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the statistics interface."""
        layout = QVBoxLayout(self)
        
        # Create tab widget for different statistics views
        self.stats_tabs = QTabWidget()
        layout.addWidget(self.stats_tabs)
        
        # Overview tab
        overview_widget = self.create_overview_tab()
        self.stats_tabs.addTab(overview_widget, "Overview")
        
        # File Types tab
        types_widget = self.create_types_tab()
        self.stats_tabs.addTab(types_widget, "File Types")
        
        # Extensions tab
        extensions_widget = self.create_extensions_tab()
        self.stats_tabs.addTab(extensions_widget, "Extensions")
        
        # Largest Files tab
        largest_widget = self.create_largest_files_tab()
        self.stats_tabs.addTab(largest_widget, "Largest Files")
        
        # Export controls
        export_widget = self.create_export_controls()
        layout.addWidget(export_widget)
    
    def create_overview_tab(self):
        """Create the overview statistics tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Summary statistics group
        summary_group = QGroupBox("Summary Statistics")
        summary_layout = QVBoxLayout(summary_group)
        
        # Create summary labels
        self.total_files_label = QLabel("Total Files: 0")
        self.total_size_label = QLabel("Total Size: 0 B")
        self.avg_file_size_label = QLabel("Average File Size: 0 B")
        self.largest_file_label = QLabel("Largest File: N/A")
        
        # Apply styling to summary labels
        for label in [self.total_files_label, self.total_size_label, 
                     self.avg_file_size_label, self.largest_file_label]:
            font = label.font()
            font.setPointSize(12)
            font.setBold(True)
            label.setFont(font)
            summary_layout.addWidget(label)
        
        layout.addWidget(summary_group)
        
        # Directory information
        dir_group = QGroupBox("Directory Information")
        dir_layout = QVBoxLayout(dir_group)
        
        self.root_path_label = QLabel("Root Path: Not selected")
        self.error_count_label = QLabel("Errors: 0")
        
        dir_layout.addWidget(self.root_path_label)
        dir_layout.addWidget(self.error_count_label)
        
        layout.addWidget(dir_group)
        layout.addStretch()
        
        return widget
    
    def create_types_tab(self):
        """Create the file types statistics tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # File types table
        types_group = QGroupBox("Files by Type")
        types_layout = QVBoxLayout(types_group)
        
        self.types_table = QTableWidget()
        self.types_table.setColumnCount(4)
        self.types_table.setHorizontalHeaderLabels(["Type", "Count", "Total Size", "Percentage"])
        self.types_table.setAlternatingRowColors(True)
        self.types_table.setSortingEnabled(True)
        
        # Configure table
        header = self.types_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        types_layout.addWidget(self.types_table)
        layout.addWidget(types_group)
        
        return widget
    
    def create_extensions_tab(self):
        """Create the file extensions statistics tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Extensions table
        ext_group = QGroupBox("Files by Extension")
        ext_layout = QVBoxLayout(ext_group)
        
        self.extensions_table = QTableWidget()
        self.extensions_table.setColumnCount(4)
        self.extensions_table.setHorizontalHeaderLabels(["Extension", "Count", "Total Size", "Percentage"])
        self.extensions_table.setAlternatingRowColors(True)
        self.extensions_table.setSortingEnabled(True)
        
        # Configure table
        header = self.extensions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        ext_layout.addWidget(self.extensions_table)
        layout.addWidget(ext_group)
        
        return widget
    
    def create_largest_files_tab(self):
        """Create the largest files tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Largest files table
        largest_group = QGroupBox("Largest Files")
        largest_layout = QVBoxLayout(largest_group)
        
        self.largest_table = QTableWidget()
        self.largest_table.setColumnCount(5)
        self.largest_table.setHorizontalHeaderLabels(["Name", "Size", "Type", "Extension", "Path"])
        self.largest_table.setAlternatingRowColors(True)
        self.largest_table.setSortingEnabled(True)
        
        # Configure table
        header = self.largest_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
        largest_layout.addWidget(self.largest_table)
        layout.addWidget(largest_group)
        
        return widget
    
    def create_export_controls(self):
        """Create export control widgets."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Export format selection
        layout.addWidget(QLabel("Export Format:"))
        
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["CSV", "JSON"])
        layout.addWidget(self.export_format_combo)
        
        # Export buttons
        self.export_current_button = QPushButton("Export Current Tab")
        self.export_current_button.clicked.connect(self.export_current_tab)
        self.export_current_button.setEnabled(False)
        layout.addWidget(self.export_current_button)
        
        self.export_all_button = QPushButton("Export All Statistics")
        self.export_all_button.clicked.connect(self.export_all_statistics)
        self.export_all_button.setEnabled(False)
        layout.addWidget(self.export_all_button)
        
        layout.addStretch()
        
        return widget
    
    def update_statistics(self, analysis_result):
        """Update all statistics displays with new analysis results."""
        self.current_analysis = analysis_result
        
        # Update overview
        self.update_overview(analysis_result)
        
        # Update file types
        self.update_types_table(analysis_result)
        
        # Update extensions
        self.update_extensions_table(analysis_result)
        
        # Update largest files
        self.update_largest_files_table(analysis_result)
        
        # Enable export buttons
        self.export_current_button.setEnabled(True)
        self.export_all_button.setEnabled(True)
        
        logger.info("Statistics updated successfully")
    
    def update_overview(self, analysis_result):
        """Update overview statistics."""
        total_files = analysis_result.total_files
        total_size = analysis_result.total_size
        avg_size = total_size / total_files if total_files > 0 else 0
        
        largest_file = analysis_result.largest_files[0] if analysis_result.largest_files else None
        largest_name = f"{largest_file.name} ({format_file_size(largest_file.size)})" if largest_file else "N/A"
        
        self.total_files_label.setText(f"Total Files: {total_files:,}")
        self.total_size_label.setText(f"Total Size: {format_file_size(total_size)}")
        self.avg_file_size_label.setText(f"Average File Size: {format_file_size(avg_size)}")
        self.largest_file_label.setText(f"Largest File: {largest_name}")
        
        self.root_path_label.setText(f"Root Path: {analysis_result.root_path}")
        self.error_count_label.setText(f"Errors: {len(analysis_result.error_files)}")
    
    def update_types_table(self, analysis_result):
        """Update file types table."""
        self.types_table.setRowCount(0)
        
        total_files = analysis_result.total_files
        total_size = analysis_result.total_size
        
        for file_type, files in analysis_result.files_by_type.items():
            if not files:  # Skip empty types
                continue
                
            row = self.types_table.rowCount()
            self.types_table.insertRow(row)
            
            count = len(files)
            type_size = sum(f.size for f in files)
            percentage = (count / total_files * 100) if total_files > 0 else 0
            
            self.types_table.setItem(row, 0, QTableWidgetItem(file_type.title()))
            self.types_table.setItem(row, 1, QTableWidgetItem(f"{count:,}"))
            self.types_table.setItem(row, 2, QTableWidgetItem(format_file_size(type_size)))
            self.types_table.setItem(row, 3, QTableWidgetItem(f"{percentage:.1f}%"))
    
    def update_extensions_table(self, analysis_result):
        """Update file extensions table."""
        self.extensions_table.setRowCount(0)
        
        total_files = analysis_result.total_files
        
        # Sort extensions by count
        ext_data = []
        for ext, files in analysis_result.files_by_extension.items():
            count = len(files)
            ext_size = sum(f.size for f in files)
            percentage = (count / total_files * 100) if total_files > 0 else 0
            ext_data.append((ext or "No Extension", count, ext_size, percentage))
        
        ext_data.sort(key=lambda x: x[1], reverse=True)
        
        for ext_name, count, ext_size, percentage in ext_data[:100]:  # Limit to top 100
            row = self.extensions_table.rowCount()
            self.extensions_table.insertRow(row)
            
            self.extensions_table.setItem(row, 0, QTableWidgetItem(ext_name))
            self.extensions_table.setItem(row, 1, QTableWidgetItem(f"{count:,}"))
            self.extensions_table.setItem(row, 2, QTableWidgetItem(format_file_size(ext_size)))
            self.extensions_table.setItem(row, 3, QTableWidgetItem(f"{percentage:.1f}%"))
    
    def update_largest_files_table(self, analysis_result):
        """Update largest files table."""
        self.largest_table.setRowCount(0)
        
        for file_info in analysis_result.largest_files[:100]:  # Top 100 largest
            row = self.largest_table.rowCount()
            self.largest_table.insertRow(row)
            
            self.largest_table.setItem(row, 0, QTableWidgetItem(file_info.name))
            self.largest_table.setItem(row, 1, QTableWidgetItem(format_file_size(file_info.size)))
            self.largest_table.setItem(row, 2, QTableWidgetItem(file_info.type.title()))
            self.largest_table.setItem(row, 3, QTableWidgetItem(file_info.extension))
            self.largest_table.setItem(row, 4, QTableWidgetItem(str(file_info.path)))
    
    def export_current_tab(self):
        """Export data from the currently selected tab."""
        if not self.current_analysis:
            QMessageBox.warning(self, "Warning", "No data to export.")
            return
        
        current_tab = self.stats_tabs.currentIndex()
        tab_names = ["overview", "types", "extensions", "largest_files"]
        
        if current_tab < len(tab_names):
            self.export_data(tab_names[current_tab])
    
    def export_all_statistics(self):
        """Export all statistics data."""
        if not self.current_analysis:
            QMessageBox.warning(self, "Warning", "No data to export.")
            return
        
        self.export_data("all")
    
    def export_data(self, data_type):
        """Export statistics data to file."""
        if not self.current_analysis:
            return
        
        format_type = self.export_format_combo.currentText().lower()
        
        # Get save location
        if format_type == "csv":
            file_filter = "CSV Files (*.csv)"
            default_ext = ".csv"
        else:
            file_filter = "JSON Files (*.json)"
            default_ext = ".json"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Export {data_type.title()} Statistics",
            f"file_statistics_{data_type}{default_ext}",
            file_filter
        )
        
        if not file_path:
            return
        
        try:
            if format_type == "csv":
                self.export_to_csv(file_path, data_type)
            else:
                self.export_to_json(file_path, data_type)
            
            QMessageBox.information(self, "Export Complete", f"Statistics exported to:\n{file_path}")
            logger.info(f"Statistics exported to {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export data:\n{str(e)}")
            logger.error(f"Export error: {e}", exc_info=True)
    
    def export_to_csv(self, file_path, data_type):
        """Export data to CSV format."""
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            if data_type == "overview" or data_type == "all":
                writer.writerow(["Overview Statistics"])
                writer.writerow(["Metric", "Value"])
                writer.writerow(["Total Files", f"{self.current_analysis.total_files:,}"])
                writer.writerow(["Total Size", format_file_size(self.current_analysis.total_size)])
                writer.writerow(["Root Path", str(self.current_analysis.root_path)])
                writer.writerow(["Errors", len(self.current_analysis.error_files)])
                writer.writerow([])
            
            if data_type == "types" or data_type == "all":
                writer.writerow(["File Types"])
                writer.writerow(["Type", "Count", "Total Size", "Percentage"])
                for file_type, files in self.current_analysis.files_by_type.items():
                    if files:
                        count = len(files)
                        type_size = sum(f.size for f in files)
                        percentage = (count / self.current_analysis.total_files * 100) if self.current_analysis.total_files > 0 else 0
                        writer.writerow([file_type.title(), count, format_file_size(type_size), f"{percentage:.1f}%"])
                writer.writerow([])
            
            if data_type == "extensions" or data_type == "all":
                writer.writerow(["File Extensions"])
                writer.writerow(["Extension", "Count", "Total Size", "Percentage"])
                for ext, files in sorted(self.current_analysis.files_by_extension.items(), key=lambda x: len(x[1]), reverse=True):
                    count = len(files)
                    ext_size = sum(f.size for f in files)
                    percentage = (count / self.current_analysis.total_files * 100) if self.current_analysis.total_files > 0 else 0
                    writer.writerow([ext or "No Extension", count, format_file_size(ext_size), f"{percentage:.1f}%"])
                writer.writerow([])
            
            if data_type == "largest_files" or data_type == "all":
                writer.writerow(["Largest Files"])
                writer.writerow(["Name", "Size", "Type", "Extension", "Path"])
                for file_info in self.current_analysis.largest_files[:100]:
                    writer.writerow([
                        file_info.name,
                        format_file_size(file_info.size),
                        file_info.type.title(),
                        file_info.extension,
                        str(file_info.path)
                    ])
    
    def export_to_json(self, file_path, data_type):
        """Export data to JSON format."""
        data = {}
        
        if data_type == "overview" or data_type == "all":
            data["overview"] = {
                "total_files": self.current_analysis.total_files,
                "total_size": self.current_analysis.total_size,
                "total_size_formatted": format_file_size(self.current_analysis.total_size),
                "root_path": str(self.current_analysis.root_path),
                "error_count": len(self.current_analysis.error_files)
            }
        
        if data_type == "types" or data_type == "all":
            data["file_types"] = {}
            for file_type, files in self.current_analysis.files_by_type.items():
                if files:
                    count = len(files)
                    type_size = sum(f.size for f in files)
                    percentage = (count / self.current_analysis.total_files * 100) if self.current_analysis.total_files > 0 else 0
                    data["file_types"][file_type] = {
                        "count": count,
                        "total_size": type_size,
                        "total_size_formatted": format_file_size(type_size),
                        "percentage": round(percentage, 1)
                    }
        
        if data_type == "extensions" or data_type == "all":
            data["extensions"] = {}
            for ext, files in self.current_analysis.files_by_extension.items():
                count = len(files)
                ext_size = sum(f.size for f in files)
                percentage = (count / self.current_analysis.total_files * 100) if self.current_analysis.total_files > 0 else 0
                data["extensions"][ext or "no_extension"] = {
                    "count": count,
                    "total_size": ext_size,
                    "total_size_formatted": format_file_size(ext_size),
                    "percentage": round(percentage, 1)
                }
        
        if data_type == "largest_files" or data_type == "all":
            data["largest_files"] = []
            for file_info in self.current_analysis.largest_files[:100]:
                data["largest_files"].append({
                    "name": file_info.name,
                    "size": file_info.size,
                    "size_formatted": format_file_size(file_info.size),
                    "type": file_info.type,
                    "extension": file_info.extension,
                    "path": str(file_info.path)
                })
        
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    def clear_data(self):
        """Clear all displayed data."""
        self.current_analysis = None
        
        # Clear overview
        self.total_files_label.setText("Total Files: 0")
        self.total_size_label.setText("Total Size: 0 B")
        self.avg_file_size_label.setText("Average File Size: 0 B")
        self.largest_file_label.setText("Largest File: N/A")
        self.root_path_label.setText("Root Path: Not selected")
        self.error_count_label.setText("Errors: 0")
        
        # Clear tables
        self.types_table.setRowCount(0)
        self.extensions_table.setRowCount(0)
        self.largest_table.setRowCount(0)
        
        # Disable export buttons
        self.export_current_button.setEnabled(False)
        self.export_all_button.setEnabled(False)
