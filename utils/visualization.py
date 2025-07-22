import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import streamlit as st

class VisualizationEngine:
    """Create interactive visualizations using Plotly"""
    
    @staticmethod
    def create_chart(df: pd.DataFrame, chart_config: Dict[str, Any]) -> Optional[go.Figure]:
        """Create a chart based on configuration"""
        try:
            chart_type = chart_config.get('chart_type', '').lower()
            
            if chart_type == 'histogram':
                return VisualizationEngine._create_histogram(df, chart_config)
            elif chart_type == 'bar':
                return VisualizationEngine._create_bar_chart(df, chart_config)
            elif chart_type == 'line':
                return VisualizationEngine._create_line_chart(df, chart_config)
            elif chart_type == 'scatter':
                return VisualizationEngine._create_scatter_plot(df, chart_config)
            elif chart_type == 'box':
                return VisualizationEngine._create_box_plot(df, chart_config)
            elif chart_type == 'heatmap':
                return VisualizationEngine._create_heatmap(df, chart_config)
            elif chart_type == 'pie':
                return VisualizationEngine._create_pie_chart(df, chart_config)
            elif chart_type == 'violin':
                return VisualizationEngine._create_violin_plot(df, chart_config)
            elif chart_type == 'sunburst':
                return VisualizationEngine._create_sunburst(df, chart_config)
            elif chart_type == 'treemap':
                return VisualizationEngine._create_treemap(df, chart_config)
            else:
                st.error(f"Unsupported chart type: {chart_type}")
                return None
                
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
            return None
    
    @staticmethod
    def _create_histogram(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create histogram"""
        column = config.get('x_column')
        if not column or column not in df.columns:
            raise ValueError("Invalid or missing x_column for histogram")
        
        fig = px.histogram(
            df, 
            x=column,
            title=config.get('title', f'Distribution of {column}'),
            nbins=config.get('bins', 30),
            color=config.get('color_column'),
            facet_col=config.get('facet_column')
        )
        
        fig.update_layout(
            xaxis_title=column,
            yaxis_title='Count',
            showlegend=True if config.get('color_column') else False
        )
        
        return fig
    
    @staticmethod
    def _create_bar_chart(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create bar chart"""
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        
        if not x_col or x_col not in df.columns:
            raise ValueError("Invalid or missing x_column for bar chart")
        
        if y_col and y_col in df.columns:
            # Grouped bar chart
            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                color=config.get('color_column'),
                title=config.get('title', f'{y_col} by {x_col}'),
                orientation=config.get('orientation', 'v')
            )
        else:
            # Count bar chart
            value_counts = df[x_col].value_counts().head(20)  # Limit to top 20
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=config.get('title', f'Count by {x_col}')
            )
        
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col or 'Count'
        )
        
        return fig
    
    @staticmethod
    def _create_line_chart(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create line chart"""
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        
        if not all([x_col, y_col]) or not all([col in df.columns for col in [x_col, y_col]]):
            raise ValueError("Invalid or missing columns for line chart")
        
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=config.get('color_column'),
            title=config.get('title', f'{y_col} over {x_col}')
        )
        
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col
        )
        
        return fig
    
    @staticmethod
    def _create_scatter_plot(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create scatter plot"""
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        
        if not all([x_col, y_col]) or not all([col in df.columns for col in [x_col, y_col]]):
            raise ValueError("Invalid or missing columns for scatter plot")
        
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=config.get('color_column'),
            size=config.get('size_column'),
            title=config.get('title', f'{y_col} vs {x_col}'),
            trendline=config.get('trendline', None)
        )
        
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col
        )
        
        return fig
    
    @staticmethod
    def _create_box_plot(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create box plot"""
        y_col = config.get('y_column')
        x_col = config.get('x_column')  # Optional grouping
        
        if not y_col or y_col not in df.columns:
            raise ValueError("Invalid or missing y_column for box plot")
        
        fig = px.box(
            df,
            x=x_col if x_col and x_col in df.columns else None,
            y=y_col,
            color=config.get('color_column'),
            title=config.get('title', f'Box Plot of {y_col}')
        )
        
        return fig
    
    @staticmethod
    def _create_heatmap(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create correlation heatmap"""
        # Use only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            raise ValueError("No numeric columns available for heatmap")
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        fig = px.imshow(
            corr_matrix,
            title=config.get('title', 'Correlation Heatmap'),
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        
        fig.update_layout(
            xaxis_title='Features',
            yaxis_title='Features'
        )
        
        return fig
    
    @staticmethod
    def _create_pie_chart(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create pie chart"""
        column = config.get('column')
        if not column or column not in df.columns:
            raise ValueError("Invalid or missing column for pie chart")
        
        # Get value counts
        value_counts = df[column].value_counts().head(10)  # Limit to top 10
        
        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=config.get('title', f'Distribution of {column}')
        )
        
        return fig
    
    @staticmethod
    def _create_violin_plot(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create violin plot"""
        y_col = config.get('y_column')
        x_col = config.get('x_column')  # Optional grouping
        
        if not y_col or y_col not in df.columns:
            raise ValueError("Invalid or missing y_column for violin plot")
        
        fig = px.violin(
            df,
            x=x_col if x_col and x_col in df.columns else None,
            y=y_col,
            color=config.get('color_column'),
            title=config.get('title', f'Violin Plot of {y_col}')
        )
        
        return fig
    
    @staticmethod
    def _create_sunburst(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create sunburst chart"""
        path_columns = config.get('path', [])
        values_column = config.get('values')
        
        if not path_columns or not all(col in df.columns for col in path_columns):
            raise ValueError("Invalid or missing path columns for sunburst")
        
        # Aggregate data for sunburst
        if values_column and values_column in df.columns:
            agg_df = df.groupby(path_columns)[values_column].sum().reset_index()
        else:
            agg_df = df.groupby(path_columns).size().reset_index(name='count')
            values_column = 'count'
        
        fig = px.sunburst(
            agg_df,
            path=path_columns,
            values=values_column,
            title=config.get('title', 'Sunburst Chart')
        )
        
        return fig
    
    @staticmethod
    def _create_treemap(df: pd.DataFrame, config: Dict) -> go.Figure:
        """Create treemap"""
        path_columns = config.get('path', [])
        values_column = config.get('values')
        
        if not path_columns or not all(col in df.columns for col in path_columns):
            raise ValueError("Invalid or missing path columns for treemap")
        
        # Aggregate data for treemap
        if values_column and values_column in df.columns:
            agg_df = df.groupby(path_columns)[values_column].sum().reset_index()
        else:
            agg_df = df.groupby(path_columns).size().reset_index(name='count')
            values_column = 'count'
        
        fig = px.treemap(
            agg_df,
            path=path_columns,
            values=values_column,
            title=config.get('title', 'Treemap')
        )
        
        return fig
    
    @staticmethod
    def get_chart_config_template(chart_type: str) -> Dict[str, Any]:
        """Get configuration template for a chart type"""
        templates = {
            'histogram': {
                'chart_type': 'histogram',
                'x_column': '',
                'bins': 30,
                'title': '',
                'color_column': None,
                'facet_column': None
            },
            'bar': {
                'chart_type': 'bar',
                'x_column': '',
                'y_column': None,
                'title': '',
                'color_column': None,
                'orientation': 'v'
            },
            'line': {
                'chart_type': 'line',
                'x_column': '',
                'y_column': '',
                'title': '',
                'color_column': None
            },
            'scatter': {
                'chart_type': 'scatter',
                'x_column': '',
                'y_column': '',
                'title': '',
                'color_column': None,
                'size_column': None,
                'trendline': None
            },
            'box': {
                'chart_type': 'box',
                'y_column': '',
                'x_column': None,
                'title': '',
                'color_column': None
            },
            'heatmap': {
                'chart_type': 'heatmap',
                'title': 'Correlation Heatmap'
            },
            'pie': {
                'chart_type': 'pie',
                'column': '',
                'title': ''
            }
        }
        
        return templates.get(chart_type, {})
    
    @staticmethod
    def export_chart_config(fig: go.Figure, config: Dict) -> Dict[str, Any]:
        """Export chart configuration and data for sharing"""
        return {
            'config': config,
            'layout': fig.layout.to_dict(),
            'data': [trace.to_dict() for trace in fig.data]
        }
