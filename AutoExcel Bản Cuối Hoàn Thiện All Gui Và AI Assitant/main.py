# File: main.py
#!/usr/bin/env python3

import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import Config
from src.gui_app import ExcelProcessorGUI
from src.logger import Logger
from src.exceptions import ExcelProcessorError

def setup_environment():
    try:
        Config.setup_directories()
        logger = Logger().get_logger()
        logger.info("="*50)
        logger.info("Excel Processor Pro - AI Assistant Starting")
        logger.info(f"Version: {get_version()}")
        logger.info("="*50)
        return logger
    except Exception as e:
        print(f"Failed to setup environment: {e}")
        sys.exit(1)

def get_version():
    try:
        from src import __version__
        return __version__
    except ImportError:
        return "2.0.0-AI"

def main():
    logger = setup_environment()
    
    try:
        app = ExcelProcessorGUI()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except ExcelProcessorError as e:
        logger.error(f"Application error: {e}")
        print(f"Application Error: {e}")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        logger.critical(traceback.format_exc())
        print(f"Unexpected Error: {e}")
        print("Check log file for details.")
    finally:
        logger.info("AI Assistant application shutdown complete")

if __name__ == "__main__":
    main()