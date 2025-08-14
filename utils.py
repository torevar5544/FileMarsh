"""
Utility Functions - Common helper functions for the File Organizer application.
"""

import os
import mimetypes
from pathlib import Path
from typing import Union

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
    size_index = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and size_index < len(size_names) - 1:
        size /= 1024.0
        size_index += 1
    
    if size_index == 0:
        return f"{int(size)} {size_names[size_index]}"
    else:
        return f"{size:.1f} {size_names[size_index]}"

def get_file_icon(file_path: Union[str, Path]) -> str:
    """Get appropriate icon name for file type (for future use with icon libraries)."""
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    # Icon mappings based on file types
    icon_mappings = {
        # Images
        '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image',
        '.bmp': 'image', '.tiff': 'image', '.svg': 'image', '.webp': 'image',
        
        # Videos
        '.mp4': 'video', '.avi': 'video', '.mkv': 'video', '.mov': 'video',
        '.wmv': 'video', '.flv': 'video', '.webm': 'video',
        
        # Audio
        '.mp3': 'music', '.wav': 'music', '.flac': 'music', '.aac': 'music',
        '.ogg': 'music', '.wma': 'music', '.m4a': 'music',
        
        # Documents
        '.pdf': 'file-text', '.doc': 'file-text', '.docx': 'file-text',
        '.txt': 'file-text', '.rtf': 'file-text', '.odt': 'file-text',
        '.xls': 'file-text', '.xlsx': 'file-text', '.ppt': 'file-text',
        '.pptx': 'file-text', '.csv': 'file-text',
        
        # Archives
        '.zip': 'archive', '.rar': 'archive', '.7z': 'archive',
        '.tar': 'archive', '.gz': 'archive', '.bz2': 'archive',
        
        # Code files
        '.py': 'code', '.js': 'code', '.html': 'code', '.css': 'code',
        '.cpp': 'code', '.c': 'code', '.java': 'code', '.php': 'code',
        
        # Executables
        '.exe': 'settings', '.msi': 'settings', '.deb': 'settings',
        '.rpm': 'settings', '.dmg': 'settings', '.app': 'settings'
    }
    
    return icon_mappings.get(extension, 'file')

def sanitize_filename(filename: str, replacement: str = '_') -> str:
    """Sanitize filename by replacing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    
    for char in invalid_chars:
        filename = filename.replace(char, replacement)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Ensure filename is not empty
    if not filename:
        filename = 'unnamed_file'
    
    return filename

def is_hidden_file(file_path: Union[str, Path]) -> bool:
    """Check if file is hidden (starts with dot on Unix systems)."""
    file_path = Path(file_path)
    return file_path.name.startswith('.')

def get_safe_path(base_path: Union[str, Path], relative_path: Union[str, Path]) -> Path:
    """Safely join paths, preventing directory traversal attacks."""
    base_path = Path(base_path).resolve()
    relative_path = Path(relative_path)
    
    # Remove any parent directory references
    safe_parts = []
    for part in relative_path.parts:
        if part not in ('..', '.'):
            safe_parts.append(part)
    
    if not safe_parts:
        return base_path
    
    safe_relative = Path(*safe_parts)
    result_path = base_path / safe_relative
    
    # Ensure the result is still within the base path
    try:
        result_path.resolve().relative_to(base_path)
        return result_path
    except ValueError:
        # If relative_to fails, the path is outside base_path
        return base_path / safe_relative.name

def get_directory_size(directory_path: Union[str, Path]) -> int:
    """Calculate total size of all files in directory recursively."""
    directory_path = Path(directory_path)
    total_size = 0
    
    try:
        for file_path in directory_path.rglob('*'):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except (OSError, IOError):
                    # Skip files that can't be accessed
                    continue
    except (OSError, IOError):
        # Handle permission errors or other filesystem issues
        pass
    
    return total_size

def create_backup_name(file_path: Union[str, Path]) -> Path:
    """Create a backup filename by appending timestamp."""
    import datetime
    
    file_path = Path(file_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if file_path.suffix:
        backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    else:
        backup_name = f"{file_path.name}_backup_{timestamp}"
    
    return file_path.parent / backup_name

def validate_export_destination(export_path: Union[str, Path], 
                              source_path: Union[str, Path] = None) -> tuple[bool, str]:
    """Validate export destination path."""
    export_path = Path(export_path)
    
    # Check if path is absolute
    if not export_path.is_absolute():
        return False, "Export path must be absolute"
    
    # Check if we can create the directory
    try:
        export_path.mkdir(parents=True, exist_ok=True)
    except (OSError, IOError) as e:
        return False, f"Cannot create export directory: {e}"
    
    # Check if directory is writable
    if not os.access(export_path, os.W_OK):
        return False, "Export directory is not writable"
    
    # Check if export path is not a subdirectory of source (to prevent recursion)
    if source_path:
        source_path = Path(source_path).resolve()
        try:
            export_path.resolve().relative_to(source_path)
            return False, "Export path cannot be inside source directory"
        except ValueError:
            # This is good - export path is not inside source
            pass
    
    return True, "Export path is valid"

def estimate_operation_time(file_count: int, total_size: int, operation_type: str = 'copy') -> str:
    """Estimate operation time based on file count and size."""
    # Rough estimates based on typical disk speeds
    # These are very approximate and can vary greatly
    
    if operation_type == 'copy':
        # Assume ~50 MB/s for copying
        size_time = total_size / (50 * 1024 * 1024)  # seconds
        # Assume ~100 files/second for file operations
        file_time = file_count / 100  # seconds
    else:  # move
        # Moving is typically faster (just metadata changes for same drive)
        size_time = total_size / (100 * 1024 * 1024)  # seconds
        file_time = file_count / 200  # seconds
    
    estimated_seconds = max(size_time, file_time)
    
    if estimated_seconds < 60:
        return f"~{int(estimated_seconds)} seconds"
    elif estimated_seconds < 3600:
        minutes = int(estimated_seconds / 60)
        return f"~{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        hours = int(estimated_seconds / 3600)
        minutes = int((estimated_seconds % 3600) / 60)
        if minutes > 0:
            return f"~{hours}h {minutes}m"
        else:
            return f"~{hours} hour{'s' if hours != 1 else ''}"

def get_mime_type_category(mime_type: str) -> str:
    """Get general category from MIME type."""
    if not mime_type:
        return 'unknown'
    
    category_mappings = {
        'image/': 'images',
        'video/': 'videos', 
        'audio/': 'audio',
        'text/': 'documents',
        'application/pdf': 'documents',
        'application/msword': 'documents',
        'application/vnd.openxmlformats': 'documents',
        'application/zip': 'archives',
        'application/x-rar': 'archives',
        'application/x-tar': 'archives',
        'application/x-executable': 'executables',
        'application/x-msdownload': 'executables'
    }
    
    for prefix, category in category_mappings.items():
        if mime_type.startswith(prefix):
            return category
    
    return 'unknown'
