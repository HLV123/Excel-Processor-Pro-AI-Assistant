import pandas as pd
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from exceptions import DataValidationError, EmptyDataError, MissingColumnsError
from config import Config
from logger import Logger

logger = Logger().get_logger()

class DataValidator:
    
    @staticmethod
    def validate_file_path(file_path: Path) -> None:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.suffix.lower() in ['.xlsx', '.xls']:
            raise DataValidationError(f"Invalid file format: {file_path.suffix}")
        
        logger.info(f"File validation passed: {file_path}")
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: Optional[List[str]] = None) -> None:
        if df is None:
            raise EmptyDataError("DataFrame is None")
        
        if df.empty:
            raise EmptyDataError("DataFrame is empty")
        
        # Flexible validation - only check if required_columns specified
        if required_columns:
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise MissingColumnsError(f"Missing required columns: {missing_columns}")
        
        logger.info(f"DataFrame validation passed. Shape: {df.shape}, Columns: {list(df.columns)}")
    
    @staticmethod
    def analyze_dataframe_structure(df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze DataFrame to suggest best columns for visualization"""
        analysis = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "numeric_columns": [],
            "categorical_columns": [],
            "suggested_x": None,
            "suggested_y": None,
            "data_types": {}
        }
        
        for col in df.columns:
            dtype = df[col].dtype
            analysis["data_types"][col] = str(dtype)
            
            # Check if numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                analysis["numeric_columns"].append(col)
            else:
                # Check if categorical (string/object with limited unique values)
                unique_count = df[col].nunique()
                if unique_count <= len(df) * 0.5:  # Less than 50% unique values
                    analysis["categorical_columns"].append(col)
        
        # Auto-suggest best columns for charts
        if analysis["categorical_columns"] and analysis["numeric_columns"]:
            analysis["suggested_x"] = analysis["categorical_columns"][0]
            analysis["suggested_y"] = analysis["numeric_columns"][0]
        elif len(df.columns) >= 2:
            analysis["suggested_x"] = df.columns[0]
            analysis["suggested_y"] = df.columns[1]
        
        logger.info(f"DataFrame analysis: {analysis}")
        return analysis
    
    @staticmethod
    def validate_chart_input(title: str, xlabel: str, ylabel: str) -> None:
        if not title or not title.strip():
            raise DataValidationError("Chart title cannot be empty")
        
        if not xlabel or not xlabel.strip():
            raise DataValidationError("X-axis label cannot be empty")
        
        if not ylabel or not ylabel.strip():
            raise DataValidationError("Y-axis label cannot be empty")
        
        for label in [title, xlabel, ylabel]:
            if len(label.strip()) > 100:
                raise DataValidationError("Chart labels must be less than 100 characters")
        
        logger.info("Chart input validation passed")
    
    @staticmethod
    def validate_column_selection(df: pd.DataFrame, x_col: str, y_col: str) -> None:
        """Validate that selected columns exist and are suitable for charting"""
        if x_col not in df.columns:
            raise DataValidationError(f"X-axis column '{x_col}' not found in data")
        
        if y_col not in df.columns:
            raise DataValidationError(f"Y-axis column '{y_col}' not found in data")
        
        # Check if y_col is numeric for aggregation
        if not pd.api.types.is_numeric_dtype(df[y_col]):
            # Try to convert to numeric
            try:
                pd.to_numeric(df[y_col], errors='coerce')
            except:
                raise DataValidationError(f"Y-axis column '{y_col}' cannot be converted to numeric values")
        
        logger.info(f"Column selection validation passed: X='{x_col}', Y='{y_col}'")