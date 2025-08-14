"""
Export Manager - Handle file organization and export operations.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Tuple
from PyQt6.QtCore import QThread, pyqtSignal

from file_analyzer import AnalysisResult, FileInfo

logger = logging.getLogger(__name__)

class ExportManager:
    """Manages file export and organization operations."""
    
    def __init__(self):
        """Initialize the export manager."""
        logger.info("Export manager initialized")
    
    def create_export_structure(self, export_path: Path, preserve_structure: bool = True) -> Dict[str, Path]:
        """Create the export directory structure."""
        export_path = Path(export_path)
        export_path.mkdir(parents=True, exist_ok=True)
        
        # Create type-based subdirectories
        type_dirs = {}
        file_types = ['images', 'videos', 'audio', 'documents', 'archives', 'executables', 'unknown']
        
        for file_type in file_types:
            type_dir = export_path / file_type
            type_dir.mkdir(exist_ok=True)
            type_dirs[file_type] = type_dir
        
        logger.info(f"Created export structure at {export_path}")
        return type_dirs
    
    def get_export_destination(self, file_info: FileInfo, type_dirs: Dict[str, Path], 
                             preserve_structure: bool, root_path: Path) -> Path:
        """Determine the export destination for a file."""
        type_dir = type_dirs[file_info.type]
        
        if preserve_structure:
            # Calculate relative path from root
            try:
                rel_path = file_info.path.parent.relative_to(root_path)
                dest_dir = type_dir / rel_path
                dest_dir.mkdir(parents=True, exist_ok=True)
                return dest_dir / file_info.name
            except ValueError:
                # If relative path calculation fails, use type directory
                return type_dir / file_info.name
        else:
            return type_dir / file_info.name
    
    def export_file(self, file_info: FileInfo, destination: Path, move_file: bool = False) -> bool:
        """Export a single file to destination."""
        try:
            source = file_info.path
            
            # Handle filename conflicts
            if destination.exists():
                base = destination.stem
                suffix = destination.suffix
                counter = 1
                while destination.exists():
                    new_name = f"{base}_{counter}{suffix}"
                    destination = destination.parent / new_name
                    counter += 1
            
            # Perform the operation
            if move_file:
                shutil.move(str(source), str(destination))
                logger.debug(f"Moved {source} to {destination}")
            else:
                shutil.copy2(str(source), str(destination))
                logger.debug(f"Copied {source} to {destination}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error exporting file {file_info.path}: {e}")
            return False
    
    def export_files(self, analysis_result: AnalysisResult, export_path: str, 
                    move_files: bool = False, preserve_structure: bool = True,
                    selected_extensions: List[str] = None, progress_callback=None) -> Tuple[int, int]:
        """Export files based on analysis results."""
        export_path = Path(export_path)
        
        # Create export structure
        type_dirs = self.create_export_structure(export_path, preserve_structure)
        
        # Collect files to export
        files_to_export = []
        
        if selected_extensions is None:
            # Export all files
            for file_type, files in analysis_result.files_by_type.items():
                files_to_export.extend(files)
        else:
            # Export only files with selected extensions
            for file_type, files in analysis_result.files_by_type.items():
                for file_info in files:
                    if file_info.extension.lower() in [ext.lower() for ext in selected_extensions]:
                        files_to_export.append(file_info)
        
        total_files = len(files_to_export)
        exported_count = 0
        skipped_count = 0
        
        logger.info(f"Starting export of {total_files} files to {export_path}")
        
        for i, file_info in enumerate(files_to_export):
            try:
                if progress_callback:
                    progress_callback(f"Exporting: {file_info.name}", i, total_files)
                
                # Get destination path
                destination = self.get_export_destination(
                    file_info, type_dirs, preserve_structure, analysis_result.root_path
                )
                
                # Export the file
                if self.export_file(file_info, destination, move_files):
                    exported_count += 1
                else:
                    skipped_count += 1
                
            except Exception as e:
                logger.error(f"Error processing file {file_info.path}: {e}")
                skipped_count += 1
        
        logger.info(f"Export complete: {exported_count} exported, {skipped_count} skipped")
        return exported_count, skipped_count
    
    def validate_export_path(self, export_path: str) -> bool:
        """Validate that the export path is usable."""
        try:
            export_path = Path(export_path)
            
            # Check if path exists or can be created
            if not export_path.exists():
                export_path.mkdir(parents=True, exist_ok=True)
            
            # Check if writable
            test_file = export_path / ".test_write"
            test_file.touch()
            test_file.unlink()
            
            return True
            
        except Exception as e:
            logger.error(f"Export path validation failed: {e}")
            return False

class ExportWorker(QThread):
    """Worker thread for performing file export operations."""
    
    progress = pyqtSignal(str, int, int)  # message, current, total
    finished = pyqtSignal(int, int)  # exported_count, skipped_count
    error = pyqtSignal(str)  # error message
    
    def __init__(self, analysis_result: AnalysisResult, export_path: str, 
                 move_files: bool, preserve_structure: bool, export_manager: ExportManager,
                 selected_extensions: List[str] = None):
        super().__init__()
        self.analysis_result = analysis_result
        self.export_path = export_path
        self.move_files = move_files
        self.preserve_structure = preserve_structure
        self.export_manager = export_manager
        self.selected_extensions = selected_extensions
    
    def run(self):
        """Run the export operation in background thread."""
        try:
            def progress_callback(message, current, total):
                self.progress.emit(message, current, total)
            
            # Validate export path
            if not self.export_manager.validate_export_path(self.export_path):
                self.error.emit(f"Invalid or inaccessible export path: {self.export_path}")
                return
            
            # Perform export
            exported_count, skipped_count = self.export_manager.export_files(
                self.analysis_result,
                self.export_path,
                self.move_files,
                self.preserve_structure,
                self.selected_extensions,
                progress_callback
            )
            
            self.finished.emit(exported_count, skipped_count)
            
        except Exception as e:
            logger.error(f"Export worker error: {e}", exc_info=True)
            self.error.emit(str(e))
