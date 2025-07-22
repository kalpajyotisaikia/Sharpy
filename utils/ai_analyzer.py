import json
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import streamlit as st

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
from openai import OpenAI

class AIAnalyzer:
    """AI-powered data analysis using OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Check if AI analyzer is available"""
        return self.client is not None
    
    def analyze_dataset_overview(self, df: pd.DataFrame, data_info: Dict) -> Dict[str, Any]:
        """Generate comprehensive dataset analysis"""
        if not self.is_available():
            return {"error": "OpenAI API key not available"}
        
        try:
            # Prepare dataset summary for AI
            summary = self._prepare_dataset_summary(df, data_info)
            
            prompt = f"""
            Analyze this dataset and provide insights in JSON format:
            
            Dataset Summary:
            {json.dumps(summary, indent=2, default=str)}
            
            Sample Data (first 5 rows):
            {df.head().to_json(orient='records', indent=2)}
            
            Please provide analysis in JSON format with these keys:
            - "summary": Brief overview of the dataset
            - "key_insights": List of 3-5 important observations
            - "data_quality": Assessment of data quality issues
            - "recommended_analyses": List of suggested analysis approaches
            - "visualization_suggestions": List of recommended chart types with reasons
            - "business_questions": List of business questions this data could answer
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert data analyst. Provide thorough, actionable insights about datasets."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {"error": f"AI analysis failed: {str(e)}"}
    
    def suggest_visualizations(self, df: pd.DataFrame, column_subset: Optional[List[str]] = None) -> Dict[str, Any]:
        """Suggest appropriate visualizations for specific columns"""
        if not self.is_available():
            return {"error": "OpenAI API key not available"}
        
        try:
            # Use subset of columns if specified, otherwise analyze all
            cols_to_analyze = column_subset if column_subset else df.columns.tolist()
            
            # Prepare column analysis
            column_info = {}
            for col in cols_to_analyze[:20]:  # Limit to prevent token overflow
                col_data = df[col]
                column_info[col] = {
                    "dtype": str(col_data.dtype),
                    "null_count": int(col_data.isnull().sum()),
                    "unique_count": int(col_data.nunique()),
                    "sample_values": col_data.dropna().head(5).tolist()
                }
                
                if col_data.dtype in ['int64', 'float64']:
                    column_info[col]["stats"] = {
                        "min": float(col_data.min()),
                        "max": float(col_data.max()),
                        "mean": float(col_data.mean()),
                        "std": float(col_data.std())
                    }
            
            prompt = f"""
            Suggest visualizations for this dataset based on column analysis:
            
            Columns to analyze: {cols_to_analyze}
            
            Column Information:
            {json.dumps(column_info, indent=2, default=str)}
            
            Dataset shape: {df.shape}
            
            Provide recommendations in JSON format with these keys:
            - "single_column_charts": List of charts for individual columns
            - "multi_column_charts": List of charts comparing multiple columns
            - "advanced_analyses": List of complex visualizations (correlations, distributions, etc.)
            
            For each chart suggestion, include:
            - "chart_type": Type of chart (bar, line, scatter, histogram, etc.)
            - "columns": Columns to use
            - "title": Suggested chart title
            - "reason": Why this visualization is recommended
            - "insights": What insights this chart might reveal
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a data visualization expert. Recommend the most appropriate and insightful charts."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {"error": f"Visualization suggestion failed: {str(e)}"}
    
    def analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations and relationships in the data"""
        if not self.is_available():
            return {"error": "OpenAI API key not available"}
        
        try:
            # Get numeric columns for correlation analysis
            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                return {"error": "No numeric columns available for correlation analysis"}
            
            # Calculate correlations
            correlations = numeric_df.corr()
            
            # Find strong correlations (>0.7 or <-0.7)
            strong_correlations = []
            for i in range(len(correlations.columns)):
                for j in range(i+1, len(correlations.columns)):
                    corr_val = correlations.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        strong_correlations.append({
                            "col1": correlations.columns[i],
                            "col2": correlations.columns[j],
                            "correlation": float(corr_val)
                        })
            
            prompt = f"""
            Analyze these correlations and provide insights:
            
            Strong Correlations (>0.7 or <-0.7):
            {json.dumps(strong_correlations, indent=2)}
            
            Full Correlation Matrix:
            {correlations.to_json(indent=2)}
            
            Column Information:
            {json.dumps({col: {"mean": float(numeric_df[col].mean()), "std": float(numeric_df[col].std())} for col in numeric_df.columns}, indent=2)}
            
            Provide analysis in JSON format:
            - "correlation_insights": List of key findings about relationships
            - "strongest_relationships": Analysis of the strongest correlations
            - "recommendations": Suggested follow-up analyses
            - "potential_causations": Possible causal relationships to investigate
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a statistical analyst expert in correlation analysis and causation inference."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            result["correlation_matrix"] = correlations.to_dict()
            result["strong_correlations"] = strong_correlations
            return result
            
        except Exception as e:
            return {"error": f"Correlation analysis failed: {str(e)}"}
    
    def generate_insights_for_column(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Generate detailed insights for a specific column"""
        if not self.is_available():
            return {"error": "OpenAI API key not available"}
        
        if column not in df.columns:
            return {"error": f"Column '{column}' not found in dataset"}
        
        try:
            col_data = df[column]
            
            # Prepare column analysis
            analysis = {
                "column_name": column,
                "dtype": str(col_data.dtype),
                "total_count": len(col_data),
                "null_count": int(col_data.isnull().sum()),
                "unique_count": int(col_data.nunique()),
            }
            
            if col_data.dtype in ['int64', 'float64']:
                analysis.update({
                    "min": float(col_data.min()),
                    "max": float(col_data.max()),
                    "mean": float(col_data.mean()),
                    "median": float(col_data.median()),
                    "std": float(col_data.std()),
                    "quartiles": col_data.quantile([0.25, 0.5, 0.75]).to_dict()
                })
            else:
                analysis["top_values"] = col_data.value_counts().head(10).to_dict()
            
            prompt = f"""
            Analyze this column in detail and provide insights:
            
            Column Analysis:
            {json.dumps(analysis, indent=2, default=str)}
            
            Sample Values:
            {col_data.dropna().head(20).tolist()}
            
            Provide detailed analysis in JSON format:
            - "summary": Brief description of the column
            - "data_quality": Assessment of data quality (nulls, outliers, etc.)
            - "distribution_insights": Insights about the data distribution
            - "anomalies": Any unusual patterns or outliers detected
            - "recommendations": Suggested data cleaning or analysis steps
            - "visualization_suggestions": Best charts for this column
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a data quality expert specializing in column-level analysis."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            result["column_stats"] = analysis
            return result
            
        except Exception as e:
            return {"error": f"Column analysis failed: {str(e)}"}
    
    def _prepare_dataset_summary(self, df: pd.DataFrame, data_info: Dict) -> Dict:
        """Prepare a concise dataset summary for AI analysis"""
        return {
            "shape": data_info["shape"],
            "columns": data_info["columns"][:20],  # Limit columns to prevent token overflow
            "data_types": {k: str(v) for k, v in data_info["dtypes"].items()},
            "memory_usage_mb": round(data_info["memory_usage"] / 1024**2, 2),
            "null_percentages": {k: round(v, 2) for k, v in data_info["null_percentage"].items() if v > 0},
            "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
            "categorical_columns": len(df.select_dtypes(include=['object', 'category']).columns),
            "datetime_columns": len(df.select_dtypes(include=['datetime64']).columns)
        }
