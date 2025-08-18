# File: src/ai_assistant_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Optional, Callable
import pandas as pd

class DataQualityAssessment:
    
    @staticmethod
    def assess_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
        total_cells = df.size
        total_nan = df.isnull().sum().sum()
        nan_percentage = (total_nan / total_cells) * 100 if total_cells > 0 else 0
        
        column_analysis = {}
        overall_issues = []
        
        for col in df.columns:
            col_analysis = DataQualityAssessment._analyze_column(df[col], col)
            column_analysis[col] = col_analysis
            if col_analysis['issues']:
                overall_issues.extend(col_analysis['issues'])
        
        quality_score = DataQualityAssessment._calculate_quality_score(nan_percentage, overall_issues, df)
        outliers = DataQualityAssessment._detect_outliers(df)
        
        return {
            'quality_score': quality_score,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'total_nan_cells': total_nan,
            'nan_percentage': round(nan_percentage, 2),
            'column_analysis': column_analysis,
            'outliers': outliers,
            'overall_issues': overall_issues,
            'recommendations': DataQualityAssessment._generate_recommendations(nan_percentage, column_analysis, outliers)
        }
    
    @staticmethod
    def _analyze_column(series: pd.Series, col_name: str) -> Dict[str, Any]:
        total_count = len(series)
        null_count = series.isnull().sum()
        null_percentage = (null_count / total_count) * 100 if total_count > 0 else 0
        
        issues = []
        suggestions = {}
        
        if pd.api.types.is_numeric_dtype(series):
            data_type = "numeric"
            valid_data = series.dropna()
            
            if len(valid_data) > 0:
                suggestions = {
                    'mean': round(valid_data.mean(), 2),
                    'median': round(valid_data.median(), 2),
                    'mode': valid_data.mode().iloc[0] if not valid_data.mode().empty else 0,
                    'std': round(valid_data.std(), 2)
                }
                
                q1 = valid_data.quantile(0.25)
                q3 = valid_data.quantile(0.75)
                iqr = q3 - q1
                outlier_count = ((valid_data < (q1 - 1.5 * iqr)) | (valid_data > (q3 + 1.5 * iqr))).sum()
                
                if outlier_count > 0:
                    issues.append({
                        'type': 'outliers',
                        'severity': 'medium' if outlier_count <= 5 else 'high',
                        'count': outlier_count,
                        'message': f"{outlier_count} giá trị bất thường"
                    })
        else:
            data_type = "categorical"
            valid_data = series.dropna()
            
            if len(valid_data) > 0:
                value_counts = valid_data.value_counts()
                mode_value = value_counts.index[0] if len(value_counts) > 0 else "Unknown"
                
                suggestions = {
                    'mode': mode_value,
                    'unique_count': valid_data.nunique(),
                    'most_common_count': value_counts.iloc[0] if len(value_counts) > 0 else 0
                }
        
        if null_percentage > 50:
            issues.append({
                'type': 'high_missing',
                'severity': 'critical',
                'percentage': null_percentage,
                'message': f"Thiếu {null_percentage:.1f}% dữ liệu - nghiêm trọng!"
            })
        elif null_percentage > 20:
            issues.append({
                'type': 'medium_missing',
                'severity': 'medium',
                'percentage': null_percentage,
                'message': f"Thiếu {null_percentage:.1f}% dữ liệu - cần xử lý"
            })
        elif null_percentage > 0:
            issues.append({
                'type': 'low_missing',
                'severity': 'low',
                'percentage': null_percentage,
                'message': f"Thiếu {null_percentage:.1f}% dữ liệu - ít"
            })
        
        return {
            'data_type': data_type,
            'null_count': null_count,
            'null_percentage': round(null_percentage, 2),
            'suggestions': suggestions,
            'issues': issues
        }
    
    @staticmethod
    def _calculate_quality_score(nan_percentage: float, issues: List[Dict], df: pd.DataFrame) -> float:
        base_score = 1.0
        
        if nan_percentage > 50:
            base_score -= 0.5
        elif nan_percentage > 20:
            base_score -= 0.3
        elif nan_percentage > 5:
            base_score -= 0.1
        
        critical_issues = len([i for i in issues if i.get('severity') == 'critical'])
        medium_issues = len([i for i in issues if i.get('severity') == 'medium'])
        
        base_score -= critical_issues * 0.2
        base_score -= medium_issues * 0.1
        
        if len(df) > 1000:
            base_score += 0.05
        if len(df.columns) > 5:
            base_score += 0.05
        
        return max(0.0, min(1.0, base_score))
    
    @staticmethod
    def _detect_outliers(df: pd.DataFrame) -> Dict[str, List]:
        outliers = {}
        
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                series = df[col].dropna()
                if len(series) > 0:
                    q1 = series.quantile(0.25)
                    q3 = series.quantile(0.75)
                    iqr = q3 - q1
                    
                    outlier_values = series[
                        (series < (q1 - 1.5 * iqr)) | (series > (q3 + 1.5 * iqr))
                    ].tolist()
                    
                    if outlier_values:
                        outliers[col] = outlier_values[:5]
        
        return outliers
    
    @staticmethod
    def _generate_recommendations(nan_percentage: float, column_analysis: Dict, outliers: Dict) -> List[Dict]:
        recommendations = []
        
        if nan_percentage > 50:
            recommendations.append({
                'type': 'data_quality',
                'priority': 'critical',
                'action': 'review_data_source',
                'title': 'Kiểm tra lại nguồn dữ liệu',
                'description': 'Dữ liệu thiếu quá nhiều (>50%). Nên kiểm tra lại file gốc.',
                'confidence': 0.9
            })
        elif nan_percentage > 20:
            recommendations.append({
                'type': 'nan_handling',
                'priority': 'high',
                'action': 'statistical_imputation',
                'title': 'Sử dụng phương pháp thống kê',
                'description': 'Điền giá trị thiếu bằng median/mode để tránh bias.',
                'confidence': 0.8
            })
        elif nan_percentage > 0:
            recommendations.append({
                'type': 'nan_handling',
                'priority': 'medium',
                'action': 'conservative_fill',
                'title': 'Điền giá trị an toàn',
                'description': 'Dữ liệu khá sạch, có thể điền giá trị trung bình.',
                'confidence': 0.85
            })
        
        if outliers:
            recommendations.append({
                'type': 'outlier_handling',
                'priority': 'medium',
                'action': 'investigate_outliers',
                'title': 'Kiểm tra giá trị bất thường',
                'description': f'Phát hiện outliers trong {len(outliers)} cột. Có thể là lỗi nhập liệu.',
                'confidence': 0.7
            })
        
        return recommendations


