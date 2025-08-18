# File: src/gui_app.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from pathlib import Path
from typing import Dict, Any
import pandas as pd

from excel_processor import FlexibleExcelProcessor
from ai_assistant_dialog import IntelligentAnalysisDialog
from gui_components import (
    ModernStatusBar, FileSelectionFrame, FlexibleAnalysisFrame,
    ChartConfigFrame, DataPreviewFrame, ActionButtonsFrame, NaNHandlingFrame
)
from config import Config
from exceptions import ExcelProcessorError
from validators import DataValidator
from logger import Logger

logger = Logger().get_logger()

class ResizableFrame:
    def __init__(self, parent, initial_width=500):
        self.parent = parent
        self.initial_width = initial_width
        self.current_width = initial_width
        self.is_dragging = False
        
        self.main_frame = tk.Frame(parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.left_frame = tk.Frame(self.main_frame, width=self.current_width, bg='#f0f0f0')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.left_frame.pack_propagate(False)
        
        self.splitter = tk.Frame(self.main_frame, width=6, bg='#d0d0d0', cursor='sb_h_double_arrow')
        self.splitter.pack(side=tk.LEFT, fill=tk.Y)
        
        self.right_frame = tk.Frame(self.main_frame, bg='white')
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.splitter.bind('<Button-1>', self.start_drag)
        self.splitter.bind('<B1-Motion>', self.on_drag)
        self.splitter.bind('<ButtonRelease-1>', self.stop_drag)
        self.splitter.bind('<Enter>', self.on_enter)
        self.splitter.bind('<Leave>', self.on_leave)
    
    def start_drag(self, event):
        self.is_dragging = True
        self.splitter.config(bg='#4472c4')
    
    def on_drag(self, event):
        if self.is_dragging:
            x = event.x_root - self.main_frame.winfo_rootx()
            min_width = 350
            max_width = self.main_frame.winfo_width() - 500
            new_width = max(min_width, min(x, max_width))
            
            if new_width != self.current_width:
                self.current_width = new_width
                self.left_frame.config(width=self.current_width)
    
    def stop_drag(self, event):
        self.is_dragging = False
        self.splitter.config(bg='#d0d0d0')
    
    def on_enter(self, event):
        if not self.is_dragging:
            self.splitter.config(bg='#a0a0a0')
    
    def on_leave(self, event):
        if not self.is_dragging:
            self.splitter.config(bg='#d0d0d0')

class CollapsibleFrame:
    def __init__(self, parent, title: str, content_creator_func):
        self.parent = parent
        self.is_expanded = True
        
        self.main_frame = ttk.Frame(parent)
        self.main_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X)
        
        self.toggle_btn = ttk.Button(self.header_frame, text="▼", width=3, command=self.toggle)
        self.toggle_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.title_label = ttk.Label(self.header_frame, text=title, font=("Arial", 10, "bold"))
        self.title_label.pack(side=tk.LEFT)
        
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.X, padx=(20, 0), pady=(5, 0))
        
        self.content_widget = content_creator_func(self.content_frame)
    
    def toggle(self):
        if self.is_expanded:
            self.content_frame.pack_forget()
            self.toggle_btn.config(text="►")
        else:
            self.content_frame.pack(fill=tk.X, padx=(20, 0), pady=(5, 0))
            self.toggle_btn.config(text="▼")
        self.is_expanded = not self.is_expanded

