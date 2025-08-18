"""
Excel Processor Pro - Advanced Excel Data Processing Application

A comprehensive Python application for processing Excel data with GUI interface,
advanced charting capabilities, and robust error handling.

Modules:
    config: Application configuration settings
    exceptions: Custom exception classes
    logger: Logging configuration and management
    validators: Data validation utilities
    data_loader: Excel file loading and saving
    data_processor: Data cleaning and analysis
    chart_creator: Chart generation utilities
    excel_processor: Main processing engine
    gui_components: GUI component classes
    gui_app: Main GUI application

Author: Excel Processor Pro Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Excel Processor Pro Team"
__email__ = "support@excelprocessorpro.com"
__license__ = "MIT"

from .config import Config
from .exceptions import (
    ExcelProcessorError,
    DataValidationError,
    FileNotFoundError,
    ChartCreationError,
    DataProcessingError,
    EmptyDataError,
    MissingColumnsError
)
from .logger import Logger
from .excel_processor import FlexibleExcelProcessor  # ← Giữ nguyên
from .gui_app import ExcelProcessorGUI  # ← Đổi tên class

__all__ = [
    "Config",
    "ExcelProcessorError",
    "DataValidationError", 
    "FileNotFoundError",
    "ChartCreationError",
    "DataProcessingError",
    "EmptyDataError",
    "MissingColumnsError",
    "Logger",
    "FlexibleExcelProcessor",  # ← Giữ nguyên
    "ExcelProcessorGUI",  # ← Đổi tên class
    "__version__",
    "__author__",
    "__email__",
    "__license__"
]

def get_version():
    """Return the current version of the package."""
    return __version__

def get_package_info():
    """Return package information as a dictionary."""
    return {
        "name": "Excel Processor Pro",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "description": "Advanced Excel data processing application with GUI"
    }