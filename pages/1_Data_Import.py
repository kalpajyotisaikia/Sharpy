import streamlit as st
import pandas as pd
import json
from utils.data_loader import DataLoader
import io

st.set_page_config(page_title="Data Import", page_icon="📁", layout="wide")

st.title("📁 Data Import")
st.markdown("Import data from various sources: CSV, JSON, APIs, or databases")

# Initialize data loader
data_loader = DataLoader()

# Tabs for different import methods
tab1, tab2, tab3, tab4 = st.tabs(["📄 File Upload", "🌐 API Import", "🗄️ Database", "📊 Sample Data"])

# Tab 1: File Upload
with tab1:
    st.subheader("Upload Data Files")
    
    upload_type = st.selectbox("Select file type:", ["CSV", "JSON"])
    
    uploaded_file = st.file_uploader(
        f"Choose a {upload_type} file",
        type=[upload_type.lower()],
        help=f"Upload your {upload_type} file to begin analysis"
    )
    
    if uploaded_file is not None:
        with st.spinner(f"Loading {upload_type} file..."):
            if upload_type == "CSV":
                df, error = data_loader.load_csv(uploaded_file)
            else:  # JSON
                df, error = data_loader.load_json(uploaded_file)
            
            if error:
                st.error(f"❌ {error}")
            else:
                # Validate data
                is_valid, validation_error = data_loader.validate_data(df)
                
                if not is_valid:
                    st.error(f"❌ {validation_error}")
                else:
                    # Store in session state
                    st.session_state.data = df
                    st.session_state.data_source = {
                        'type': upload_type.lower(),
                        'config': {'file_name': uploaded_file.name}
                    }
                    
                    st.success(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
                    
                    # Show preview
                    st.subheader("📊 Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Show data info
                    data_info = data_loader.get_data_info(df)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Rows", data_info['shape'][0])
                        st.metric("Columns", data_info['shape'][1])
                    with col2:
                        st.metric("Memory (MB)", f"{data_info['memory_usage'] / 1024**2:.2f}")
                        st.metric("Numeric Columns", data_info.get('numeric_columns', 0))
                    with col3:
                        st.metric("Categorical Columns", data_info.get('categorical_columns', 0))
                        total_nulls = sum(data_info['null_counts'].values())
                        st.metric("Total Null Values", total_nulls)

# Tab 2: API Import
with tab2:
    st.subheader("Import from API")
    
    api_url = st.text_input(
        "API URL:",
        placeholder="https://api.example.com/data",
        help="Enter the full URL of the API endpoint"
    )
    
    # Headers configuration
    st.write("**Headers (Optional):**")
    add_headers = st.checkbox("Add custom headers")
    headers = {}
    
    if add_headers:
        col1, col2 = st.columns(2)
        header_keys = []
        header_values = []
        
        for i in range(3):  # Allow up to 3 headers
            with col1:
                key = st.text_input(f"Header Key {i+1}:", key=f"header_key_{i}")
                if key:
                    header_keys.append(key)
            with col2:
                value = st.text_input(f"Header Value {i+1}:", key=f"header_value_{i}")
                if key:
                    header_values.append(value)
        
        headers = dict(zip(header_keys, header_values))
    
    # Parameters configuration
    st.write("**Query Parameters (Optional):**")
    add_params = st.checkbox("Add query parameters")
    params = {}
    
    if add_params:
        param_text = st.text_area(
            "Parameters (JSON format):",
            placeholder='{"limit": 100, "format": "json"}',
            help="Enter parameters as JSON"
        )
        
        if param_text:
            try:
                params = json.loads(param_text)
            except json.JSONDecodeError:
                st.error("Invalid JSON format for parameters")
    
    if st.button("🔄 Load Data from API", type="primary"):
        if not api_url:
            st.error("Please enter an API URL")
        else:
            with st.spinner("Fetching data from API..."):
                df, error = data_loader.load_from_api(api_url, headers, params)
                
                if error:
                    st.error(f"❌ {error}")
                else:
                    # Validate data
                    is_valid, validation_error = data_loader.validate_data(df)
                    
                    if not is_valid:
                        st.error(f"❌ {validation_error}")
                    else:
                        # Store in session state
                        st.session_state.data = df
                        st.session_state.data_source = {
                            'type': 'api',
                            'config': {
                                'url': api_url,
                                'headers': headers,
                                'params': params
                            }
                        }
                        
                        st.success(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
                        
                        # Show preview
                        st.subheader("📊 Data Preview")
                        st.dataframe(df.head(10), use_container_width=True)

# Tab 3: Database
with tab3:
    st.subheader("Import from Database")
    
    # Connection options
    connection_method = st.radio(
        "Connection Method:",
        ["Environment Variable (DATABASE_URL)", "Custom Connection String"]
    )
    
    connection_string = None
    if connection_method == "Custom Connection String":
        connection_string = st.text_input(
            "Connection String:",
            placeholder="postgresql://user:password@host:port/database",
            type="password",
            help="Enter your database connection string"
        )
    
    # SQL Query
    sql_query = st.text_area(
        "SQL Query:",
        placeholder="SELECT * FROM your_table LIMIT 1000;",
        height=150,
        help="Enter your SQL query to fetch data"
    )
    
    if st.button("🔄 Execute Query", type="primary"):
        if not sql_query:
            st.error("Please enter a SQL query")
        else:
            with st.spinner("Executing query..."):
                df, error = data_loader.load_from_database(sql_query, connection_string)
                
                if error:
                    st.error(f"❌ {error}")
                else:
                    # Validate data
                    is_valid, validation_error = data_loader.validate_data(df)
                    
                    if not is_valid:
                        st.error(f"❌ {validation_error}")
                    else:
                        # Store in session state
                        st.session_state.data = df
                        st.session_state.data_source = {
                            'type': 'database',
                            'config': {
                                'query': sql_query,
                                'connection_string': connection_string or 'Environment Variable'
                            }
                        }
                        
                        st.success(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
                        
                        # Show preview
                        st.subheader("📊 Data Preview")
                        st.dataframe(df.head(10), use_container_width=True)

# Tab 4: Sample Data
with tab4:
    st.subheader("Load Sample Datasets")
    st.info("Use sample datasets to explore the tool's features")
    
    sample_datasets = {
        "E-commerce Sales": {
            "description": "Online store sales data with products, customers, and transactions",
            "columns": ["date", "product_id", "category", "price", "quantity", "customer_id", "region"],
            "rows": 1000
        },
        "Marketing Campaign": {
            "description": "Digital marketing campaign performance data",
            "columns": ["campaign_id", "channel", "impressions", "clicks", "conversions", "cost", "date"],
            "rows": 500
        },
        "Financial Stock Data": {
            "description": "Stock price and volume data for multiple companies",
            "columns": ["symbol", "date", "open", "high", "low", "close", "volume"],
            "rows": 750
        }
    }
    
    selected_dataset = st.selectbox(
        "Choose a sample dataset:",
        list(sample_datasets.keys())
    )
    
    if selected_dataset:
        dataset_info = sample_datasets[selected_dataset]
        st.write(f"**Description:** {dataset_info['description']}")
        st.write(f"**Columns:** {', '.join(dataset_info['columns'])}")
        st.write(f"**Rows:** {dataset_info['rows']}")
        
        if st.button("📊 Load Sample Dataset", type="primary"):
            with st.spinner("Generating sample data..."):
                # Generate sample data based on selection
                import numpy as np
                
                np.random.seed(42)  # For reproducible results
                
                if selected_dataset == "E-commerce Sales":
                    df = pd.DataFrame({
                        'date': pd.date_range('2024-01-01', periods=1000, freq='H'),
                        'product_id': np.random.choice(range(1, 101), 1000),
                        'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Sports'], 1000),
                        'price': np.random.uniform(10, 500, 1000).round(2),
                        'quantity': np.random.randint(1, 10, 1000),
                        'customer_id': np.random.choice(range(1, 201), 1000),
                        'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], 1000)
                    })
                    df['revenue'] = df['price'] * df['quantity']
                
                elif selected_dataset == "Marketing Campaign":
                    df = pd.DataFrame({
                        'campaign_id': np.random.choice(range(1, 21), 500),
                        'channel': np.random.choice(['Google Ads', 'Facebook', 'Instagram', 'Email', 'Display'], 500),
                        'impressions': np.random.randint(1000, 100000, 500),
                        'clicks': np.random.randint(10, 5000, 500),
                        'conversions': np.random.randint(1, 200, 500),
                        'cost': np.random.uniform(50, 2000, 500).round(2),
                        'date': pd.date_range('2024-01-01', periods=500)
                    })
                    df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
                    df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
                    df['cpc'] = (df['cost'] / df['clicks']).round(2)
                
                else:  # Financial Stock Data
                    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
                    df_list = []
                    for symbol in symbols:
                        dates = pd.date_range('2024-01-01', periods=150)
                        base_price = np.random.uniform(100, 300)
                        prices = base_price + np.cumsum(np.random.normal(0, 5, 150))
                        
                        symbol_df = pd.DataFrame({
                            'symbol': symbol,
                            'date': dates,
                            'open': prices + np.random.uniform(-2, 2, 150),
                            'high': prices + np.random.uniform(0, 5, 150),
                            'low': prices + np.random.uniform(-5, 0, 150),
                            'close': prices,
                            'volume': np.random.randint(1000000, 10000000, 150)
                        })
                        df_list.append(symbol_df)
                    
                    df = pd.concat(df_list, ignore_index=True)
                
                # Store in session state
                st.session_state.data = df
                st.session_state.data_source = {
                    'type': 'sample',
                    'config': {'dataset': selected_dataset}
                }
                
                st.success(f"✅ Successfully loaded {selected_dataset} dataset")
                st.subheader("📊 Data Preview")
                st.dataframe(df.head(10), use_container_width=True)

# Current data status
st.markdown("---")
if st.session_state.data is not None:
    st.success(f"✅ **Current Dataset:** {len(st.session_state.data)} rows × {len(st.session_state.data.columns)} columns")
    
    if st.button("🔄 Clear Current Dataset"):
        st.session_state.data = None
        st.session_state.data_source = None
        st.session_state.analysis_results = None
        st.session_state.visualizations = []
        st.rerun()
else:
    st.info("ℹ️ No dataset loaded. Please import data using one of the methods above.")
