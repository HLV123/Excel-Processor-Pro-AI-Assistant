import pandas as pd
from typing import Optional, Dict, Any, Tuple
from exceptions import DataProcessingError, EmptyDataError
from validators import DataValidator
from config import Config
from logger import Logger

logger = Logger().get_logger()

class FlexibleDataProcessor:
    
    @staticmethod
    def analyze_nan_values(df: pd.DataFrame) -> Dict[str, Any]:
        """Phân tích chi tiết các giá trị NaN trong DataFrame"""
        try:
            nan_analysis = {
                "total_rows": len(df),
                "total_cells": df.size,
                "columns_with_nan": {},
                "total_nan_cells": 0,
                "nan_percentage": 0,
                "recommendations": {}
            }
            
            for col in df.columns:
                nan_count = df[col].isnull().sum()
                if nan_count > 0:
                    nan_percentage = (nan_count / len(df)) * 100
                    
                    # Phân tích kiểu dữ liệu và đưa ra gợi ý
                    if pd.api.types.is_numeric_dtype(df[col]):
                        # Tính toán các giá trị thống kê cho numeric
                        valid_data = df[col].dropna()
                        if len(valid_data) > 0:
                            suggestions = {
                                "mean": round(valid_data.mean(), 2),
                                "median": round(valid_data.median(), 2),
                                "mode": valid_data.mode().iloc[0] if not valid_data.mode().empty else 0,
                                "min": valid_data.min(),
                                "max": valid_data.max()
                            }
                        else:
                            suggestions = {"mean": 0, "median": 0, "mode": 0, "min": 0, "max": 0}
                        
                        nan_analysis["recommendations"][col] = {
                            "type": "numeric",
                            "suggestions": suggestions,
                            "recommended": "median"  # Median thường tốt hơn mean
                        }
                    else:
                        # Phân tích categorical
                        valid_data = df[col].dropna()
                        if len(valid_data) > 0:
                            mode_value = valid_data.mode().iloc[0] if not valid_data.mode().empty else "Unknown"
                            unique_count = valid_data.nunique()
                        else:
                            mode_value = "Unknown"
                            unique_count = 0
                        
                        nan_analysis["recommendations"][col] = {
                            "type": "categorical",
                            "mode": mode_value,
                            "unique_values": unique_count,
                            "recommended": "mode" if unique_count < 20 else "unknown"
                        }
                    
                    nan_analysis["columns_with_nan"][col] = {
                        "count": nan_count,
                        "percentage": round(nan_percentage, 2),
                        "dtype": str(df[col].dtype)
                    }
                    nan_analysis["total_nan_cells"] += nan_count
            
            nan_analysis["nan_percentage"] = round(
                (nan_analysis["total_nan_cells"] / nan_analysis["total_cells"]) * 100, 2
            )
            
            logger.info(f"NaN analysis completed: {nan_analysis['total_nan_cells']} NaN values found")
            return nan_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing NaN values: {e}")
            return {}
    
    @staticmethod
    def clean_data_with_strategy(df: pd.DataFrame, nan_strategy: Dict[str, Dict] = None) -> pd.DataFrame:
        """
        Làm sạch dữ liệu với chiến lược xử lý NaN tùy chỉnh
        
        nan_strategy format:
        {
            "column_name": {
                "method": "fill|drop|keep",
                "value": fill_value (nếu method="fill")
            }
        }
        """
        try:
            DataValidator.validate_dataframe(df)
            logger.info("Starting flexible data cleaning with NaN strategy")
            
            df_cleaned = df.copy()
            initial_rows = len(df_cleaned)
            
            # Phân tích NaN trước khi xử lý
            nan_analysis = FlexibleDataProcessor.analyze_nan_values(df_cleaned)
            
            if nan_strategy is None:
                # Sử dụng chiến lược mặc định thông minh
                nan_strategy = FlexibleDataProcessor._get_default_nan_strategy(df_cleaned, nan_analysis)
            
            # Áp dụng chiến lược cho từng cột
            for col in df_cleaned.columns:
                if col in nan_strategy:
                    strategy = nan_strategy[col]
                    method = strategy.get("method", "fill")
                    
                    if method == "fill":
                        fill_value = strategy.get("value")
                        if fill_value is None:
                            # Sử dụng giá trị được gợi ý
                            if col in nan_analysis.get("recommendations", {}):
                                rec = nan_analysis["recommendations"][col]
                                if rec["type"] == "numeric":
                                    fill_value = rec["suggestions"][rec["recommended"]]
                                else:
                                    fill_value = rec.get("mode", "Unknown")
                            else:
                                fill_value = 0 if pd.api.types.is_numeric_dtype(df_cleaned[col]) else "Unknown"
                        
                        null_count = df_cleaned[col].isnull().sum()
                        df_cleaned[col].fillna(fill_value, inplace=True)
                        if null_count > 0:
                            logger.info(f"Filled {null_count} NaN values in '{col}' with '{fill_value}'")
                    
                    elif method == "drop":
                        # Xóa các dòng có NaN trong cột này
                        before_count = len(df_cleaned)
                        df_cleaned = df_cleaned.dropna(subset=[col])
                        dropped_count = before_count - len(df_cleaned)
                        if dropped_count > 0:
                            logger.info(f"Dropped {dropped_count} rows with NaN in column '{col}'")
                    
                    elif method == "keep":
                        # Giữ nguyên NaN
                        logger.info(f"Keeping NaN values in column '{col}' as-is")
            
            # Xóa duplicates
            df_cleaned.drop_duplicates(inplace=True)
            final_rows = len(df_cleaned)
            
            logger.info(f"Data cleaning completed. Rows: {initial_rows} → {final_rows}")
            logger.info(f"Removed {initial_rows - final_rows} duplicate rows")
            
            return df_cleaned
            
        except Exception as e:
            logger.error(f"Error during advanced data cleaning: {e}")
            raise DataProcessingError(f"Advanced data cleaning failed: {e}")
    
    @staticmethod
    def _get_default_nan_strategy(df: pd.DataFrame, nan_analysis: Dict) -> Dict[str, Dict]:
        """Tạo chiến lược xử lý NaN mặc định thông minh"""
        strategy = {}
        
        for col in df.columns:
            if col in nan_analysis.get("columns_with_nan", {}):
                nan_info = nan_analysis["columns_with_nan"][col]
                recommendations = nan_analysis.get("recommendations", {}).get(col, {})
                
                # Quyết định dựa trên tỷ lệ NaN
                nan_percentage = nan_info["percentage"]
                
                if nan_percentage > 50:
                    # Quá nhiều NaN, có thể bỏ cột hoặc fill với giá trị mặc định
                    strategy[col] = {"method": "fill", "value": "N/A"}
                    logger.warning(f"Column '{col}' has {nan_percentage}% NaN values")
                
                elif nan_percentage > 20:
                    # Khá nhiều NaN, sử dụng giá trị thống kê
                    if recommendations.get("type") == "numeric":
                        recommended_value = recommendations["suggestions"][recommendations["recommended"]]
                        strategy[col] = {"method": "fill", "value": recommended_value}
                    else:
                        strategy[col] = {"method": "fill", "value": "Unknown"}
                
                else:
                    # Ít NaN, có thể xóa dòng hoặc fill
                    if recommendations.get("type") == "numeric":
                        recommended_value = recommendations["suggestions"][recommendations["recommended"]]
                        strategy[col] = {"method": "fill", "value": recommended_value}
                    else:
                        mode_value = recommendations.get("mode", "Unknown")
                        strategy[col] = {"method": "fill", "value": mode_value}
            
            else:
                # Không có NaN
                strategy[col] = {"method": "keep"}
        
        return strategy
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Phương thức cũ - tương thích ngược"""
        return FlexibleDataProcessor.clean_data_with_strategy(df)
    
    @staticmethod
    def analyze_data_flexible(df: pd.DataFrame, x_col: str, y_col: str, operation: str = "sum") -> pd.DataFrame:
        """Phân tích dữ liệu linh hoạt với xử lý NaN cải tiến"""
        try:
            DataValidator.validate_column_selection(df, x_col, y_col)
            logger.info(f"Starting flexible analysis: {x_col} vs {y_col} ({operation})")
            
            # Kiểm tra NaN trong các cột được chọn
            x_nan_count = df[x_col].isnull().sum()
            y_nan_count = df[y_col].isnull().sum()
            
            if x_nan_count > 0 or y_nan_count > 0:
                logger.warning(f"Found NaN values: {x_col}={x_nan_count}, {y_col}={y_nan_count}")
            
            # Xử lý NaN cho cột X (categorical)
            df_analysis = df.copy()
            if x_nan_count > 0:
                df_analysis[x_col] = df_analysis[x_col].fillna("Unknown")
                logger.info(f"Filled {x_nan_count} NaN values in X column '{x_col}' with 'Unknown'")
            
            # Xử lý NaN cho cột Y (numeric)
            if y_nan_count > 0:
                if not pd.api.types.is_numeric_dtype(df_analysis[y_col]):
                    df_analysis[y_col] = pd.to_numeric(df_analysis[y_col], errors='coerce')
                
                # Với các phép tính khác nhau, xử lý NaN khác nhau
                if operation in ["sum", "count"]:
                    # Sum và count: NaN = 0
                    df_analysis[y_col] = df_analysis[y_col].fillna(0)
                    logger.info(f"Filled {y_nan_count} NaN values in Y column '{y_col}' with 0 for {operation}")
                else:
                    # Mean, max, min: bỏ qua NaN
                    logger.info(f"Will ignore NaN values in Y column '{y_col}' for {operation}")
            
            # Convert y_col to numeric if not already
            if not pd.api.types.is_numeric_dtype(df_analysis[y_col]):
                df_analysis[y_col] = pd.to_numeric(df_analysis[y_col], errors='coerce').fillna(0)
            
            # Group by x_col and aggregate y_col
            if operation == "sum":
                result = df_analysis.groupby(x_col)[y_col].sum().reset_index()
            elif operation == "mean":
                result = df_analysis.groupby(x_col)[y_col].mean().reset_index()
            elif operation == "count":
                result = df_analysis.groupby(x_col)[y_col].count().reset_index()
            elif operation == "max":
                result = df_analysis.groupby(x_col)[y_col].max().reset_index()
            elif operation == "min":
                result = df_analysis.groupby(x_col)[y_col].min().reset_index()
            else:
                result = df_analysis.groupby(x_col)[y_col].sum().reset_index()
            
            # Sort by values descending
            result = result.sort_values(y_col, ascending=False)
            
            if result.empty:
                raise EmptyDataError("Analysis resulted in empty dataset")
            
            logger.info(f"Analysis completed. Found {len(result)} categories")
            for _, row in result.head(10).iterrows():  # Log top 10
                logger.info(f"Category: {row[x_col]}, Value: {row[y_col]:,.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error during flexible analysis: {e}")
            raise DataProcessingError(f"Flexible analysis failed: {e}")
    
    @staticmethod
    def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
        """Tạo thống kê tóm tắt với thông tin NaN chi tiết"""
        try:
            DataValidator.validate_dataframe(df)
            
            summary_data = []
            
            for col in df.columns:
                null_count = df[col].isnull().sum()
                null_percentage = round((null_count / len(df)) * 100, 2)
                
                col_info = {
                    "Column": col,
                    "Type": str(df[col].dtype),
                    "Count": len(df[col]),
                    "Null_Count": null_count,
                    "Null_Percentage": f"{null_percentage}%",
                    "Unique_Values": df[col].nunique(),
                    "Memory_Usage": f"{df[col].memory_usage(deep=True)} bytes"
                }
                
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Thống kê cho cột số (bỏ qua NaN)
                    valid_data = df[col].dropna()
                    if len(valid_data) > 0:
                        col_info.update({
                            "Mean": round(valid_data.mean(), 2),
                            "Std": round(valid_data.std(), 2),
                            "Min": valid_data.min(),
                            "25%": round(valid_data.quantile(0.25), 2),
                            "Median": round(valid_data.median(), 2),
                            "75%": round(valid_data.quantile(0.75), 2),
                            "Max": valid_data.max(),
                            "Zero_Count": (valid_data == 0).sum()
                        })
                    else:
                        col_info.update({
                            "Mean": "N/A", "Std": "N/A", "Min": "N/A", 
                            "Median": "N/A", "Max": "N/A", "Zero_Count": 0
                        })
                else:
                    # Thống kê cho cột categorical
                    valid_data = df[col].dropna()
                    if len(valid_data) > 0:
                        mode_value = valid_data.mode().iloc[0] if not valid_data.mode().empty else "N/A"
                        most_common_count = valid_data.value_counts().iloc[0] if len(valid_data.value_counts()) > 0 else 0
                        
                        col_info.update({
                            "Most_Common": str(mode_value)[:50],  # Truncate long strings
                            "Most_Common_Count": most_common_count,
                            "Most_Common_Pct": round((most_common_count / len(valid_data)) * 100, 2),
                            "Avg_Length": round(valid_data.astype(str).str.len().mean(), 1),
                            "Empty_Strings": (valid_data == "").sum()
                        })
                    else:
                        col_info.update({
                            "Most_Common": "N/A", "Most_Common_Count": 0,
                            "Most_Common_Pct": 0, "Avg_Length": 0, "Empty_Strings": 0
                        })
                
                summary_data.append(col_info)
            
            summary = pd.DataFrame(summary_data)
            logger.info("Generated comprehensive summary statistics with NaN analysis")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary statistics: {e}")
            raise DataProcessingError(f"Summary statistics generation failed: {e}")
    
    @staticmethod
    def suggest_analysis_options(df: pd.DataFrame) -> Dict[str, Any]:
        """Gợi ý tùy chọn phân tích tốt nhất dựa trên cấu trúc dữ liệu"""
        try:
            analysis = DataValidator.analyze_dataframe_structure(df)
            nan_analysis = FlexibleDataProcessor.analyze_nan_values(df)
            
            suggestions = {
                "recommended_charts": [],
                "x_options": [],
                "y_options": [],
                "operations": ["sum", "mean", "count", "max", "min"],
                "nan_info": nan_analysis,
                "warnings": []
            }
            
            # Cảnh báo về NaN
            if nan_analysis.get("total_nan_cells", 0) > 0:
                suggestions["warnings"].append(
                    f"⚠️ Phát hiện {nan_analysis['total_nan_cells']} ô trống ({nan_analysis['nan_percentage']}%)"
                )
            
            # Lọc các cột có quá nhiều NaN
            columns_with_high_nan = []
            for col, info in nan_analysis.get("columns_with_nan", {}).items():
                if info["percentage"] > 50:
                    columns_with_high_nan.append(col)
                    suggestions["warnings"].append(f"⚠️ Cột '{col}' có {info['percentage']}% giá trị trống")
            
            # Add columns as options (exclude high NaN columns for better results)
            available_categorical = [col for col in analysis["categorical_columns"] if col not in columns_with_high_nan]
            available_numeric = [col for col in analysis["numeric_columns"] if col not in columns_with_high_nan]
            
            suggestions["x_options"] = available_categorical if available_categorical else list(df.columns)
            suggestions["y_options"] = available_numeric if available_numeric else list(df.columns)
            
            # Recommend chart types
            if available_categorical and available_numeric:
                suggestions["recommended_charts"] = ["Bar Chart", "Pie Chart", "Line Chart"]
            elif len(df.columns) >= 2:
                suggestions["recommended_charts"] = ["Bar Chart"]
            
            logger.info(f"Generated analysis suggestions with NaN considerations: {suggestions}")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return {
                "recommended_charts": [], 
                "x_options": [], 
                "y_options": [], 
                "operations": ["sum"],
                "nan_info": {},
                "warnings": ["❌ Lỗi phân tích dữ liệu"]
            }