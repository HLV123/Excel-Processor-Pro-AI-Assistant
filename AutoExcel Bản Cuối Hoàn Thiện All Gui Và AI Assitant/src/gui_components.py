# File: src/gui_components.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable, Dict, Any, List, Optional
from pathlib import Path
import pandas as pd
from config import Config
from logger import Logger

logger = Logger().get_logger()

class ModernStatusBar:
    
    def __init__(self, parent: tk.Widget):
        self.frame = ttk.Frame(parent)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        
        self.status_frame = ttk.Frame(self.frame)
        self.status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
        
        self.status_icon = ttk.Label(
            self.status_frame, 
            text="●", 
            foreground="green", 
            font=("Arial", 12, "bold")
        )
        self.status_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.label = ttk.Label(
            self.status_frame, 
            text="Sẵn sàng...", 
            font=("Arial", 10)
        )
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress = ttk.Progressbar(
            self.frame, 
            mode='indeterminate', 
            length=200
        )
        self.progress.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def set_status(self, message: str, status_type: str = "ready", show_progress: bool = False):
        colors = {
            "ready": "green", 
            "working": "blue", 
            "error": "red", 
            "success": "darkgreen",
            "warning": "orange"
        }
        
        self.status_icon.config(foreground=colors.get(status_type, "green"))
        self.label.config(text=message)
        
        if show_progress:
            self.progress.start(10)
        else:
            self.progress.stop()

class FileSelectionFrame:
    
    def __init__(self, parent: tk.Widget, on_file_selected: Callable[[str], None]):
        self.frame = ttk.LabelFrame(parent, text="📁 Chọn tệp dữ liệu Excel", padding=10)
        self.frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.file_path_var = tk.StringVar(value="Chưa chọn tệp...")
        self.on_file_selected = on_file_selected
        
        self._create_widgets()
    
    def _create_widgets(self):
        file_row = ttk.Frame(self.frame)
        file_row.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_row, text="Tệp Excel:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, pady=2)
        
        self.entry = ttk.Entry(
            file_row, 
            textvariable=self.file_path_var, 
            state="readonly", 
            width=70,
            font=("Arial", 9)
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10), pady=2)
        
        browse_btn = ttk.Button(
            file_row, 
            text="📂 Duyệt...", 
            command=self._browse_file,
            width=12
        )
        browse_btn.pack(side=tk.RIGHT, pady=2)
        
        info_frame = ttk.Frame(self.frame)
        info_frame.pack(fill=tk.X)
        
        self.info_label = ttk.Label(
            info_frame,
            text=" Chất lượng dữ liệu được phân tích và gợi ý thông minh được đưa ra",
            font=("Arial", 9),
            foreground="darkgreen"
        )
        self.info_label.pack(side=tk.LEFT)
        
        self.file_info_label = ttk.Label(
            info_frame,
            text="",
            font=("Arial", 9),
            foreground="blue"
        )
        self.file_info_label.pack(side=tk.RIGHT)
    
    def _browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Chọn tệp Excel",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ],
            initialdir=Path.home() / "Documents"
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            
            file_size = Path(file_path).stat().st_size / 1024
            self.file_info_label.config(text=f"📊 {file_size:.1f} KB")
            
            self.on_file_selected(file_path)
            logger.info(f"User selected file: {file_path}")
    
    def get_file_path(self) -> str:
        path = self.file_path_var.get()
        return path if path != "Chưa chọn tệp..." else ""
    
    def reset(self):
        self.file_path_var.set("Chưa chọn tệp...")
        self.file_info_label.config(text="")
    
    def has_file_selected(self) -> bool:
        return self.get_file_path() != ""

