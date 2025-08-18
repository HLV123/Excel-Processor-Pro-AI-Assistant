import pandas as pd
from pathlib import Path
from typing import Optional
from exceptions import FileNotFoundError, DataProcessingError
from validators import DataValidator
from logger import Logger

logger = Logger().get_logger()

class DataLoader:
    
    @staticmethod
    def load_excel(file_path: Path) -> Optional[pd.DataFrame]:
        try:
            DataValidator.validate_file_path(file_path)
            
            df = pd.read_excel(file_path)
            logger.info(f"Successfully loaded data from {file_path}. Shape: {df.shape}")
            
            return df
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            raise DataProcessingError(f"Failed to load Excel file: {e}")
    
    @staticmethod
    def save_excel(df: pd.DataFrame, file_path: Path, sheet_name: str = "Sheet1") -> None:
        try:
            DataValidator.validate_dataframe(df)
            
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_excel(file_path, sheet_name=sheet_name, index=False)
            logger.info(f"Successfully saved data to {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving Excel file: {e}")
            raise DataProcessingError(f"Failed to save Excel file: {e}")