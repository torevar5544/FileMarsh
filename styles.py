"""
Application Styles - Define consistent styling for the File Organizer application.
"""

class AppStyles:
    """Application-wide style definitions."""
    
    # Color palette
    COLORS = {
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
    
    @classmethod
    def get_main_style(cls) -> str:
        """Get the main application stylesheet."""
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text']};
        }}
        
        /* Group Boxes */
        QGroupBox {{
            font-weight: bold;
            font-size: 12px;
            border: 2px solid {cls.COLORS['border']};
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
            background-color: {cls.COLORS['surface']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: {cls.COLORS['primary']};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {cls.COLORS['primary']};
            border: none;
            color: white;
            padding: 8px 16px;
            text-align: center;
            font-size: 12px;
            border-radius: 4px;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: #1976D2;
        }}
        
        QPushButton:pressed {{
            background-color: #0D47A1;
        }}
        
        QPushButton:disabled {{
            background-color: {cls.COLORS['text_secondary']};
            color: #FFFFFF;
        }}
        
        QPushButton[checkable="true"]:checked {{
            background-color: {cls.COLORS['secondary']};
        }}
        
        /* Line Edits */
        QLineEdit {{
            border: 2px solid {cls.COLORS['border']};
            border-radius: 4px;
            padding: 5px;
            font-size: 12px;
            background-color: {cls.COLORS['surface']};
        }}
        
        QLineEdit:focus {{
            border-color: {cls.COLORS['primary']};
        }}
        
        /* Combo Boxes */
        QComboBox {{
            border: 2px solid {cls.COLORS['border']};
            border-radius: 4px;
            padding: 5px;
            font-size: 12px;
            background-color: {cls.COLORS['surface']};
            min-width: 100px;
        }}
        
        QComboBox:focus {{
            border-color: {cls.COLORS['primary']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border: 5px solid {cls.COLORS['text']};
            border-top-color: {cls.COLORS['text']};
            border-left-color: transparent;
            border-right-color: transparent;
            border-bottom-color: transparent;
        }}
        
        /* Tables */
        QTableWidget {{
            gridline-color: {cls.COLORS['border']};
            background-color: {cls.COLORS['surface']};
            alternate-background-color: {cls.COLORS['background']};
            selection-background-color: {cls.COLORS['selected']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 4px;
        }}
        
        QTableWidget::item {{
            padding: 5px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {cls.COLORS['selected']};
        }}
        
        QHeaderView::section {{
            background-color: {cls.COLORS['primary']};
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }}
        
        /* Tree Widget */
        QTreeWidget {{
            background-color: {cls.COLORS['surface']};
            alternate-background-color: {cls.COLORS['background']};
            selection-background-color: {cls.COLORS['selected']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 4px;
        }}
        
        QTreeWidget::item {{
            padding: 3px;
            border: none;
        }}
        
        QTreeWidget::item:selected {{
            background-color: {cls.COLORS['selected']};
        }}
        
        QTreeWidget::item:hover {{
            background-color: {cls.COLORS['hover']};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {cls.COLORS['border']};
            background-color: {cls.COLORS['surface']};
            border-radius: 4px;
        }}
        
        QTabBar::tab {{
            background-color: {cls.COLORS['background']};
            border: 1px solid {cls.COLORS['border']};
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {cls.COLORS['primary']};
            color: white;
        }}
        
        QTabBar::tab:hover {{
            background-color: {cls.COLORS['hover']};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 2px solid {cls.COLORS['border']};
            border-radius: 5px;
            text-align: center;
            background-color: {cls.COLORS['background']};
        }}
        
        QProgressBar::chunk {{
            background-color: {cls.COLORS['primary']};
            border-radius: 3px;
        }}
        
        /* Text Edit */
        QTextEdit {{
            border: 1px solid {cls.COLORS['border']};
            border-radius: 4px;
            background-color: {cls.COLORS['surface']};
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 10px;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text']};
            border-top: 1px solid {cls.COLORS['border']};
        }}
        
        QStatusBar::item {{
            border: none;
        }}
        
        /* Labels */
        QLabel {{
            color: {cls.COLORS['text']};
        }}
        
        /* Splitter */
        QSplitter::handle {{
            background-color: {cls.COLORS['border']};
        }}
        
        QSplitter::handle:horizontal {{
            width: 3px;
        }}
        
        QSplitter::handle:vertical {{
            height: 3px;
        }}
        
        /* Scroll Bars */
        QScrollBar:vertical {{
            background-color: {cls.COLORS['background']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.COLORS['text_secondary']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.COLORS['text']};
        }}
        
        QScrollBar:horizontal {{
            background-color: {cls.COLORS['background']};
            height: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {cls.COLORS['text_secondary']};
            border-radius: 6px;
            min-width: 20px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {cls.COLORS['text']};
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
