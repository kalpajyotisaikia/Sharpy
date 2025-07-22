import pandas as pd
import requests
import json
import io
import streamlit as st
from typing import Dict, Any, Optional, Tuple
import sqlalchemy as sa
import os

class DataLoader:
    """Handles data loading from various sources"""
    
    @staticmethod
    def load_csv(file_data) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Load data from CSV file"""
        try:
            df = pd.read_csv(file_data)
            return df, None
        except Exception as e:
            return None, f"Error loading CSV: {str(e)}"
    
    @staticmethod
    def load_json(file_data) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Load data from JSON file"""
        try:
            # Try to read as JSON
            data = json.load(file_data)
            
            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # If it's a dict, try to find the main data array
                if len(data) == 1:
                    key = list(data.keys())[0]
                    if isinstance(data[key], list):
                        df = pd.DataFrame(data[key])
                    else:
                        df = pd.DataFrame([data])
                else:
                    df = pd.DataFrame([data])
            else:
                return None, "JSON format not supported"
                
            return df, None
        except Exception as e:
            return None, f"Error loading JSON: {str(e)}"
    
    @staticmethod
    def load_from_api(url: str, headers: Optional[Dict] = None, params: Optional[Dict] = None) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Load data from API endpoint"""
        try:
            if headers is None:
                headers = {}
            if params is None:
                params = {}
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            # Try to parse as JSON
            try:
                data = response.json()
                
                # Handle different response structures
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                elif isinstance(data, dict):
                    # Look for common data keys
                    data_keys = ['data', 'results', 'items', 'records', 'rows']
                    found_data = None
                    
                    for key in data_keys:
                        if key in data and isinstance(data[key], list):
                            found_data = data[key]
                            break
                    
                    if found_data:
                        df = pd.DataFrame(found_data)
                    else:
                        # If no array found, treat the dict as a single record
                        df = pd.DataFrame([data])
                else:
                    return None, "API response format not supported"
                    
                return df, None
                
            except json.JSONDecodeError:
                return None, "API response is not valid JSON"
                
        except requests.exceptions.RequestException as e:
            return None, f"Error fetching data from API: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"
    
    @staticmethod
    def load_from_database(query: str, connection_string: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Load data from database using SQL query"""
        try:
            # Use provided connection string or get from environment
            if connection_string is None:
                connection_string = os.getenv("DATABASE_URL")
                
            if not connection_string:
                return None, "No database connection string provided"
            
            engine = sa.create_engine(connection_string)
            df = pd.read_sql(query, engine)
            engine.dispose()
            
            return df, None
            
        except Exception as e:
            return None, f"Database error: {str(e)}"
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """Validate loaded data"""
        if df is None:
            return False, "Data is None"
        
        if df.empty:
            return False, "Data is empty"
        
        if len(df.columns) == 0:
            return False, "No columns found"
        
        # Check for reasonable size limits
        if len(df) > 1000000:  # 1M rows
            return False, "Dataset too large (>1M rows). Please use a smaller dataset."
        
        if len(df.columns) > 1000:
            return False, "Too many columns (>1000). Please use a dataset with fewer columns."
        
        return True, None
    
    @staticmethod
    def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
        """Get comprehensive information about the dataset"""
        info = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'null_counts': df.isnull().sum().to_dict(),
            'null_percentage': (df.isnull().sum() / len(df) * 100).to_dict()
        }
        
        # Basic statistics for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            info['numeric_summary'] = df[numeric_cols].describe().to_dict()
        
        # Unique values for categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        info['categorical_info'] = {}
        for col in categorical_cols:
            unique_count = df[col].nunique()
            info['categorical_info'][col] = {
                'unique_count': unique_count,
                'top_values': df[col].value_counts().head(5).to_dict() if unique_count < 1000 else {}
            }
        
        return info
