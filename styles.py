"""
Application Styles - Define consistent styling for the File Organizer application.
"""

class AppStyles:
    """Application-wide style definitions."""
    
    # Light theme color palette
    LIGHT_COLORS = {
        'primary': '#2196F3',      # Blue
        'secondary': '#4CAF50',    # Green
        'warning': '#FF9800',      # Orange
        'error': '#F44336',        # Red
        'background': '#FAFAFA',   # Light grey
        'text': '#212121',         # Dark grey
        'text_secondary': '#757575',  # Medium grey
        'surface': '#FFFFFF',      # White
        'border': '#E0E0E0',       # Light border
        'hover': '#E3F2FD',        # Light blue
        'selected': '#BBDEFB'      # Blue selection
    }
    
    # Dark theme color palette
    DARK_COLORS = {
        'primary': '#BB86FC',      # Purple
        'secondary': '#03DAC6',    # Teal
        'warning': '#FF9800',      # Orange
        'error': '#CF6679',        # Pink
        'background': '#121212',   # Very dark grey
        'text': '#FFFFFF',         # White
        'text_secondary': '#B3B3B3',  # Light grey
        'surface': '#1E1E1E',      # Dark grey
        'border': '#3E3E3E',       # Medium grey
        'hover': '#2D2D2D',        # Slightly lighter dark
        'selected': '#3D3D3D'      # Selection grey
    }
    
    # Current theme (default to light)
    _current_theme = 'light'
    
    @classmethod
    def set_theme(cls, theme: str):
        """Set the current theme (light or dark)."""
        if theme in ['light', 'dark']:
            cls._current_theme = theme
    
    @classmethod
    def get_theme(cls) -> str:
        """Get the current theme."""
        return cls._current_theme
    
    @classmethod
    def get_colors(cls) -> dict:
        """Get colors for the current theme."""
        return cls.DARK_COLORS if cls._current_theme == 'dark' else cls.LIGHT_COLORS
    
    # For backward compatibility
    @property
    def COLORS(self):
        return self.get_colors()
    
    @classmethod
    def get_main_style(cls) -> str:
        """Get the main application stylesheet."""
        colors = cls.get_colors()
        
        return f"""
        /* Global Font Settings */
        * {{
            font-family: "Segoe UI", "Ubuntu", "Roboto", "Arial", sans-serif;
            font-size: 13px;
        }}
        
        /* Main Window */
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        
        /* Group Boxes */
        QGroupBox {{
            font-weight: bold;
            font-size: 13px;
            border: 2px solid {colors['border']};
            border-radius: 6px;
            margin-top: 1ex;
            padding-top: 12px;
            background-color: {colors['surface']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 6px 0 6px;
            color: {colors['primary']};
            font-weight: bold;
        }}
        
        /* Buttons - Enhanced */
        QPushButton {{
            background-color: {colors['primary']};
            border: none;
            color: white;
            padding: 10px 18px;
            text-align: center;
            font-size: 13px;
            font-weight: 500;
            border-radius: 6px;
            min-width: 90px;
            min-height: 32px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['primary']}CC;
        }}
        
        QPushButton:pressed {{
            background-color: {colors['primary']}AA;
        }}
        
        QPushButton:disabled {{
            background-color: {colors['text_secondary']};
            color: {colors['background']};
            opacity: 0.6;
        }}
        
        QPushButton[checkable="true"]:checked {{
            background-color: {colors['secondary']};
            border: 2px solid {colors['primary']};
        }}
        
        /* Line Edits - Enhanced */
        QLineEdit {{
            border: 2px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            font-family: "Segoe UI", "Ubuntu", "Roboto", "Arial", sans-serif;
            background-color: {colors['surface']};
            color: {colors['text']};
            min-height: 20px;
        }}
        
        QLineEdit:focus {{
            border-color: {colors['primary']};
            background-color: {colors['surface']};
        }}
        
        QLineEdit:disabled {{
            background-color: {colors['background']};
            color: {colors['text_secondary']};
        }}
        
        /* Combo Boxes - Enhanced */
        QComboBox {{
            border: 2px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            font-family: "Segoe UI", "Ubuntu", "Roboto", "Arial", sans-serif;
            background-color: {colors['surface']};
            color: {colors['text']};
            min-width: 120px;
            min-height: 20px;
        }}
        
        QComboBox:focus {{
            border-color: {colors['primary']};
        }}
        
        QComboBox:hover {{
            border-color: {colors['primary']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 24px;
            background-color: {colors['primary']};
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border: 6px solid transparent;
            border-top-color: white;
            margin-right: 6px;
        }}
        
        QComboBox QAbstractItemView {{
            border: 2px solid {colors['border']};
            background-color: {colors['surface']};
            color: {colors['text']};
            selection-background-color: {colors['selected']};
            border-radius: 6px;
        }}
        
        /* Tables - Enhanced */
        QTableWidget {{
            gridline-color: {colors['border']};
            background-color: {colors['surface']};
            alternate-background-color: {colors['background']};
            selection-background-color: {colors['selected']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            font-size: 13px;
            color: {colors['text']};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors['selected']};
            color: {colors['text']};
        }}
        
        QTableWidget::item:hover {{
            background-color: {colors['hover']};
        }}
        
        QHeaderView::section {{
            background-color: {colors['primary']};
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
            font-size: 13px;
        }}
        
        /* Tree Widget - Enhanced */
        QTreeWidget {{
            background-color: {colors['surface']};
            alternate-background-color: {colors['background']};
            selection-background-color: {colors['selected']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            font-size: 13px;
            color: {colors['text']};
        }}
        
        QTreeWidget::item {{
            padding: 6px;
            border: none;
        }}
        
        QTreeWidget::item:selected {{
            background-color: {colors['selected']};
            color: {colors['text']};
        }}
        
        QTreeWidget::item:hover {{
            background-color: {colors['hover']};
        }}
        
        /* Tab Widget - Enhanced */
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            background-color: {colors['surface']};
            border-radius: 6px;
        }}
        
        QTabBar::tab {{
            background-color: {colors['background']};
            border: 1px solid {colors['border']};
            padding: 10px 18px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-size: 13px;
            color: {colors['text']};
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        QTabBar::tab:hover {{
            background-color: {colors['hover']};
        }}
        
        /* Progress Bar - Enhanced */
        QProgressBar {{
            border: 2px solid {colors['border']};
            border-radius: 6px;
            text-align: center;
            background-color: {colors['background']};
            font-size: 13px;
            color: {colors['text']};
            min-height: 20px;
        }}
        
        QProgressBar::chunk {{
            background-color: {colors['primary']};
            border-radius: 4px;
        }}
        
        /* Text Edit - Enhanced */
        QTextEdit {{
            border: 1px solid {colors['border']};
            border-radius: 6px;
            background-color: {colors['surface']};
            color: {colors['text']};
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            padding: 8px;
        }}
        
        /* Status Bar - Enhanced */
        QStatusBar {{
            background-color: {colors['background']};
            color: {colors['text']};
            border-top: 1px solid {colors['border']};
            font-size: 13px;
        }}
        
        QStatusBar::item {{
            border: none;
        }}
        
        /* Labels - Enhanced */
        QLabel {{
            color: {colors['text']};
            font-size: 13px;
        }}
        
        /* Splitter - Enhanced */
        QSplitter::handle {{
            background-color: {colors['border']};
        }}
        
        QSplitter::handle:horizontal {{
            width: 3px;
        }}
        
        QSplitter::handle:vertical {{
            height: 3px;
        }}
        
        /* Scroll Bars - Enhanced */
        QScrollBar:vertical {{
            background-color: {colors['background']};
            width: 14px;
            border-radius: 7px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['text_secondary']};
            border-radius: 7px;
            min-height: 24px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['text']};
        }}
        
        QScrollBar:horizontal {{
            background-color: {colors['background']};
            height: 14px;
            border-radius: 7px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors['text_secondary']};
            border-radius: 7px;
            min-width: 24px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors['text']};
        }}
        
        QScrollBar::add-line, QScrollBar::sub-line {{
            border: none;
            background: none;
        }}
        """
    
    @classmethod
    def get_button_style(cls, button_type: str = 'primary') -> str:
        """Get specific button styles."""
        styles = {
            'primary': f"""
                QPushButton {{
                    background-color: {cls.COLORS['primary']};
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: #1976D2;
                }}
            """,
            'secondary': f"""
                QPushButton {{
                    background-color: {cls.COLORS['secondary']};
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: #388E3C;
                }}
            """,
            'warning': f"""
                QPushButton {{
                    background-color: {cls.COLORS['warning']};
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: #F57C00;
                }}
            """,
            'error': f"""
                QPushButton {{
                    background-color: {cls.COLORS['error']};
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: #D32F2F;
                }}
            """
        }
        
        return styles.get(button_type, styles['primary'])
