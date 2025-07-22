import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import json

class CodeGenerator:
    """Generate reproducible code for data analysis and visualizations"""
    
    @staticmethod
    def generate_data_loading_code(source_type: str, source_config: Dict) -> str:
        """Generate code for data loading"""
        if source_type == 'csv':
            return f"""
# Data Loading - CSV
import pandas as pd

# Load data from CSV
df = pd.read_csv('{source_config.get("file_path", "data.csv")}')
print(f"Dataset shape: {{df.shape}}")
print("\\nFirst 5 rows:")
print(df.head())
"""
        
        elif source_type == 'json':
            return f"""
# Data Loading - JSON
import pandas as pd
import json

# Load data from JSON
with open('{source_config.get("file_path", "data.json")}', 'r') as f:
    data = json.load(f)

# Convert to DataFrame (adjust based on JSON structure)
df = pd.DataFrame(data)
print(f"Dataset shape: {{df.shape}}")
print("\\nFirst 5 rows:")
print(df.head())
"""
        
        elif source_type == 'api':
            return f"""
# Data Loading - API
import pandas as pd
import requests

# API Configuration
url = '{source_config.get("url", "")}'
headers = {source_config.get("headers", {})}
params = {source_config.get("params", {})}

# Fetch data from API
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

# Convert to DataFrame
data = response.json()
df = pd.DataFrame(data)  # Adjust based on API response structure
print(f"Dataset shape: {{df.shape}}")
print("\\nFirst 5 rows:")
print(df.head())
"""
        
        elif source_type == 'database':
            return f"""
# Data Loading - Database
import pandas as pd
import sqlalchemy as sa

# Database connection
connection_string = '{source_config.get("connection_string", "postgresql://user:pass@host:port/db")}'
engine = sa.create_engine(connection_string)

# Execute query
query = '''
{source_config.get("query", "SELECT * FROM table_name")}
'''

df = pd.read_sql(query, engine)
engine.dispose()

print(f"Dataset shape: {{df.shape}}")
print("\\nFirst 5 rows:")
print(df.head())
"""
        
        return "# Data loading code not available for this source type"
    
    @staticmethod
    def generate_data_exploration_code(df: pd.DataFrame) -> str:
        """Generate code for basic data exploration"""
        return f"""
# Data Exploration
import pandas as pd
import numpy as np

# Basic information
print("Dataset Info:")
print(f"Shape: {{df.shape}}")
print(f"Columns: {{df.columns.tolist()}}")
print("\\nData types:")
print(df.dtypes)

print("\\nBasic statistics:")
print(df.describe())

# Missing values analysis
print("\\nMissing values:")
missing_counts = df.isnull().sum()
missing_percentages = (missing_counts / len(df)) * 100
missing_info = pd.DataFrame({{
    'Missing_Count': missing_counts,
    'Missing_Percentage': missing_percentages
}})
print(missing_info[missing_info['Missing_Count'] > 0])

# Memory usage
print(f"\\nMemory usage: {{df.memory_usage(deep=True).sum() / 1024**2:.2f}} MB")

# Unique values for categorical columns
categorical_cols = df.select_dtypes(include=['object', 'category']).columns
if len(categorical_cols) > 0:
    print("\\nCategorical columns unique values:")
    for col in categorical_cols:
        unique_count = df[col].nunique()
        print(f"{{col}}: {{unique_count}} unique values")
        if unique_count <= 10:
            print(f"  Values: {{df[col].value_counts().head().to_dict()}}")
"""
    
    @staticmethod
    def generate_visualization_code(chart_config: Dict) -> str:
        """Generate code for creating visualizations"""
        chart_type = chart_config.get('chart_type', '').lower()
        
        base_imports = """
# Visualization
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

"""
        
        if chart_type == 'histogram':
            return base_imports + f"""
# Create histogram
fig = px.histogram(
    df,
    x='{chart_config.get("x_column", "")}',
    title='{chart_config.get("title", "")}',
    nbins={chart_config.get("bins", 30)},
    {f'color="{chart_config.get("color_column")}",' if chart_config.get("color_column") else ''}
)

fig.update_layout(
    xaxis_title='{chart_config.get("x_column", "")}',
    yaxis_title='Count'
)

fig.show()
"""
        
        elif chart_type == 'bar':
            y_col = chart_config.get('y_column')
            if y_col:
                return base_imports + f"""
# Create bar chart
fig = px.bar(
    df,
    x='{chart_config.get("x_column", "")}',
    y='{y_col}',
    title='{chart_config.get("title", "")}',
    {f'color="{chart_config.get("color_column")}",' if chart_config.get("color_column") else ''}
)

fig.update_layout(
    xaxis_title='{chart_config.get("x_column", "")}',
    yaxis_title='{y_col}'
)

fig.show()
"""
            else:
                return base_imports + f"""
# Create count bar chart
value_counts = df['{chart_config.get("x_column", "")}'].value_counts().head(20)
fig = px.bar(
    x=value_counts.index,
    y=value_counts.values,
    title='{chart_config.get("title", "")}'
)

fig.update_layout(
    xaxis_title='{chart_config.get("x_column", "")}',
    yaxis_title='Count'
)

fig.show()
"""
        
        elif chart_type == 'line':
            return base_imports + f"""
# Create line chart
fig = px.line(
    df,
    x='{chart_config.get("x_column", "")}',
    y='{chart_config.get("y_column", "")}',
    title='{chart_config.get("title", "")}',
    {f'color="{chart_config.get("color_column")}",' if chart_config.get("color_column") else ''}
)

fig.update_layout(
    xaxis_title='{chart_config.get("x_column", "")}',
    yaxis_title='{chart_config.get("y_column", "")}'
)

fig.show()
"""
        
        elif chart_type == 'scatter':
            return base_imports + f"""
# Create scatter plot
fig = px.scatter(
    df,
    x='{chart_config.get("x_column", "")}',
    y='{chart_config.get("y_column", "")}',
    title='{chart_config.get("title", "")}',
    {f'color="{chart_config.get("color_column")}",' if chart_config.get("color_column") else ''}
    {f'size="{chart_config.get("size_column")}",' if chart_config.get("size_column") else ''}
    {f'trendline="{chart_config.get("trendline")}",' if chart_config.get("trendline") else ''}
)

fig.update_layout(
    xaxis_title='{chart_config.get("x_column", "")}',
    yaxis_title='{chart_config.get("y_column", "")}'
)

fig.show()
"""
        
        elif chart_type == 'heatmap':
            return base_imports + f"""
# Create correlation heatmap
numeric_df = df.select_dtypes(include=[np.number])
corr_matrix = numeric_df.corr()

fig = px.imshow(
    corr_matrix,
    title='{chart_config.get("title", "Correlation Heatmap")}',
    color_continuous_scale='RdBu',
    aspect='auto'
)

fig.update_layout(
    xaxis_title='Features',
    yaxis_title='Features'
)

fig.show()
"""
        
        return base_imports + "# Visualization code not available for this chart type"
    
    @staticmethod
    def generate_analysis_code(analysis_type: str, columns: List[str] = None) -> str:
        """Generate code for specific analysis tasks"""
        
        if analysis_type == 'correlation_analysis':
            return """
# Correlation Analysis
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Get numeric columns only
numeric_df = df.select_dtypes(include=[np.number])

# Calculate correlation matrix
corr_matrix = numeric_df.corr()

print("Correlation Matrix:")
print(corr_matrix)

# Find strong correlations (>0.7 or <-0.7)
strong_correlations = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        corr_val = corr_matrix.iloc[i, j]
        if abs(corr_val) > 0.7:
            strong_correlations.append({
                'col1': corr_matrix.columns[i],
                'col2': corr_matrix.columns[j],
                'correlation': corr_val
            })

print("\\nStrong Correlations (>0.7 or <-0.7):")
for corr in strong_correlations:
    print(f"{corr['col1']} - {corr['col2']}: {corr['correlation']:.3f}")

# Visualize correlation matrix
fig = px.imshow(corr_matrix, 
                title='Correlation Heatmap',
                color_continuous_scale='RdBu',
                aspect='auto')
fig.show()
"""
        
        elif analysis_type == 'outlier_detection':
            return """
# Outlier Detection
import pandas as pd
import numpy as np

# Get numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns

outlier_summary = {}

for col in numeric_cols:
    # IQR method for outlier detection
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define outlier bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Find outliers
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    
    outlier_summary[col] = {
        'outlier_count': len(outliers),
        'outlier_percentage': len(outliers) / len(df) * 100,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outlier_values': outliers[col].tolist()[:10]  # First 10 outliers
    }

print("Outlier Analysis:")
for col, info in outlier_summary.items():
    if info['outlier_count'] > 0:
        print(f"\\n{col}:")
        print(f"  Outliers: {info['outlier_count']} ({info['outlier_percentage']:.2f}%)")
        print(f"  Bounds: [{info['lower_bound']:.2f}, {info['upper_bound']:.2f}]")
        print(f"  Sample outlier values: {info['outlier_values'][:5]}")
"""
        
        elif analysis_type == 'missing_values':
            return """
# Missing Values Analysis
import pandas as pd
import numpy as np

# Calculate missing values
missing_counts = df.isnull().sum()
missing_percentages = (missing_counts / len(df)) * 100

# Create missing values summary
missing_summary = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': missing_counts,
    'Missing_Percentage': missing_percentages,
    'Data_Type': df.dtypes
})

# Filter to show only columns with missing values
missing_summary = missing_summary[missing_summary['Missing_Count'] > 0]
missing_summary = missing_summary.sort_values('Missing_Percentage', ascending=False)

print("Missing Values Analysis:")
print(missing_summary)

# Strategies for handling missing values
print("\\nSuggested strategies:")
for _, row in missing_summary.iterrows():
    col = row['Column']
    pct = row['Missing_Percentage']
    dtype = row['Data_Type']
    
    if pct > 50:
        print(f"{col}: Consider dropping column (>{pct:.1f}% missing)")
    elif dtype in ['object', 'category']:
        print(f"{col}: Fill with mode or 'Unknown' ({pct:.1f}% missing)")
    else:
        print(f"{col}: Fill with mean/median ({pct:.1f}% missing)")

# Example code for handling missing values
print("\\n# Example missing value handling:")
print("# For numeric columns - fill with median")
print("df_cleaned = df.copy()")
print("numeric_cols = df.select_dtypes(include=[np.number]).columns")
print("df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].median())")
print("\\n# For categorical columns - fill with mode")
print("categorical_cols = df.select_dtypes(include=['object', 'category']).columns")
print("for col in categorical_cols:")
print("    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])")
"""
        
        return "# Analysis code not available for this type"
    
    @staticmethod
    def generate_complete_notebook(data_source: Dict, analysis_results: Dict, visualizations: List[Dict]) -> str:
        """Generate a complete Jupyter notebook with all analysis"""
        notebook_code = f"""
# Complete Data Analysis Notebook
# Generated by DevData Analytics

{CodeGenerator.generate_data_loading_code(data_source.get('type', 'csv'), data_source.get('config', {}))}

{CodeGenerator.generate_data_exploration_code(pd.DataFrame())}

# AI Analysis Summary
print("AI-Generated Insights:")
print("{analysis_results.get('summary', 'No summary available')}")

print("\\nKey Insights:")
for insight in analysis_results.get('key_insights', []):
    print(f"- {insight}")

print("\\nRecommended Analyses:")
for recommendation in analysis_results.get('recommended_analyses', []):
    print(f"- {recommendation}")

# Visualizations
"""
        
        for i, viz in enumerate(visualizations):
            notebook_code += f"\n# Visualization {i+1}: {viz.get('title', 'Chart')}\n"
            notebook_code += CodeGenerator.generate_visualization_code(viz)
            notebook_code += "\n"
        
        return notebook_code
    
    @staticmethod
    def generate_sql_queries(df: pd.DataFrame, table_name: str = "data_table") -> Dict[str, str]:
        """Generate useful SQL queries for the dataset"""
        queries = {}
        
        # Basic queries
        queries['select_all'] = f"SELECT * FROM {table_name} LIMIT 100;"
        queries['row_count'] = f"SELECT COUNT(*) as total_rows FROM {table_name};"
        queries['column_info'] = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';"
        
        # Numeric columns analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col_stats = ", ".join([f"AVG({col}) as avg_{col}, MIN({col}) as min_{col}, MAX({col}) as max_{col}" for col in numeric_cols[:5]])
            queries['numeric_summary'] = f"SELECT {col_stats} FROM {table_name};"
        
        # Categorical analysis
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
            queries[f'{col}_distribution'] = f"SELECT {col}, COUNT(*) as count FROM {table_name} GROUP BY {col} ORDER BY count DESC LIMIT 10;"
        
        # Missing values
        null_checks = []
        for col in df.columns[:10]:  # Check first 10 columns
            null_checks.append(f"SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) as {col}_nulls")
        
        if null_checks:
            queries['null_analysis'] = f"SELECT {', '.join(null_checks)} FROM {table_name};"
        
        return queries
