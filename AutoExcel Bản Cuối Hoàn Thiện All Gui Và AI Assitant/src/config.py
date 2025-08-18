from pathlib import Path
from typing import Dict, Any
import logging

class Config:
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"  # src/data/
    LOGS_DIR = BASE_DIR.parent / "logs"  # project_root/logs/
    
    # Output files in src/data/
    OUTPUT_FILE = DATA_DIR / "processed_data.xlsx"
    CHART_DIR = DATA_DIR / "charts"
    
    # Flexible column mapping - no required columns
    DEFAULT_CHART_DEFAULTS: Dict[str, Any] = {
        "title": "Biểu đồ dữ liệu",
        "xlabel": "Danh mục", 
        "ylabel": "Giá trị",
        "figsize": (10, 6),
        "dpi": 300,
        "color": "steelblue"
    }
    
    LOG_CONFIG = {
        "level": logging.INFO,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "filename": LOGS_DIR / "app.log"
    }
    
    @classmethod
    def setup_directories(cls) -> None:
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.CHART_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)