class IntelligentAnalysisDialog:
    
    def __init__(self, parent: tk.Widget, analysis_preview: Dict[str, Any], 
                 on_proceed: Callable = None, on_customize: Callable = None):
        
        self.parent = parent
        self.analysis_preview = analysis_preview
        self.on_proceed = on_proceed
        self.on_customize = on_customize
        
        self.dialog = None
        self.result = None
        self.selected_strategy = {}
        
    def show(self) -> str:
        self._create_dialog()
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self.dialog.geometry("800x700")
        self._center_dialog()
        
        self.parent.wait_window(self.dialog)
        
        return self.result
    
    def _create_dialog(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("🤖 AI Assistant - Phân tích thông minh")
        self.dialog.resizable(True, True)
        
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._create_header(main_frame)
        self._create_content_notebook(main_frame)
        self._create_action_buttons(main_frame)
    
    def _create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        avatar_frame = ttk.Frame(header_frame)
        avatar_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        avatar_label = ttk.Label(avatar_frame, text="🤖", font=("Arial", 48))
        avatar_label.pack()
        
        status_label = ttk.Label(avatar_frame, text="AI Assistant", 
                               font=("Arial", 10, "bold"), foreground="blue")
        status_label.pack()
        
        greeting_frame = ttk.Frame(header_frame)
        greeting_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        quality_score = self.analysis_preview.get('quality_assessment', {}).get('quality_score', 0)
        
        if quality_score > 0.8:
            greeting = "🎉 Tuyệt vời! Tôi đã phân tích dữ liệu của bạn và có tin tốt..."
            color = "darkgreen"
        elif quality_score > 0.6:
            greeting = "🔍 Tôi đã phân tích dữ liệu và có một số phát hiện thú vị..."
            color = "blue"
        else:
            greeting = "⚠️ Tôi đã phân tích dữ liệu và phát hiện một số vấn đề cần lưu ý..."
            color = "darkorange"
        
        greeting_label = ttk.Label(
            greeting_frame,
            text=greeting,
            font=("Arial", 14, "bold"),
            foreground=color,
            wraplength=500
        )
        greeting_label.pack(anchor=tk.W)
        
        data_info = self.analysis_preview.get('basic_info', {})
        info_text = f"📊 {data_info.get('rows', 0)} dòng, {data_info.get('columns', 0)} cột | " \
                   f"🎯 Phân tích: {data_info.get('x_column', '')} vs {data_info.get('y_column', '')}"
        
        info_label = ttk.Label(
            greeting_frame,
            text=info_text,
            font=("Arial", 10),
            foreground="gray"
        )
        info_label.pack(anchor=tk.W, pady=(5, 0))
    
    def _create_content_notebook(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self._create_findings_tab()
        self._create_recommendations_tab()
        self._create_preview_tab()
    
    def _create_findings_tab(self):
        findings_frame = ttk.Frame(self.notebook)
        self.notebook.add(findings_frame, text="🔍 Phát hiện")
        
        canvas = tk.Canvas(findings_frame)
        scrollbar = ttk.Scrollbar(findings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        quality_assessment = self.analysis_preview.get('quality_assessment', {})
        
        quality_score = quality_assessment.get('quality_score', 0)
        score_frame = ttk.LabelFrame(scrollable_frame, text="📊 Điểm chất lượng dữ liệu", padding=10)
        score_frame.pack(fill=tk.X, padx=10, pady=5)
        
        score_color = "green" if quality_score > 0.8 else "orange" if quality_score > 0.6 else "red"
        score_text = f"{quality_score:.1%}"
        
        score_label = ttk.Label(score_frame, text=f"Điểm số: {score_text}", 
                              font=("Arial", 14, "bold"), foreground=score_color)
        score_label.pack(anchor=tk.W)
        
        overall_issues = quality_assessment.get('overall_issues', [])
        if overall_issues:
            issues_frame = ttk.LabelFrame(scrollable_frame, text="⚠️ Vấn đề phát hiện", padding=10)
            issues_frame.pack(fill=tk.X, padx=10, pady=5)
            
            for issue in overall_issues[:5]:
                self._create_issue_widget(issues_frame, issue)
        
        nan_info = quality_assessment
        if nan_info.get('total_nan_cells', 0) > 0:
            nan_frame = ttk.LabelFrame(scrollable_frame, text="🔍 Phân tích dữ liệu thiếu", padding=10)
            nan_frame.pack(fill=tk.X, padx=10, pady=5)
            
            nan_text = f"Tổng ô trống: {nan_info.get('total_nan_cells', 0):,} " \
                      f"({nan_info.get('nan_percentage', 0):.1f}%)"
            ttk.Label(nan_frame, text=nan_text, font=("Arial", 11)).pack(anchor=tk.W)
        
        outliers = quality_assessment.get('outliers', {})
        if outliers:
            outlier_frame = ttk.LabelFrame(scrollable_frame, text="📈 Giá trị bất thường", padding=10)
            outlier_frame.pack(fill=tk.X, padx=10, pady=5)
            
            for col, values in outliers.items():
                outlier_text = f"{col}: {values[:3]}..."
                ttk.Label(outlier_frame, text=outlier_text, font=("Arial", 10)).pack(anchor=tk.W)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_issue_widget(self, parent, issue):
        issue_frame = ttk.Frame(parent)
        issue_frame.pack(fill=tk.X, pady=2)
        
        severity_colors = {'critical': 'red', 'medium': 'orange', 'low': 'blue'}
        severity_icons = {'critical': '🔴', 'medium': '🟡', 'low': '🔵'}
        
        severity = issue.get('severity', 'low')
        icon = severity_icons.get(severity, '🔵')
        color = severity_colors.get(severity, 'blue')
        
        icon_label = ttk.Label(issue_frame, text=icon, font=("Arial", 12))
        icon_label.pack(side=tk.LEFT, padx=(0, 5))
        
        message_label = ttk.Label(issue_frame, text=issue.get('message', ''), 
                                font=("Arial", 10), foreground=color)
        message_label.pack(side=tk.LEFT)
    
    def _create_recommendations_tab(self):
        rec_frame = ttk.Frame(self.notebook)
        self.notebook.add(rec_frame, text="💡 Khuyến nghị")
        
        canvas = tk.Canvas(rec_frame)
        scrollbar = ttk.Scrollbar(rec_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        recommendations = self.analysis_preview.get('quality_assessment', {}).get('recommendations', [])
        
        for i, rec in enumerate(recommendations):
            rec_widget = ttk.LabelFrame(scrollable_frame, text=f"{rec.get('title', '')}", padding=10)
            rec_widget.pack(fill=tk.X, padx=10, pady=5)
            
            priority_colors = {'critical': 'red', 'high': 'orange', 'medium': 'blue', 'low': 'green'}
            priority = rec.get('priority', 'medium')
            color = priority_colors.get(priority, 'blue')
            
            priority_label = ttk.Label(rec_widget, text=f"Mức độ: {priority.upper()}", 
                                     font=("Arial", 9, "bold"), foreground=color)
            priority_label.pack(anchor=tk.W)
            
            desc_label = ttk.Label(rec_widget, text=rec.get('description', ''), 
                                 font=("Arial", 10), wraplength=600)
            desc_label.pack(anchor=tk.W, pady=(5, 0))
            
            confidence = rec.get('confidence', 0)
            conf_label = ttk.Label(rec_widget, text=f"Độ tin cậy: {confidence:.0%}", 
                                 font=("Arial", 9), foreground="gray")
            conf_label.pack(anchor=tk.W, pady=(5, 0))
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_preview_tab(self):
        preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(preview_frame, text="👁️ Xem trước")
        
        preview_info = self.analysis_preview.get('estimated_results', {})
        
        info_frame = ttk.LabelFrame(preview_frame, text="📊 Dự kiến kết quả", padding=15)
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        estimated_categories = preview_info.get('categories', 0)
        estimated_operation = preview_info.get('operation', 'sum')
        
        result_text = f"Số danh mục dự kiến: {estimated_categories}\n" \
                     f"Phép tính: {estimated_operation}\n" \
                     f"Loại biểu đồ phù hợp: Bar Chart, Pie Chart"
        
        ttk.Label(info_frame, text=result_text, font=("Arial", 11)).pack(anchor=tk.W)
        
        strategy_frame = ttk.LabelFrame(preview_frame, text="🔧 Chiến lược xử lý", padding=15)
        strategy_frame.pack(fill=tk.X, padx=20, pady=10)
        
        strategy_text = self._generate_strategy_text()
        ttk.Label(strategy_frame, text=strategy_text, font=("Arial", 10), wraplength=700).pack(anchor=tk.W)
    
    def _generate_strategy_text(self) -> str:
        quality_assessment = self.analysis_preview.get('quality_assessment', {})
        nan_percentage = quality_assessment.get('nan_percentage', 0)
        
        if nan_percentage > 50:
            return "🔴 Chiến lược: Điền 'N/A' cho dữ liệu thiếu vì tỷ lệ thiếu quá cao.\n" \
                   "⚠️ Cảnh báo: Kết quả có thể không chính xác do chất lượng dữ liệu thấp."
        elif nan_percentage > 20:
            return "🟡 Chiến lược: Sử dụng phương pháp thống kê (median/mode) để điền dữ liệu thiếu.\n" \
                   "📊 Phương pháp này giúp giữ được tính chính xác của phân tích."
        elif nan_percentage > 0:
            return "🟢 Chiến lược: Điền giá trị an toàn (median/mode) cho số ít dữ liệu thiếu.\n" \
                   "✅ Dữ liệu có chất lượng tốt, kết quả sẽ đáng tin cậy."
        else:
            return "✨ Chiến lược: Không cần xử lý - dữ liệu hoàn hảo!\n" \
                   "🎯 Có thể tiến hành phân tích ngay lập tức."
    
    def _create_action_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        left_frame = ttk.Frame(button_frame)
        left_frame.pack(side=tk.LEFT)
        
        right_frame = ttk.Frame(button_frame)
        right_frame.pack(side=tk.RIGHT)
        
        quality_score = self.analysis_preview.get('quality_assessment', {}).get('quality_score', 0)
        
        if quality_score > 0.5:
            proceed_btn = ttk.Button(
                right_frame,
                text="🚀 Tiến hành phân tích",
                command=self._on_proceed_clicked,
                style="Accent.TButton"
            )
            proceed_btn.pack(side=tk.RIGHT, padx=(10, 0))
        else:
            warning_btn = ttk.Button(
                right_frame,
                text="⚠️ Vẫn tiếp tục (không khuyến nghị)",
                command=self._on_force_proceed,
                style="Accent.TButton"
            )
            warning_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        customize_btn = ttk.Button(
            right_frame,
            text="⚙️ Tùy chỉnh",
            command=self._on_customize_clicked
        )
        customize_btn.pack(side=tk.RIGHT)
        
        cancel_btn = ttk.Button(
            left_frame,
            text="❌ Hủy",
            command=self._on_cancel_clicked
        )
        cancel_btn.pack(side=tk.LEFT)
        
        help_btn = ttk.Button(
            left_frame,
            text="❓ Trợ giúp",
            command=self._show_help
        )
        help_btn.pack(side=tk.LEFT, padx=(10, 0))
    
    def _on_proceed_clicked(self):
        self.result = "proceed"
        self.dialog.destroy()
    
    def _on_force_proceed(self):
        result = messagebox.askyesno(
            "Xác nhận",
            "Dữ liệu có chất lượng thấp. Kết quả phân tích có thể không chính xác.\n\n"
            "Bạn có chắc chắn muốn tiếp tục?"
        )
        if result:
            self.result = "force_proceed"
            self.dialog.destroy()
    
    def _on_customize_clicked(self):
        self.result = "customize"
        self.dialog.destroy()
    
    def _on_cancel_clicked(self):
        self.result = "cancel"
        self.dialog.destroy()
    
    def _show_help(self):
        help_text = """
🤖 AI Assistant Hướng dẫn:

🔍 Tab Phát hiện:
- Hiển thị điểm chất lượng dữ liệu (0-100%)
- Liệt kê các vấn đề được phát hiện
- Phân tích dữ liệu thiếu và giá trị bất thường

💡 Tab Khuyến nghị:
- Đưa ra các gợi ý xử lý dữ liệu
- Mức độ ưu tiên và độ tin cậy
- Giải thích lý do cho từng khuyến nghị

👁️ Tab Xem trước:
- Dự đoán kết quả phân tích
- Chiến lược xử lý sẽ áp dụng
- Loại biểu đồ phù hợp

🚀 Tiến hành: Áp dụng chiến lược tự động
⚙️ Tùy chỉnh: Điều chỉnh thủ công
❌ Hủy: Quay lại màn hình chính
        """
        
        messagebox.showinfo("Trợ giúp", help_text)
    
    def _center_dialog(self):
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")