class FlexibleAnalysisFrame:
    
    def __init__(self, parent: tk.Widget):
        self.frame = ttk.LabelFrame(parent, text="🔧 Cấu hình phân tích dữ liệu", padding=10)
        self.frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.x_column_var = tk.StringVar()
        self.y_column_var = tk.StringVar()
        self.operation_var = tk.StringVar(value="sum")
        
        self.x_options = []
        self.y_options = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        main_grid = ttk.Frame(self.frame)
        main_grid.pack(fill=tk.X)
        
        col_frame = ttk.LabelFrame(main_grid, text="Chọn cột dữ liệu", padding=8)
        col_frame.grid(row=0, column=0, sticky=tk.EW, padx=(0, 10))
        
        ttk.Label(col_frame, text="Cột X (phân loại):", font=("Arial", 9, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=3
        )
        self.x_combo = ttk.Combobox(
            col_frame, 
            textvariable=self.x_column_var, 
            state="readonly", 
            width=30,
            font=("Arial", 9)
        )
        self.x_combo.grid(row=0, column=1, sticky=tk.EW, padx=(5, 0), pady=3)
        
        ttk.Label(col_frame, text="Cột Y (số liệu):", font=("Arial", 9, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=3
        )
        self.y_combo = ttk.Combobox(
            col_frame, 
            textvariable=self.y_column_var, 
            state="readonly", 
            width=30,
            font=("Arial", 9)
        )
        self.y_combo.grid(row=1, column=1, sticky=tk.EW, padx=(5, 0), pady=3)
        
        col_frame.columnconfigure(1, weight=1)
        
        op_frame = ttk.LabelFrame(main_grid, text="Phép tính", padding=8)
        op_frame.grid(row=0, column=1, sticky=tk.EW)
        
        operations = [
            ("sum", "Tổng"),
            ("mean", "Trung bình"),
            ("count", "Đếm"),
            ("max", "⬆️Lớn nhất"),
            ("min", "⬇️Nhỏ nhất")
        ]
        
        for i, (value, text) in enumerate(operations):
            rb = ttk.Radiobutton(
                op_frame,
                text=text,
                variable=self.operation_var,
                value=value,
                style="TRadiobutton"
            )
            rb.grid(row=i, column=0, sticky=tk.W, pady=2)
        
        main_grid.columnconfigure(0, weight=1)
        main_grid.columnconfigure(1, weight=1)
        
        suggest_frame = ttk.Frame(self.frame)
        suggest_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.suggest_btn = ttk.Button(
            suggest_frame,
            text="🎯 Tự động gợi ý cột tốt nhất",
            command=self._auto_suggest,
            style="Accent.TButton"
        )
        self.suggest_btn.pack(side=tk.LEFT)
        
        self.analysis_status = ttk.Label(
            suggest_frame,
            text="",
            font=("Arial", 9),
            foreground="blue"
        )
        self.analysis_status.pack(side=tk.RIGHT)
    
    def _auto_suggest(self):
        if self.x_options and self.y_options:
            best_x = self.x_options[0] if self.x_options else ""
            best_y = self.y_options[0] if self.y_options else ""
            
            if best_x:
                self.x_column_var.set(best_x)
            if best_y:
                self.y_column_var.set(best_y)
            
            self.analysis_status.config(text=f"✅ Đã chọn: {best_x} vs {best_y}")
        else:
            self.analysis_status.config(text="⚠️ Chưa có dữ liệu để gợi ý")
    
    def update_column_options(self, x_options: List[str], y_options: List[str], 
                            suggested_x: str = None, suggested_y: str = None):
        self.x_options = x_options
        self.y_options = y_options
        
        self.x_combo['values'] = x_options
        self.y_combo['values'] = y_options
        
        if suggested_x and suggested_x in x_options:
            self.x_column_var.set(suggested_x)
        elif x_options:
            self.x_column_var.set(x_options[0])
            
        if suggested_y and suggested_y in y_options:
            self.y_column_var.set(suggested_y)
        elif y_options:
            self.y_column_var.set(y_options[0])
        
        if x_options and y_options:
            self.analysis_status.config(text=f"📊 {len(x_options)} cột X, {len(y_options)} cột Y")
    
    def get_analysis_config(self) -> Dict[str, str]:
        return {
            "x_column": self.x_column_var.get(),
            "y_column": self.y_column_var.get(),
            "operation": self.operation_var.get()
        }
    
    def has_valid_selection(self) -> bool:
        return bool(self.x_column_var.get() and self.y_column_var.get())
    
    def reset(self):
        self.x_column_var.set("")
        self.y_column_var.set("")
        self.operation_var.set("sum")
        self.analysis_status.config(text="")

class ChartConfigFrame:
    
    def __init__(self, parent: tk.Widget):
        self.frame = ttk.LabelFrame(parent, text="📊 Cấu hình biểu đồ", padding=10)
        self.frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.title_var = tk.StringVar(value=Config.DEFAULT_CHART_DEFAULTS["title"])
        self.xlabel_var = tk.StringVar(value=Config.DEFAULT_CHART_DEFAULTS["xlabel"])
        self.ylabel_var = tk.StringVar(value=Config.DEFAULT_CHART_DEFAULTS["ylabel"])
        
        self._create_widgets()
    
    def _create_widgets(self):
        labels_grid = ttk.Frame(self.frame)
        labels_grid.pack(fill=tk.X)
        
        ttk.Label(labels_grid, text="Tiêu đề:", font=("Arial", 9, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=3
        )
        title_entry = ttk.Entry(labels_grid, textvariable=self.title_var, width=50, font=("Arial", 9))
        title_entry.grid(row=0, column=1, sticky=tk.EW, padx=(5, 0), pady=3)
        
        ttk.Label(labels_grid, text="Nhãn trục X:", font=("Arial", 9, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=3
        )
        xlabel_entry = ttk.Entry(labels_grid, textvariable=self.xlabel_var, width=50, font=("Arial", 9))
        xlabel_entry.grid(row=1, column=1, sticky=tk.EW, padx=(5, 0), pady=3)
        
        ttk.Label(labels_grid, text="Nhãn trục Y:", font=("Arial", 9, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=3
        )
        ylabel_entry = ttk.Entry(labels_grid, textvariable=self.ylabel_var, width=50, font=("Arial", 9))
        ylabel_entry.grid(row=2, column=1, sticky=tk.EW, padx=(5, 0), pady=3)
        
        labels_grid.columnconfigure(1, weight=1)
        
        template_frame = ttk.Frame(self.frame)
        template_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(template_frame, text="Mẫu nhanh:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        
        templates = [
            ("📊 Doanh số", "Biểu đồ doanh số", "Khu vực", "Doanh số (VNĐ)"),
            ("👥 Nhân sự", "Biểu đồ nhân sự", "Phòng ban", "Số lượng người"),
            ("📈 Hiệu suất", "Biểu đồ hiệu suất", "Tháng", "Hiệu suất (%)"),
        ]
        
        for text, title, xlabel, ylabel in templates:
            btn = ttk.Button(
                template_frame,
                text=text,
                command=lambda t=title, x=xlabel, y=ylabel: self._apply_template(t, x, y),
                width=12
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def _apply_template(self, title: str, xlabel: str, ylabel: str):
        self.title_var.set(title)
        self.xlabel_var.set(xlabel)
        self.ylabel_var.set(ylabel)
    
    def get_chart_config(self) -> Dict[str, str]:
        return {
            "title": self.title_var.get().strip(),
            "xlabel": self.xlabel_var.get().strip(),
            "ylabel": self.ylabel_var.get().strip()
        }
    
    def reset_to_defaults(self):
        self.title_var.set(Config.DEFAULT_CHART_DEFAULTS["title"])
        self.xlabel_var.set(Config.DEFAULT_CHART_DEFAULTS["xlabel"])
        self.ylabel_var.set(Config.DEFAULT_CHART_DEFAULTS["ylabel"])

class DataPreviewFrame:
    
    def __init__(self, parent: tk.Widget):
        self.frame = ttk.LabelFrame(parent, text="📊 Thông tin & Kết quả", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self._create_widgets()
    
    def _create_widgets(self):
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self._create_info_tab()
        self._create_stats_tab()
        self._create_preview_tab()
    
    def _create_info_tab(self):
        self.info_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.info_frame, text="📋 Thông tin")
        
        self.info_text = tk.Text(
            self.info_frame,
            height=10,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#f8f9fa",
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        
        info_scrollbar = ttk.Scrollbar(self.info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_stats_tab(self):
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="📈 Thống kê")
        
        self.stats_text = tk.Text(
            self.stats_frame,
            height=10,
            state=tk.DISABLED,
            wrap=tk.NONE,
            font=("Consolas", 9),
            bg="#f8f9fa"
        )
        
        stats_scrollbar_y = ttk.Scrollbar(self.stats_frame, orient=tk.VERTICAL, command=self.stats_text.yview)
        stats_scrollbar_x = ttk.Scrollbar(self.stats_frame, orient=tk.HORIZONTAL, command=self.stats_text.xview)
        self.stats_text.configure(yscrollcommand=stats_scrollbar_y.set, xscrollcommand=stats_scrollbar_x.set)
        
        self.stats_text.grid(row=0, column=0, sticky=tk.NSEW)
        stats_scrollbar_y.grid(row=0, column=1, sticky=tk.NS)
        stats_scrollbar_x.grid(row=1, column=0, sticky=tk.EW)
        
        self.stats_frame.rowconfigure(0, weight=1)
        self.stats_frame.columnconfigure(0, weight=1)
    
    def _create_preview_tab(self):
        self.preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_frame, text="👁️ Xem trước")
        
        columns = ("col1", "col2", "col3", "col4", "col5")
        self.tree = ttk.Treeview(self.preview_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=f"Cột {col}")
            self.tree.column(col, width=120)
        
        tree_scrollbar_y = ttk.Scrollbar(self.preview_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scrollbar_x = ttk.Scrollbar(self.preview_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
        
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        tree_scrollbar_y.grid(row=0, column=1, sticky=tk.NS)
        tree_scrollbar_x.grid(row=1, column=0, sticky=tk.EW)
        
        self.preview_frame.rowconfigure(0, weight=1)
        self.preview_frame.columnconfigure(0, weight=1)
    
    def update_info(self, message: str):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, message)
        self.info_text.config(state=tk.DISABLED)
    
    def update_stats(self, stats_text: str):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats_text)
        self.stats_text.config(state=tk.DISABLED)
    
    def update_preview(self, df: Optional[pd.DataFrame]):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if df is not None and not df.empty:
            columns = list(df.columns)[:5]
            for i, col in enumerate(columns):
                self.tree.heading(f"col{i+1}", text=str(col)[:15])
            
            for idx, row in df.head(50).iterrows():
                values = [str(row[col])[:20] if col in row.index else "" for col in columns]
                self.tree.insert("", tk.END, values=values)

class ActionButtonsFrame:
    
    def __init__(self, parent: tk.Widget, callbacks: Dict[str, Callable]):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.callbacks = callbacks
        self._create_widgets()
    
    def _create_widgets(self):
        main_buttons = [
            ("🤖 Phân tích thông minh", "analyze", "#2563eb"),
            ("📊 Biểu đồ cột", "create_bar_chart", "#059669"),
            ("🥧 Biểu đồ tròn", "create_pie_chart", "#dc2626"),
            ("📈 Biểu đồ đường", "create_line_chart", "#ea580c"),
        ]
        
        secondary_buttons = [
            ("💾 Xuất Excel", "export_excel", "#6b7280"),
            ("📋 Sao chép kết quả", "copy_results", "#6b7280"),
            ("🔄 Đặt lại", "reset", "#6b7280"),
            ("❌ Thoát", "exit", "#dc2626")
        ]
        
        main_frame = ttk.LabelFrame(self.frame, text="Hành động chính", padding=5)
        main_frame.pack(fill=tk.X, pady=(0, 5))
        
        for i, (text, callback_key, color) in enumerate(main_buttons):
            btn = ttk.Button(
                main_frame,
                text=text,
                command=self.callbacks.get(callback_key, lambda: None),
                width=18
            )
            btn.grid(row=0, column=i, padx=3, sticky=tk.EW)
        
        for i in range(len(main_buttons)):
            main_frame.columnconfigure(i, weight=1)
        
        secondary_frame = ttk.Frame(self.frame)
        secondary_frame.pack(fill=tk.X)
        
        for i, (text, callback_key, color) in enumerate(secondary_buttons):
            btn = ttk.Button(
                secondary_frame,
                text=text,
                command=self.callbacks.get(callback_key, lambda: None),
                width=15
            )
            btn.grid(row=0, column=i, padx=2, sticky=tk.EW)
        
        for i in range(len(secondary_buttons)):
            secondary_frame.columnconfigure(i, weight=1)

class NaNHandlingFrame:
    
    def __init__(self, parent: tk.Widget, on_strategy_changed: Optional[Callable] = None):
        self.frame = ttk.LabelFrame(parent, text="🔧 Xử lý giá trị trống (NaN)", padding=10)
        self.frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.on_strategy_changed = on_strategy_changed
        self.nan_analysis = {}
        self.strategy_vars = {}
        self.strategy_widgets = {}
        
        self._create_widgets()
    
    def _create_widgets(self):
        self.info_frame = ttk.Frame(self.frame)
        self.info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_label = ttk.Label(
            self.info_frame,
            text="📊 Chưa phân tích dữ liệu. Vui lòng tải file Excel để xem thông tin NaN.",
            font=("Arial", 10),
            foreground="gray"
        )
        self.info_label.pack(side=tk.LEFT)
        
        self.analyze_btn = ttk.Button(
            self.info_frame,
            text=" Phân tích NaN ",
            command=self._analyze_nan,
            state="disabled"
        )
        self.analyze_btn.pack(side=tk.RIGHT)
        
        self.strategy_frame = ttk.LabelFrame(self.frame, text="Chiến lược xử lý", padding=5)
        
        self.global_frame = ttk.Frame(self.strategy_frame)
        self.global_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.global_frame, text="Áp dụng toàn bộ:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        
        global_buttons = [
            ("🔄 Tự động", self._apply_auto_strategy),
            ("❌ Xóa dòng", self._apply_drop_strategy),
            ("⚪ Điền 0", self._apply_zero_strategy),
            ("❓ Điền Unknown", self._apply_unknown_strategy)
        ]
        
        for text, command in global_buttons:
            btn = ttk.Button(self.global_frame, text=text, command=command, width=20)
            btn.pack(side=tk.LEFT, padx=5)
        
        self.columns_frame = ttk.Frame(self.strategy_frame)
        self.columns_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(self.columns_frame, height=800)
        scrollbar = ttk.Scrollbar(self.columns_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def update_data(self, df: pd.DataFrame):
        self.current_data = df
        self.analyze_btn.config(state="normal")
        
        total_nan = df.isnull().sum().sum()
        if total_nan > 0:
            self.info_label.config(
                text=f"⚠️ Phát hiện {total_nan} ô trống. Nhấn 'Phân tích NaN' để xem chi tiết.",
                foreground="orange"
            )
        else:
            self.info_label.config(
                text="✅ Không có giá trị trống trong dữ liệu.",
                foreground="green"
            )
    
    def _analyze_nan(self):
        if not hasattr(self, 'current_data'):
            return
        
        from data_processor import FlexibleDataProcessor
        
        try:
            self.nan_analysis = FlexibleDataProcessor.analyze_nan_values(self.current_data)
            self._display_analysis_results()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phân tích NaN:\n{str(e)}")
    
    def _display_analysis_results(self):
        if not self.nan_analysis.get("columns_with_nan"):
            self.info_label.config(
                text="✅ Không có giá trị NaN nào trong dữ liệu!",
                foreground="green"
            )
            return
        
        total_nan = self.nan_analysis["total_nan_cells"]
        nan_pct = self.nan_analysis["nan_percentage"]
        
        self.info_label.config(
            text=f"📊 Tìm thấy {total_nan} ô trống ({nan_pct}%) trong {len(self.nan_analysis['columns_with_nan'])} cột",
            foreground="red" if nan_pct > 10 else "orange"
        )
        
        self.strategy_frame.pack(fill=tk.X, pady=(10, 0))
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.strategy_vars = {}
        self.strategy_widgets = {}
        
        row = 0
        for col, info in self.nan_analysis["columns_with_nan"].items():
            self._create_column_strategy(col, info, row)
            row += 1
    
    def _create_column_strategy(self, col: str, info: Dict, row: int):
        col_frame = ttk.LabelFrame(self.scrollable_frame, text=f"Cột: {col}", padding=5)
        col_frame.grid(row=row, column=0, sticky=tk.EW, padx=5, pady=2)
        
        info_row = ttk.Frame(col_frame)
        info_row.pack(fill=tk.X)
        
        info_text = f"📊 {info['count']} NaN ({info['percentage']}%) - Kiểu: {info['dtype']}"
        ttk.Label(info_row, text=info_text, font=("Arial", 9)).pack(side=tk.LEFT)
        
        strategy_row = ttk.Frame(col_frame)
        strategy_row.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(strategy_row, text="Xử lý:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W)
        
        strategy_var = tk.StringVar(value="auto")
        self.strategy_vars[col] = strategy_var
        
        strategies = [
            ("auto", "🎯 Tự động"),
            ("drop", "❌ Xóa dòng"),
            ("fill", "🔄 Điền giá trị")
        ]
        
        for i, (value, text) in enumerate(strategies):
            rb = ttk.Radiobutton(
                strategy_row,
                text=text,
                variable=strategy_var,
                value=value,
                command=lambda c=col: self._on_strategy_change(c)
            )
            rb.grid(row=0, column=i+1, padx=5)
        
        fill_frame = ttk.Frame(col_frame)
        self.strategy_widgets[col] = {
            "fill_frame": fill_frame,
            "strategy_var": strategy_var
        }
        
        ttk.Label(fill_frame, text="Giá trị điền:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        recommendations = self.nan_analysis.get("recommendations", {}).get(col, {})
        
        if recommendations.get("type") == "numeric":
            fill_var = tk.StringVar(value="median")
            self.strategy_widgets[col]["fill_var"] = fill_var
            
            numeric_options = [
                ("median", f"Median ({recommendations['suggestions']['median']})"),
                ("mean", f"Mean ({recommendations['suggestions']['mean']})"),
                ("mode", f"Mode ({recommendations['suggestions']['mode']})"),
                ("zero", "Số 0"),
                ("custom", "Tùy chỉnh")
            ]
            
            for i, (value, text) in enumerate(numeric_options):
                rb = ttk.Radiobutton(fill_frame, text=text, variable=fill_var, value=value)
                rb.grid(row=0, column=i+1, padx=2)
            
            custom_var = tk.StringVar(value="0")
            self.strategy_widgets[col]["custom_var"] = custom_var
            custom_entry = ttk.Entry(fill_frame, textvariable=custom_var, width=10)
            custom_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=2)
            
        else:
            fill_var = tk.StringVar(value="unknown")
            self.strategy_widgets[col]["fill_var"] = fill_var
            
            mode_value = recommendations.get("mode", "Unknown")
            categorical_options = [
                ("mode", f"Mode ({mode_value})"),
                ("unknown", "Unknown"),
                ("empty", "Chuỗi rỗng"),
                ("custom", "Tùy chỉnh")
            ]
            
            for i, (value, text) in enumerate(categorical_options):
                rb = ttk.Radiobutton(fill_frame, text=text, variable=fill_var, value=value)
                rb.grid(row=0, column=i+1, padx=2)
            
            custom_var = tk.StringVar(value="Unknown")
            self.strategy_widgets[col]["custom_var"] = custom_var
            custom_entry = ttk.Entry(fill_frame, textvariable=custom_var, width=15)
            custom_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=2)
        
        self.scrollable_frame.columnconfigure(0, weight=1)
    
    def _on_strategy_change(self, col: str):
        strategy = self.strategy_vars[col].get()
        fill_frame = self.strategy_widgets[col]["fill_frame"]
        
        if strategy == "fill":
            fill_frame.pack(fill=tk.X, pady=(5, 0))
        else:
            fill_frame.pack_forget()
        
        if self.on_strategy_changed:
            self.on_strategy_changed()
    
    def _apply_auto_strategy(self):
        for col in self.strategy_vars:
            self.strategy_vars[col].set("auto")
            self._on_strategy_change(col)
    
    def _apply_drop_strategy(self):
        if messagebox.askyesno("Xác nhận", "Xóa tất cả dòng có giá trị trống?"):
            for col in self.strategy_vars:
                self.strategy_vars[col].set("drop")
                self._on_strategy_change(col)
    
    def _apply_zero_strategy(self):
        for col in self.strategy_vars:
            recommendations = self.nan_analysis.get("recommendations", {}).get(col, {})
            if recommendations.get("type") == "numeric":
                self.strategy_vars[col].set("fill")
                if "fill_var" in self.strategy_widgets[col]:
                    self.strategy_widgets[col]["fill_var"].set("zero")
                self._on_strategy_change(col)
    
    def _apply_unknown_strategy(self):
        for col in self.strategy_vars:
            recommendations = self.nan_analysis.get("recommendations", {}).get(col, {})
            if recommendations.get("type") != "numeric":
                self.strategy_vars[col].set("fill")
                if "fill_var" in self.strategy_widgets[col]:
                    self.strategy_widgets[col]["fill_var"].set("unknown")
                self._on_strategy_change(col)
    
    def get_nan_strategy(self) -> Dict[str, Dict]:
        strategy = {}
        
        for col, var in self.strategy_vars.items():
            method = var.get()
            
            if method == "auto":
                strategy[col] = {"method": "auto"}
            
            elif method == "drop":
                strategy[col] = {"method": "drop"}
            
            elif method == "fill":
                fill_method = self.strategy_widgets[col]["fill_var"].get()
                recommendations = self.nan_analysis.get("recommendations", {}).get(col, {})
                
                if fill_method == "median" and recommendations.get("type") == "numeric":
                    value = recommendations["suggestions"]["median"]
                elif fill_method == "mean" and recommendations.get("type") == "numeric":
                    value = recommendations["suggestions"]["mean"]
                elif fill_method == "mode":
                    if recommendations.get("type") == "numeric":
                        value = recommendations["suggestions"]["mode"]
                    else:
                        value = recommendations.get("mode", "Unknown")
                elif fill_method == "zero":
                    value = 0
                elif fill_method == "unknown":
                    value = "Unknown"
                elif fill_method == "empty":
                    value = ""
                elif fill_method == "custom":
                    value = self.strategy_widgets[col]["custom_var"].get()
                    if recommendations.get("type") == "numeric":
                        try:
                            value = float(value)
                        except ValueError:
                            value = 0
                else:
                    value = "Unknown"
                
                strategy[col] = {"method": "fill", "value": value}
        
        return strategy
    
    def has_nan_data(self) -> bool:
        return bool(self.nan_analysis.get("columns_with_nan"))
    
    def reset(self):
        self.nan_analysis = {}
        self.strategy_vars = {}
        self.strategy_widgets = {}
        
        if hasattr(self, 'current_data'):
            delattr(self, 'current_data')
        
        self.analyze_btn.config(state="disabled")
        self.info_label.config(
            text="📊 Chưa phân tích dữ liệu. Vui lòng tải file Excel để xem thông tin NaN.",
            foreground="gray"
        )
        
        self.strategy_frame.pack_forget()
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def show_nan_summary(self) -> str:
        if not self.nan_analysis:
            return "Chưa phân tích dữ liệu NaN."
        
        if not self.nan_analysis.get("columns_with_nan"):
            return "✅ Dữ liệu sạch - Không có giá trị NaN!"
        
        summary = f"📊 TÌNH TRẠNG GIÁ TRỊ TRỐNG:\n"
        summary += f"• Tổng ô trống: {self.nan_analysis['total_nan_cells']:,}\n"
        summary += f"• Tỷ lệ: {self.nan_analysis['nan_percentage']}%\n"
        summary += f"• Số cột bị ảnh hưởng: {len(self.nan_analysis['columns_with_nan'])}\n\n"
        
        summary += "CHI TIẾT TỪNG CỘT:\n"
        for col, info in self.nan_analysis["columns_with_nan"].items():
            summary += f"• {col}: {info['count']} NaN ({info['percentage']}%)\n"
        
        if self.strategy_vars:
            summary += "\nCHIẾN LƯỢC XỬ LÝ:\n"
            for col, var in self.strategy_vars.items():
                method = var.get()
                if method == "fill" and col in self.strategy_widgets:
                    fill_method = self.strategy_widgets[col]["fill_var"].get()
                    summary += f"• {col}: Điền {fill_method}\n"
                else:
                    summary += f"• {col}: {method}\n"
        
        return summary

# Alias for backward compatibility
StatusBar = ModernStatusBar