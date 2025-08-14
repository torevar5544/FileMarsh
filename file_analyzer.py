"""
File Analyzer - Core file analysis and classification functionality.
"""

import os
import mimetypes
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set
from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger(__name__)

@dataclass
class FileInfo:
    """Information about a single file."""
    path: Path
    name: str
    size: int
    type: str
    mime_type: str
    extension: str
    
    def __post_init__(self):
        """Post-initialization processing."""
        if not self.name:
            self.name = self.path.name
        if not self.extension:
            self.extension = self.path.suffix.lower()

@dataclass
class AnalysisResult:
    """Results of folder analysis."""
    root_path: Path
    total_files: int = 0
    total_size: int = 0
    files_by_type: Dict[str, List[FileInfo]] = field(default_factory=dict)
    files_by_extension: Dict[str, List[FileInfo]] = field(default_factory=dict)
    largest_files: List[FileInfo] = field(default_factory=list)
    error_files: List[tuple] = field(default_factory=list)  # (path, error)

class FileAnalyzer:
    """Analyzes and classifies files in directories."""
    
    # File type classifications based on MIME types and extensions
    TYPE_MAPPINGS = {
        'images': {
            'mime_prefixes': ['image/'],
            'extensions': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', 
                          '.webp', '.svg', '.ico', '.raw', '.cr2', '.nef', '.arw'}
        },
        'videos': {
            'mime_prefixes': ['video/'],
            'extensions': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
                          '.m4v', '.mpg', '.mpeg', '.3gp', '.ts', '.vob'}
        },
        'audio': {
            'mime_prefixes': ['audio/'],
            'extensions': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', 
                          '.opus', '.aiff', '.au', '.ra'}
        },
        'documents': {
            'mime_prefixes': ['text/', 'application/pdf', 'application/msword', 
                            'application/vnd.openxmlformats-officedocument'],
            'extensions': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', 
                          '.xlsx', '.ppt', '.pptx', '.odp', '.ods', '.csv', '.md', 
                          '.html', '.htm', '.xml', '.json', '.yaml', '.yml'}
        },
        'archives': {
            'mime_prefixes': ['application/zip', 'application/x-rar', 'application/x-tar'],
            'extensions': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', 
                          '.tar.gz', '.tar.bz2', '.tar.xz', '.jar', '.war', '.ear'}
        },
        'executables': {
            'mime_prefixes': ['application/x-executable', 'application/x-msdownload'],
            'extensions': {'.exe', '.msi', '.deb', '.rpm', '.dmg', '.pkg', '.app', 
                          '.run', '.bin', '.jar'}
        }
    }
    
    def __init__(self):
        """Initialize the file analyzer."""
        # Initialize mimetypes
        mimetypes.init()
        logger.info("File analyzer initialized")
    
    def classify_file(self, file_path: Path) -> str:
        """Classify a file based on its MIME type and extension."""
        try:
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            extension = file_path.suffix.lower()
            
            # Check each type category
            for file_type, mappings in self.TYPE_MAPPINGS.items():
                # Check MIME type prefixes
                if mime_type:
                    for prefix in mappings['mime_prefixes']:
                        if mime_type.startswith(prefix):
                            return file_type
                
                # Check extensions
                if extension in mappings['extensions']:
                    return file_type
            
            return 'unknown'
            
        except Exception as e:
            logger.warning(f"Error classifying file {file_path}: {e}")
            return 'unknown'
    
    def analyze_file(self, file_path: Path) -> FileInfo:
        """Analyze a single file and return FileInfo."""
        try:
            stat_info = file_path.stat()
            mime_type, _ = mimetypes.guess_type(str(file_path))
            file_type = self.classify_file(file_path)
            
            return FileInfo(
                path=file_path,
                name=file_path.name,
                size=stat_info.st_size,
                type=file_type,
                mime_type=mime_type or 'unknown',
                extension=file_path.suffix.lower()
            )
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            raise
    
    def analyze_directory(self, directory_path: str, progress_callback=None) -> AnalysisResult:
        """Analyze a directory and return comprehensive results."""
        root_path = Path(directory_path)
        if not root_path.exists() or not root_path.is_dir():
            raise ValueError(f"Invalid directory path: {directory_path}")
        
        result = AnalysisResult(root_path=root_path)
        processed_count = 0
        
        # Initialize type dictionaries
        for file_type in self.TYPE_MAPPINGS.keys():
            result.files_by_type[file_type] = []
        result.files_by_type['unknown'] = []
        
        try:
            # Get all files recursively
            all_files = []
            for file_path in root_path.rglob('*'):
                if file_path.is_file():
                    all_files.append(file_path)
            
            total_files = len(all_files)
            logger.info(f"Found {total_files} files to analyze")
            
            # Process each file
            for file_path in all_files:
                try:
                    if progress_callback:
                        progress_callback(f"Analyzing: {file_path.name}", processed_count, total_files)
                    
                    file_info = self.analyze_file(file_path)
                    
                    # Add to type classification
                    result.files_by_type[file_info.type].append(file_info)
                    
                    # Add to extension classification
                    ext = file_info.extension
                    if ext not in result.files_by_extension:
                        result.files_by_extension[ext] = []
                    result.files_by_extension[ext].append(file_info)
                    
                    # Update totals
                    result.total_size += file_info.size
                    
                    processed_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
                    result.error_files.append((file_path, str(e)))
            
            # Calculate final statistics
            result.total_files = processed_count
            
            # Find largest files
            all_file_infos = []
            for files in result.files_by_type.values():
                all_file_infos.extend(files)
            
            result.largest_files = sorted(all_file_infos, key=lambda f: f.size, reverse=True)[:50]
            
            logger.info(f"Analysis complete: {result.total_files} files, {result.total_size} bytes")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing directory {directory_path}: {e}")
            raise

class AnalysisWorker(QThread):
    """Worker thread for performing file analysis."""
    
    progress = pyqtSignal(str, int, int)  # message, current, total
    finished = pyqtSignal(object)  # AnalysisResult
    error = pyqtSignal(str)  # error message
    
    def __init__(self, directory_path: str, file_analyzer: FileAnalyzer):
        super().__init__()
        self.directory_path = directory_path
        self.file_analyzer = file_analyzer
    
    def run(self):
        """Run the analysis in background thread."""
        try:
            def progress_callback(message, current, total):
                self.progress.emit(message, current, total)
            
            result = self.file_analyzer.analyze_directory(
                self.directory_path, 
                progress_callback
            )
            self.finished.emit(result)
            
        except Exception as e:
            logger.error(f"Analysis worker error: {e}", exc_info=True)
            self.error.emit(str(e))
