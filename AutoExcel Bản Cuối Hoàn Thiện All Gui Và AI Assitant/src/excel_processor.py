# File: src/excel_processor.py
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List
from data_loader import DataLoader
from data_processor import FlexibleDataProcessor
from chart_creator import FlexibleChartCreator
from ai_assistant_dialog import DataQualityAssessment
from config import Config
from exceptions import ExcelProcessorError
from validators import DataValidator
from logger import Logger

logger = Logger().get_logger()

class FlexibleExcelProcessor:
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.data_processor = FlexibleDataProcessor()
        self.chart_creator = FlexibleChartCreator()
        self.raw_data: Optional[pd.DataFrame] = None
        self.processed_data: Optional[pd.DataFrame] = None
        self.analyzed_data: Optional[pd.DataFrame] = None
        self.data_analysis: Optional[Dict[str, Any]] = None
    
    def load_data(self, file_path: Path) -> pd.DataFrame:
        try:
            self.raw_data = self.data_loader.load_excel(file_path)
            self.data_analysis = DataValidator.analyze_dataframe_structure(self.raw_data)
            logger.info(f"Data loaded and analyzed. Shape: {self.raw_data.shape}")
            return self.raw_data
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise ExcelProcessorError(f"Data loading failed: {e}")
    
    def preview_analysis(self, x_col: str, y_col: str, operation: str = "sum") -> Dict[str, Any]:
        try:
            if self.raw_data is None:
                raise ExcelProcessorError("No data loaded")
            
            quality_assessment = DataQualityAssessment.assess_data_quality(self.raw_data)
            
            basic_info = {
                'rows': len(self.raw_data),
                'columns': len(self.raw_data.columns),
                'x_column': x_col,
                'y_column': y_col,
                'operation': operation
            }
            
            column_compatibility = self._check_column_compatibility(x_col, y_col)
            estimated_results = self._estimate_results(x_col, y_col, operation)
            potential_issues = self._identify_potential_issues(x_col, y_col)
            
            return {
                'basic_info': basic_info,
                'quality_assessment': quality_assessment,
                'column_compatibility': column_compatibility,
                'estimated_results': estimated_results,
                'potential_issues': potential_issues,
                'recommended_strategy': self._suggest_strategy(quality_assessment, x_col, y_col)
            }
        except Exception as e:
            logger.error(f"Preview analysis failed: {e}")
            raise ExcelProcessorError(f"Preview analysis failed: {e}")
    
    def _check_column_compatibility(self, x_col: str, y_col: str) -> Dict[str, Any]:
        try:
            x_series = self.raw_data[x_col]
            y_series = self.raw_data[y_col]
            
            x_is_categorical = not pd.api.types.is_numeric_dtype(x_series)
            y_is_numeric = pd.api.types.is_numeric_dtype(y_series)
            
            compatibility_score = 0.8 if x_is_categorical and y_is_numeric else 0.5
            
            issues = []
            if not x_is_categorical:
                issues.append("Cột X nên là categorical để nhóm dữ liệu")
            if not y_is_numeric:
                issues.append("Cột Y nên là numeric để tính toán")
            
            return {
                'score': compatibility_score,
                'x_is_categorical': x_is_categorical,
                'y_is_numeric': y_is_numeric,
                'issues': issues,
                'suitable_for_analysis': len(issues) == 0
            }
        except Exception as e:
            return {'score': 0, 'issues': [f"Lỗi kiểm tra tương thích: {e}"]}
    
    def _estimate_results(self, x_col: str, y_col: str, operation: str) -> Dict[str, Any]:
        try:
            x_unique = self.raw_data[x_col].nunique()
            total_rows = len(self.raw_data)
            
            return {
                'categories': x_unique,
                'operation': operation,
                'data_points': total_rows,
                'chart_suitability': {
                    'bar': 'excellent' if x_unique <= 20 else 'good' if x_unique <= 50 else 'poor',
                    'pie': 'excellent' if x_unique <= 10 else 'poor',
                    'line': 'good' if x_unique <= 30 else 'poor'
                }
            }
        except Exception as e:
            return {'categories': 0, 'operation': operation, 'error': str(e)}
    
    def _identify_potential_issues(self, x_col: str, y_col: str) -> List[Dict[str, str]]:
        issues = []
        
        try:
            x_unique = self.raw_data[x_col].nunique()
            if x_unique > 50:
                issues.append({
                    'type': 'too_many_categories',
                    'message': f"Cột {x_col} có {x_unique} giá trị unique - biểu đồ có thể khó đọc"
                })
            
            y_non_numeric_count = 0
            try:
                pd.to_numeric(self.raw_data[y_col], errors='raise')
            except:
                y_non_numeric_count = self.raw_data[y_col].apply(
                    lambda x: pd.isna(pd.to_numeric(x, errors='coerce'))
                ).sum()
            
            if y_non_numeric_count > 0:
                issues.append({
                    'type': 'non_numeric_values',
                    'message': f"Cột {y_col} có {y_non_numeric_count} giá trị không phải số"
                })
            
        except Exception as e:
            issues.append({'type': 'analysis_error', 'message': f"Lỗi phân tích: {e}"})
        
        return issues
    
    def _suggest_strategy(self, quality_assessment: Dict, x_col: str, y_col: str) -> Dict[str, Any]:
        quality_score = quality_assessment.get('quality_score', 0)
        nan_percentage = quality_assessment.get('nan_percentage', 0)
        
        if quality_score > 0.8:
            strategy = 'proceed_immediately'
            message = "Dữ liệu chất lượng cao - có thể phân tích ngay"
        elif quality_score > 0.6:
            strategy = 'minor_cleaning'
            message = "Cần xử lý nhẹ trước khi phân tích"
        elif quality_score > 0.4:
            strategy = 'moderate_cleaning'
            message = "Cần xử lý dữ liệu kỹ lưỡng"
        else:
            strategy = 'major_cleaning'
            message = "Dữ liệu có nhiều vấn đề - cần xem xét kỹ"
        
        return {
            'strategy': strategy,
            'message': message,
            'confidence': quality_score,
            'auto_proceed': quality_score > 0.7
        }
    
    def process_data(self, x_col: str, y_col: str, operation: str = "sum", 
                    custom_strategy: Optional[Dict] = None) -> pd.DataFrame:
        try:
            if self.raw_data is None:
                raise ExcelProcessorError("No data loaded. Please load data first.")
            
            if custom_strategy:
                self.processed_data = self.data_processor.clean_data_with_strategy(
                    self.raw_data, custom_strategy
                )
            else:
                self.processed_data = self.data_processor.clean_data(self.raw_data)
            
            self.analyzed_data = self.data_processor.analyze_data_flexible(
                self.processed_data, x_col, y_col, operation
            )
            
            logger.info("Flexible data processing completed successfully")
            return self.analyzed_data
        
        except Exception as e:
            logger.error(f"Data processing failed: {e}")
            raise ExcelProcessorError(f"Data processing failed: {e}")
    
    def get_data_suggestions(self) -> Dict[str, Any]:
        if self.data_analysis:
            return self.data_processor.suggest_analysis_options(self.raw_data)
        return {"x_options": [], "y_options": [], "recommended_charts": []}
    
    def get_data_info(self) -> str:
        if self.raw_data is None:
            return "Chưa có dữ liệu được tải."
        
        info = f"📊 Thông tin tệp dữ liệu:\n"
        info += f"• Số dòng: {len(self.raw_data):,}\n"
        info += f"• Số cột: {len(self.raw_data.columns)}\n"
        info += f"• Các cột: {', '.join(self.raw_data.columns[:5])}"
        if len(self.raw_data.columns) > 5:
            info += f" (và {len(self.raw_data.columns) - 5} cột khác)"
        info += "\n\n"
        
        if self.data_analysis:
            info += f"🔍 Phân tích cấu trúc:\n"
            info += f"• Số cột số liệu: {len(self.data_analysis['numeric_columns'])}\n"
            info += f"• Số cột phân loại: {len(self.data_analysis['categorical_columns'])}\n"
            
            if self.data_analysis['suggested_x'] and self.data_analysis['suggested_y']:
                info += f"• Gợi ý X: {self.data_analysis['suggested_x']}\n"
                info += f"• Gợi ý Y: {self.data_analysis['suggested_y']}\n"
        
        if self.analyzed_data is not None:
            info += f"\n✅ Kết quả phân tích:\n"
            for _, row in self.analyzed_data.head(10).iterrows():
                info += f"• {row.iloc[0]}: {row.iloc[1]:,.0f}\n"
            if len(self.analyzed_data) > 10:
                info += f"... và {len(self.analyzed_data) - 10} mục khác\n"
        
        return info
    
    def get_summary_statistics(self) -> str:
        if self.processed_data is None:
            return "Chưa có dữ liệu được xử lý."
        
        try:
            summary_df = self.data_processor.get_summary_statistics(self.processed_data)
            return summary_df.to_string()
        except Exception as e:
            return f"Lỗi tạo thống kê: {e}"
    
    def save_processed_data(self, output_path: Optional[Path] = None) -> None:
        try:
            if self.analyzed_data is None:
                raise ExcelProcessorError("No processed data to save. Please process data first.")
            
            if output_path is None:
                output_path = Config.OUTPUT_FILE
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.data_loader.save_excel(self.analyzed_data, output_path, "Analysis_Results")
            logger.info(f"Processed data saved to {output_path}")
        
        except Exception as e:
            logger.error(f"Failed to save processed data: {e}")
            raise ExcelProcessorError(f"Saving processed data failed: {e}")
    
    def create_bar_chart(self, chart_config: Dict[str, str], output_path: Optional[Path] = None) -> Path:
        try:
            if self.analyzed_data is None:
                raise ExcelProcessorError("No analyzed data available. Please process data first.")
            
            if output_path is None:
                output_path = Config.CHART_DIR / "bar_chart.png"
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            x_col = self.analyzed_data.columns[0]
            y_col = self.analyzed_data.columns[1]
            
            self.chart_creator.create_bar_chart(
                self.analyzed_data,
                x_col, y_col,
                output_path,
                chart_config["title"],
                chart_config["xlabel"],
                chart_config["ylabel"]
            )
            
            logger.info(f"Bar chart created successfully: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Bar chart creation failed: {e}")
            raise ExcelProcessorError(f"Bar chart creation failed: {e}")
    
    def create_pie_chart(self, title: str, output_path: Optional[Path] = None) -> Path:
        try:
            if self.analyzed_data is None:
                raise ExcelProcessorError("No analyzed data available. Please process data first.")
            
            if output_path is None:
                output_path = Config.CHART_DIR / "pie_chart.png"
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            x_col = self.analyzed_data.columns[0]
            y_col = self.analyzed_data.columns[1]
            
            self.chart_creator.create_pie_chart(
                self.analyzed_data, x_col, y_col, output_path, title
            )
            logger.info(f"Pie chart created successfully: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Pie chart creation failed: {e}")
            raise ExcelProcessorError(f"Pie chart creation failed: {e}")
    
    def create_line_chart(self, chart_config: Dict[str, str], output_path: Optional[Path] = None) -> Path:
        try:
            if self.analyzed_data is None:
                raise ExcelProcessorError("No analyzed data available. Please process data first.")
            
            if output_path is None:
                output_path = Config.CHART_DIR / "line_chart.png"
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            x_col = self.analyzed_data.columns[0]
            y_col = self.analyzed_data.columns[1]
            
            self.chart_creator.create_line_chart(
                self.analyzed_data,
                x_col, y_col,
                output_path,
                chart_config["title"],
                chart_config["xlabel"],
                chart_config["ylabel"]
            )
            
            logger.info(f"Line chart created successfully: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Line chart creation failed: {e}")
            raise ExcelProcessorError(f"Line chart creation failed: {e}")
    
    def reset(self) -> None:
        self.raw_data = None
        self.processed_data = None
        self.analyzed_data = None
        self.data_analysis = None
        logger.info("Processor state reset")
    
    def is_ready_for_processing(self) -> bool:
        return self.raw_data is not None
    
    def is_ready_for_charting(self) -> bool:
        return self.analyzed_data is not None