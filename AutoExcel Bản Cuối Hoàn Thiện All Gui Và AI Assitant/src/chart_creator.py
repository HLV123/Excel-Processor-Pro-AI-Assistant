import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Tuple
from exceptions import ChartCreationError
from validators import DataValidator
from config import Config
from logger import Logger

logger = Logger().get_logger()

class FlexibleChartCreator:
    
    def __init__(self):
        plt.style.use('default')
        sns.set_palette("husl")
    
    def create_bar_chart(
        self,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        output_path: Path,
        title: str,
        xlabel: str,
        ylabel: str,
        figsize: Tuple[int, int] = (12, 8),
        color: str = "steelblue"
    ) -> None:
        try:
            DataValidator.validate_dataframe(df)
            DataValidator.validate_column_selection(df, x_col, y_col)
            DataValidator.validate_chart_input(title, xlabel, ylabel)
            
            logger.info(f"Creating flexible bar chart: {title}")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=figsize)
            
            # Handle long category names
            x_labels = df[x_col].astype(str)
            if max(len(str(x)) for x in x_labels) > 15:
                rotation = 45
                ha = 'right'
            else:
                rotation = 0
                ha = 'center'
            
            bars = ax.bar(x_labels, df[y_col], color=color, alpha=0.8, edgecolor='navy', linewidth=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
            ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
            
            ax.grid(True, alpha=0.3, axis='y')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if pd.notna(height):  # Check for NaN values
                    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                           f'{height:,.0f}', ha='center', va='bottom', fontweight='bold')
            
            plt.xticks(rotation=rotation, ha=ha)
            plt.tight_layout()
            
            plt.savefig(output_path, dpi=Config.DEFAULT_CHART_DEFAULTS["dpi"], bbox_inches='tight')
            logger.info(f"Bar chart saved successfully to {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            raise ChartCreationError(f"Bar chart creation failed: {e}")
        
        finally:
            plt.close()
    
    def create_pie_chart(
        self,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        output_path: Path,
        title: str,
        figsize: Tuple[int, int] = (10, 10)
    ) -> None:
        try:
            DataValidator.validate_dataframe(df)
            DataValidator.validate_column_selection(df, x_col, y_col)
            
            logger.info(f"Creating flexible pie chart: {title}")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=figsize)
            
            # Filter out zero or negative values for pie chart
            df_filtered = df[df[y_col] > 0].copy()
            
            if df_filtered.empty:
                raise ChartCreationError("No positive values found for pie chart")
            
            # Limit to top 10 categories for readability
            if len(df_filtered) > 10:
                df_filtered = df_filtered.head(10)
                logger.info("Limited pie chart to top 10 categories for better readability")
            
            wedges, texts, autotexts = ax.pie(
                df_filtered[y_col], 
                labels=df_filtered[x_col].astype(str),
                autopct='%1.1f%%',
                startangle=90,
                explode=[0.05] * len(df_filtered)
            )
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            for text in texts:
                text.set_fontsize(9)
            
            plt.tight_layout()
            
            plt.savefig(output_path, dpi=Config.DEFAULT_CHART_DEFAULTS["dpi"], bbox_inches='tight')
            logger.info(f"Pie chart saved successfully to {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating pie chart: {e}")
            raise ChartCreationError(f"Pie chart creation failed: {e}")
        
        finally:
            plt.close()
    
    def create_line_chart(
        self,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        output_path: Path,
        title: str,
        xlabel: str,
        ylabel: str,
        figsize: Tuple[int, int] = (12, 8)
    ) -> None:
        try:
            DataValidator.validate_dataframe(df)
            DataValidator.validate_column_selection(df, x_col, y_col)
            DataValidator.validate_chart_input(title, xlabel, ylabel)
            
            logger.info(f"Creating line chart: {title}")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=figsize)
            
            ax.plot(df[x_col], df[y_col], marker='o', linewidth=2, markersize=6)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
            ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
            
            ax.grid(True, alpha=0.3)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            plt.savefig(output_path, dpi=Config.DEFAULT_CHART_DEFAULTS["dpi"], bbox_inches='tight')
            logger.info(f"Line chart saved successfully to {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating line chart: {e}")
            raise ChartCreationError(f"Line chart creation failed: {e}")
        
        finally:
            plt.close()