class ScrollableLeftPanel:
    def __init__(self, parent):
        self.main_frame = ttk.Frame(parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0, bg='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class ExcelProcessorGUI:
    def __init__(self):
        self.processor = FlexibleExcelProcessor()
        self.root = tk.Tk()
        self.current_data = None
        self.analysis_result = None
        self.custom_nan_strategy = None
        
        self._setup_window()
        self._create_widgets()
        self._setup_callbacks()
        
        logger.info("Enhanced GUI application initialized with improved layout")
    
    def _setup_window(self):
        self.root.title("Excel Processor Pro - Assistant")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        style = ttk.Style()
        try:
            style.theme_use('winnative')
        except:
            style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
    
    def _create_widgets(self):
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="🤖 Excel Processor Pro - AI Assistant cho phân tích dữ liệu thông minh", style='Title.TLabel')
        title_label.pack()
        
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.resizable_frame = ResizableFrame(content_frame, initial_width=500)
        self.left_container = self.resizable_frame.left_frame
        self.right_container = self.resizable_frame.right_frame
        
        self._create_left_panel()
        self._create_right_panel()
        
        self.status_bar = ModernStatusBar(self.root)
    
    def _create_left_panel(self):
        self.left_panel = ScrollableLeftPanel(self.left_container)
        
        self.collapsible_frames = {}
        
        self.collapsible_frames["file"] = CollapsibleFrame(
            self.left_panel.scrollable_frame, "📁 Chọn tệp dữ liệu Excel",
            lambda parent: FileSelectionFrame(parent, self._on_file_selected)
        )
        self.file_frame = self.collapsible_frames["file"].content_widget
        
        self.collapsible_frames["analysis"] = CollapsibleFrame(
            self.left_panel.scrollable_frame, "🔧 Cấu hình phân tích dữ liệu", 
            lambda parent: FlexibleAnalysisFrame(parent)
        )
        self.analysis_frame = self.collapsible_frames["analysis"].content_widget
        
        self.collapsible_frames["chart"] = CollapsibleFrame(
            self.left_panel.scrollable_frame, "📊 Cấu hình biểu đồ",
            lambda parent: ChartConfigFrame(parent)
        )
        self.chart_config_frame = self.collapsible_frames["chart"].content_widget
        
        self.collapsible_frames["nan"] = CollapsibleFrame(
            self.left_panel.scrollable_frame, "🔧 Xử lý giá trị trống (NaN)",
            lambda parent: NaNHandlingFrame(parent, self._on_nan_strategy_changed)
        )
        self.nan_handling_frame = self.collapsible_frames["nan"].content_widget
        
        self.collapsible_frames["actions"] = CollapsibleFrame(
            self.left_panel.scrollable_frame, "⚡ Hành động",
            lambda parent: ActionButtonsFrame(parent, self._get_button_callbacks())
        )
        self.action_frame = self.collapsible_frames["actions"].content_widget
        
        separator = ttk.Separator(self.left_panel.scrollable_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=20)
        
        info_label = ttk.Label(self.left_panel.scrollable_frame, text="💡 Tip: Kéo thanh chia giữa để điều chỉnh kích thước", font=("Arial", 9, "italic"), foreground="gray")
        info_label.pack(pady=10)
    
    def _create_right_panel(self):
        self.data_preview_frame = DataPreviewFrame(self.right_container)
    
    def _get_button_callbacks(self) -> Dict[str, callable]:
        return {
            "analyze": self._run_intelligent_analysis,
            "create_bar_chart": self._create_bar_chart,
            "create_pie_chart": self._create_pie_chart,
            "create_line_chart": self._create_line_chart,
            "export_excel": self._export_excel,
            "copy_results": self._copy_results,
            "reset": self._reset_application,
            "exit": self._exit_application
        }
    
    def _setup_callbacks(self):
        self.root.protocol("WM_DELETE_WINDOW", self._exit_application)
    
    def _on_file_selected(self, file_path: str):
        try:
            self.status_bar.set_status("Đang tải tệp...", "working", True)
            
            self.current_data = self.processor.load_data(Path(file_path))
            
            suggestions = self.processor.get_data_suggestions()
            
            self.analysis_frame.update_column_options(
                suggestions.get("x_options", []),
                suggestions.get("y_options", []),
                suggestions.get("suggested_x"),
                suggestions.get("suggested_y")
            )
            
            self.nan_handling_frame.update_data(self.current_data)
            
            self.data_preview_frame.update_info(self.processor.get_data_info())
            self.data_preview_frame.update_preview(self.current_data.head(50))
            
            self.status_bar.set_status(f"✅ Đã tải tệp: {Path(file_path).name}", "success")
            
            if not self.collapsible_frames["analysis"].is_expanded:
                self.collapsible_frames["analysis"].toggle()
            
            logger.info(f"File loaded successfully: {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải tệp:\n{str(e)}")
            self.status_bar.set_status("❌ Lỗi khi tải tệp", "error")
            self.file_frame.reset()
    
    def _on_nan_strategy_changed(self):
        self.custom_nan_strategy = self.nan_handling_frame.get_nan_strategy()
        logger.info("Custom NaN strategy updated")
    
    def _run_intelligent_analysis(self):
        if not self.file_frame.has_file_selected():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tệp Excel trước khi phân tích!")
            return
        
        if not self.analysis_frame.has_valid_selection():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột X và Y để phân tích!")
            return
        
        self.status_bar.set_status("🤖 AI đang phân tích dữ liệu...", "working", True)
        
        def analysis_preview_task():
            try:
                config = self.analysis_frame.get_analysis_config()
                
                analysis_preview = self.processor.preview_analysis(
                    config["x_column"], config["y_column"], config["operation"]
                )
                
                self.root.after(0, lambda: self._show_intelligent_dialog(analysis_preview, config))
                
            except Exception as e:
                logger.error(f"Analysis preview failed: {e}")
                self.root.after(0, lambda: self._on_preview_error(str(e)))
        
        threading.Thread(target=analysis_preview_task, daemon=True).start()
    
    def _show_intelligent_dialog(self, analysis_preview: Dict[str, Any], config: Dict[str, str]):
        self.status_bar.set_status("🤖 AI Assistant sẵn sàng...", "ready")
        
        dialog = IntelligentAnalysisDialog(
            self.root, analysis_preview,
            on_proceed=lambda: self._execute_analysis(config),
            on_customize=lambda: self._show_custom_options(analysis_preview)
        )
        
        result = dialog.show()
        
        if result == "proceed":
            self._execute_analysis(config)
        elif result == "force_proceed":
            self._execute_analysis(config, force=True)
        elif result == "customize":
            self._show_custom_options(analysis_preview)
        elif result == "cancel":
            self.status_bar.set_status("Sẵn sàng...", "ready")
    
    def _show_custom_options(self, analysis_preview: Dict[str, Any]):
        if not self.collapsible_frames["nan"].is_expanded:
            self.collapsible_frames["nan"].toggle()
        
        messagebox.showinfo(
            "Tùy chỉnh", 
            "✨ Phần 'Xử lý giá trị trống (NaN)' đã được mở rộng.\n\n"
            "Bạn có thể tùy chỉnh cách xử lý dữ liệu thiếu, "
            "sau đó nhấn '🤖 Phân tích thông minh' lại."
        )
        self.status_bar.set_status("Vui lòng tùy chỉnh và chạy lại phân tích", "ready")
    
    def _execute_analysis(self, config: Dict[str, str], force: bool = False):
        self.status_bar.set_status("⚙️ Đang xử lý dữ liệu...", "working", True)
        
        def analysis_task():
            try:
                nan_strategy = None
                if self.custom_nan_strategy and self.nan_handling_frame.has_nan_data():
                    nan_strategy = self.custom_nan_strategy
                
                self.analysis_result = self.processor.process_data(
                    config["x_column"], config["y_column"], config["operation"], nan_strategy
                )
                
                self.processor.save_processed_data()
                
                self.root.after(0, lambda: self._on_analysis_complete())
                
            except Exception as e:
                logger.error(f"Analysis failed: {e}")
                self.root.after(0, lambda: self._on_analysis_error(str(e)))
        
        threading.Thread(target=analysis_task, daemon=True).start()
    
    def _on_preview_error(self, error_message: str):
        self.status_bar.set_status("❌ Lỗi phân tích preview", "error")
        messagebox.showerror("Lỗi", f"Không thể phân tích dữ liệu:\n{error_message}")
    
    def _on_analysis_complete(self):
        self.status_bar.set_status("🎉 Phân tích hoàn thành!", "success")
        
        info_text = self.processor.get_data_info()
        self.data_preview_frame.update_info(info_text)
        
        stats_text = self.processor.get_summary_statistics()
        self.data_preview_frame.update_stats(stats_text)
        
        if self.analysis_result is not None:
            self.data_preview_frame.update_preview(self.analysis_result)
        
        nan_summary = ""
        if self.nan_handling_frame.has_nan_data():
            nan_summary = "\n\n" + self.nan_handling_frame.show_nan_summary()
        
        if not self.collapsible_frames["chart"].is_expanded:
            self.collapsible_frames["chart"].toggle()
        
        messagebox.showinfo(
            "Thành công", 
            f"✅ Dữ liệu đã được phân tích và lưu thành công!\n\n"
            f"📊 Kết quả: {len(self.analysis_result)} danh mục\n"
            f"📈 Bạn có thể tạo biểu đồ ngay bây giờ.\n"
            f"🎨 Phần cấu hình biểu đồ đã được mở rộng."
            f"{nan_summary}"
        )
        logger.info("Analysis completed successfully")
    
    def _on_analysis_error(self, error_message: str):
        self.status_bar.set_status("❌ Lỗi phân tích dữ liệu", "error")
        messagebox.showerror("Lỗi", f"Phân tích dữ liệu thất bại:\n{error_message}")
    
    def _create_bar_chart(self):
        if not self._validate_chart_creation():
            return
        self._create_chart("bar", "📊 Biểu đồ cột")
    
    def _create_pie_chart(self):
        if not self._validate_chart_creation():
            return
        self._create_chart("pie", "🥧 Biểu đồ tròn")
    
    def _create_line_chart(self):
        if not self._validate_chart_creation():
            return
        self._create_chart("line", "📈 Biểu đồ đường")
    
    def _validate_chart_creation(self) -> bool:
        if not self.file_frame.has_file_selected():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tệp Excel trước!")
            return False
            
        if not self.processor.is_ready_for_charting():
            messagebox.showwarning("Cảnh báo", "Vui lòng phân tích dữ liệu trước khi tạo biểu đồ!")
            return False
        
        return True
    
    def _create_chart(self, chart_type: str, chart_name: str):
        chart_config = self.chart_config_frame.get_chart_config()
        
        try:
            DataValidator.validate_chart_input(chart_config["title"], chart_config["xlabel"], chart_config["ylabel"])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Cấu hình biểu đồ không hợp lệ:\n{str(e)}")
            return
        
        self.status_bar.set_status(f"🎨 Đang tạo {chart_name}...", "working", True)
        
        def chart_task():
            try:
                output_path = Config.CHART_DIR / f"{chart_type}_chart.png"
                
                if chart_type == "bar":
                    result_path = self.processor.create_bar_chart(chart_config, output_path)
                elif chart_type == "pie":
                    result_path = self.processor.create_pie_chart(chart_config["title"], output_path)
                elif chart_type == "line":
                    result_path = self.processor.create_line_chart(chart_config, output_path)
                
                self.root.after(0, lambda: self._on_chart_complete(chart_name, result_path))
                
            except Exception as e:
                logger.error(f"Chart creation failed: {e}")
                self.root.after(0, lambda: self._on_chart_error(str(e)))
        
        threading.Thread(target=chart_task, daemon=True).start()
    
    def _on_chart_complete(self, chart_name: str, output_path: Path):
        self.status_bar.set_status(f"✅ {chart_name} đã tạo thành công!", "success")
        
        result = messagebox.askyesno(
            "Thành công", 
            f"🎉 {chart_name} đã được tạo thành công!\n\n"
            f"📁 Đường dẫn: {output_path}\n\n"
            f"Bạn có muốn mở thư mục chứa biểu đồ không?"
        )
        
        if result:
            import subprocess
            import platform
            
            try:
                if platform.system() == "Windows":
                    subprocess.Popen(f'explorer /select,"{output_path}"')
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", "-R", str(output_path)])
                else:
                    subprocess.Popen(["xdg-open", str(output_path.parent)])
            except Exception as e:
                logger.warning(f"Could not open folder: {e}")
        
        logger.info(f"Chart created successfully: {output_path}")
    
    def _on_chart_error(self, error_message: str):
        self.status_bar.set_status("❌ Lỗi tạo biểu đồ", "error")
        messagebox.showerror("Lỗi", f"Tạo biểu đồ thất bại:\n{error_message}")
    
    def _export_excel(self):
        if not self.processor.is_ready_for_charting():
            messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu để xuất!")
            return
        
        try:
            from tkinter import filedialog
            
            file_path = filedialog.asksaveasfilename(
                title="Lưu kết quả Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if file_path:
                self.processor.save_processed_data(Path(file_path))
                messagebox.showinfo("Thành công", f"✅ Đã xuất dữ liệu ra:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất Excel:\n{str(e)}")
    
    def _copy_results(self):
        if self.analysis_result is not None:
            try:
                result_text = self.analysis_result.to_string()
                self.root.clipboard_clear()
                self.root.clipboard_append(result_text)
                
                messagebox.showinfo("Thành công", "✅ Kết quả đã được sao chép vào clipboard!")
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể sao chép:\n{str(e)}")
        else:
            messagebox.showwarning("Cảnh báo", "Chưa có kết quả để sao chép!")
    
    def _reset_application(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đặt lại ứng dụng?"):
            self.processor.reset()
            
            self.file_frame.reset()
            self.analysis_frame.reset()
            self.chart_config_frame.reset_to_defaults()
            self.nan_handling_frame.reset()
            
            self.current_data = None
            self.analysis_result = None
            self.custom_nan_strategy = None
            
            for frame_name, frame in self.collapsible_frames.items():
                if frame_name in ["analysis", "chart", "nan"] and frame.is_expanded:
                    frame.toggle()
            
            self.data_preview_frame.update_info(
                "🤖 AI Assistant đã được đặt lại.\n\n"
                "📁 Vui lòng chọn tệp Excel để bắt đầu phân tích thông minh.\n\n"
                "💡 Tip: Sử dụng các nút ► ▼ để thu gọn/mở rộng các phần tùy ý."
            )
            self.data_preview_frame.update_stats("")
            self.data_preview_frame.update_preview(None)
            
            self.status_bar.set_status("Sẵn sàng...", "ready")
            
            logger.info("Application reset completed")
    
    def _exit_application(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thoát?"):
            logger.info("Application closing")
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        try:
            logger.info("Starting Enhanced GUI application with improved layout")
            
            self.data_preview_frame.update_info(
                "🤖 Excel Processor Pro - Assistant được thiết kế và phát triển bởi LÊ VĂN HƯNG \n\n"
                "🧠 Tính năng :\n"
                "• Phân tích chất lượng dữ liệu tự động\n"
                "• Gợi ý xử lý dữ liệu thông minh\n"
                "• Dialog tương tác trước khi phân tích\n"
                "• Xử lý NaN linh hoạt và an toàn\n\n"
                "🎨 Giao diện :\n"
                "• Layout có thể thay đổi kích thước\n"
                "• Các phần có thể thu gọn/mở rộng\n"
                "• Cuộn được khi nội dung nhiều\n"
                "• Thanh kéo thả\n\n"
                "📁 Bước 1: Chọn tệp Excel của bạn\n"
                "🤖 Bước 2: Nhận gợi ý\n"
                "✅ Bước 3: Xác nhận tạo biểu đồ\n\n"
                "💡 Tip: Kéo thanh chia giữa để điều chỉnh kích thước các phần."
            )
            
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"GUI application error: {e}")
            messagebox.showerror("Lỗi hệ thống", f"Đã xảy ra lỗi nghiêm trọng:\n{str(e)}")
        finally:
            logger.info("Enhanced GUI application terminated")