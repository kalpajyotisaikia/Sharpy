import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.visualization import VisualizationEngine
from utils.ai_analyzer import AIAnalyzer

st.set_page_config(page_title="Visualizations", page_icon="📈", layout="wide")

st.title("📈 Interactive Visualizations")
st.markdown("Create powerful, interactive charts and get AI-powered visualization recommendations")

# Check if data is loaded
if st.session_state.data is None:
    st.warning("⚠️ No data loaded. Please go to the Data Import page first.")
    st.stop()

df = st.session_state.data
viz_engine = VisualizationEngine()
ai_analyzer = AIAnalyzer()

# Initialize visualizations in session state
if 'visualizations' not in st.session_state:
    st.session_state.visualizations = []

# Tabs for different visualization methods
tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Suggestions", "🛠️ Chart Builder", "📊 Gallery", "🎨 Advanced"])

# Tab 1: AI Suggestions
with tab1:
    st.subheader("🤖 AI-Powered Visualization Suggestions")
    
    if ai_analyzer.is_available():
        # Column selector for focused suggestions
        st.write("**Focus on specific columns (optional):**")
        selected_columns = st.multiselect(
            "Select columns to focus suggestions on:",
            df.columns.tolist(),
            help="Leave empty for general dataset suggestions"
        )
        
        if st.button("🎯 Get AI Visualization Suggestions", type="primary", key="viz_suggestions"):
            with st.spinner("🤖 AI is analyzing your data for visualization opportunities..."):
                viz_suggestions = ai_analyzer.suggest_visualizations(df, selected_columns)
                
                if "error" in viz_suggestions:
                    st.error(f"❌ {viz_suggestions['error']}")
                else:
                    st.success("✅ AI suggestions generated!")
                    
                    # Single Column Charts
                    if 'single_column_charts' in viz_suggestions:
                        st.subheader("📊 Single Column Visualizations")
                        
                        for i, chart in enumerate(viz_suggestions['single_column_charts']):
                            with st.expander(f"📈 {chart.get('title', 'Chart')} ({chart.get('chart_type', 'Chart').title()})"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.write(f"**Chart Type:** {chart.get('chart_type', 'N/A').title()}")
                                    st.write(f"**Columns:** {', '.join(chart.get('columns', []))}")
                                    st.write(f"**Reason:** {chart.get('reason', 'N/A')}")
                                    st.write(f"**Insights:** {chart.get('insights', 'N/A')}")
                                
                                with col2:
                                    if st.button("Create Chart", key=f"single_chart_{i}"):
                                        # Create chart configuration
                                        chart_config = {
                                            'chart_type': chart.get('chart_type', '').lower(),
                                            'title': chart.get('title', ''),
                                        }
                                        
                                        columns = chart.get('columns', [])
                                        if columns and len(columns) > 0:
                                            chart_config['x_column'] = columns[0]
                                            if len(columns) > 1:
                                                chart_config['y_column'] = columns[1]
                                        
                                        # Create and store visualization
                                        try:
                                            fig = viz_engine.create_chart(df, chart_config)
                                            if fig:
                                                st.session_state.visualizations.append({
                                                    'figure': fig,
                                                    'config': chart_config,
                                                    'title': chart.get('title', 'Chart'),
                                                    'type': 'ai_suggested'
                                                })
                                                st.success("Chart created and added to gallery!")
                                                st.rerun()
                                        except Exception as e:
                                            st.error(f"Error creating chart: {str(e)}")
                    
                    # Multi-Column Charts
                    if 'multi_column_charts' in viz_suggestions:
                        st.subheader("🔗 Multi-Column Visualizations")
                        
                        for i, chart in enumerate(viz_suggestions['multi_column_charts']):
                            with st.expander(f"📈 {chart.get('title', 'Chart')} ({chart.get('chart_type', 'Chart').title()})"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.write(f"**Chart Type:** {chart.get('chart_type', 'N/A').title()}")
                                    st.write(f"**Columns:** {', '.join(chart.get('columns', []))}")
                                    st.write(f"**Reason:** {chart.get('reason', 'N/A')}")
                                    st.write(f"**Insights:** {chart.get('insights', 'N/A')}")
                                
                                with col2:
                                    if st.button("Create Chart", key=f"multi_chart_{i}"):
                                        # Create chart configuration
                                        chart_config = {
                                            'chart_type': chart.get('chart_type', '').lower(),
                                            'title': chart.get('title', ''),
                                        }
                                        
                                        columns = chart.get('columns', [])
                                        if columns and len(columns) > 0:
                                            chart_config['x_column'] = columns[0]
                                            if len(columns) > 1:
                                                chart_config['y_column'] = columns[1]
                                            if len(columns) > 2:
                                                chart_config['color_column'] = columns[2]
                                        
                                        try:
                                            fig = viz_engine.create_chart(df, chart_config)
                                            if fig:
                                                st.session_state.visualizations.append({
                                                    'figure': fig,
                                                    'config': chart_config,
                                                    'title': chart.get('title', 'Chart'),
                                                    'type': 'ai_suggested'
                                                })
                                                st.success("Chart created and added to gallery!")
                                                st.rerun()
                                        except Exception as e:
                                            st.error(f"Error creating chart: {str(e)}")
                    
                    # Advanced Analyses
                    if 'advanced_analyses' in viz_suggestions:
                        st.subheader("🎯 Advanced Visualizations")
                        
                        for i, chart in enumerate(viz_suggestions['advanced_analyses']):
                            with st.expander(f"📈 {chart.get('title', 'Chart')} ({chart.get('chart_type', 'Chart').title()})"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.write(f"**Chart Type:** {chart.get('chart_type', 'N/A').title()}")
                                    st.write(f"**Columns:** {', '.join(chart.get('columns', []))}")
                                    st.write(f"**Reason:** {chart.get('reason', 'N/A')}")
                                    st.write(f"**Insights:** {chart.get('insights', 'N/A')}")
                                
                                with col2:
                                    if st.button("Create Chart", key=f"advanced_chart_{i}"):
                                        chart_config = {
                                            'chart_type': chart.get('chart_type', '').lower(),
                                            'title': chart.get('title', ''),
                                        }
                                        
                                        columns = chart.get('columns', [])
                                        if chart.get('chart_type', '').lower() == 'heatmap':
                                            # Special handling for heatmap
                                            pass
                                        elif columns and len(columns) > 0:
                                            chart_config['x_column'] = columns[0]
                                            if len(columns) > 1:
                                                chart_config['y_column'] = columns[1]
                                        
                                        try:
                                            fig = viz_engine.create_chart(df, chart_config)
                                            if fig:
                                                st.session_state.visualizations.append({
                                                    'figure': fig,
                                                    'config': chart_config,
                                                    'title': chart.get('title', 'Chart'),
                                                    'type': 'ai_suggested'
                                                })
                                                st.success("Chart created and added to gallery!")
                                                st.rerun()
                                        except Exception as e:
                                            st.error(f"Error creating chart: {str(e)}")
    else:
        st.warning("⚠️ AI features unavailable. OpenAI API key required for visualization suggestions.")

# Tab 2: Chart Builder
with tab2:
    st.subheader("🛠️ Custom Chart Builder")
    
    # Chart type selector
    chart_types = {
        'Histogram': 'histogram',
        'Bar Chart': 'bar',
        'Line Chart': 'line',
        'Scatter Plot': 'scatter',
        'Box Plot': 'box',
        'Correlation Heatmap': 'heatmap',
        'Pie Chart': 'pie',
        'Violin Plot': 'violin'
    }
    
    selected_chart_type = st.selectbox("Select Chart Type:", list(chart_types.keys()))
    chart_type_code = chart_types[selected_chart_type]
    
    # Get chart configuration template
    config = viz_engine.get_chart_config_template(chart_type_code)
    config['chart_type'] = chart_type_code
    
    # Dynamic configuration based on chart type
    col1, col2 = st.columns(2)
    
    with col1:
        if 'x_column' in config:
            config['x_column'] = st.selectbox("X-Axis Column:", [''] + df.columns.tolist())
        
        if 'y_column' in config:
            y_options = [''] + df.select_dtypes(include=[np.number]).columns.tolist()
            config['y_column'] = st.selectbox("Y-Axis Column:", y_options)
        
        if 'column' in config:  # For pie charts
            config['column'] = st.selectbox("Column:", [''] + df.columns.tolist())
    
    with col2:
        if 'color_column' in config:
            config['color_column'] = st.selectbox("Color Column (optional):", [''] + df.columns.tolist())
            if config['color_column'] == '':
                config['color_column'] = None
        
        if 'size_column' in config:
            size_options = [''] + df.select_dtypes(include=[np.number]).columns.tolist()
            config['size_column'] = st.selectbox("Size Column (optional):", size_options)
            if config['size_column'] == '':
                config['size_column'] = None
        
        if 'bins' in config:
            config['bins'] = st.slider("Number of Bins:", 10, 100, 30)
    
    # Title
    config['title'] = st.text_input("Chart Title:", config.get('title', f"{selected_chart_type} - {config.get('x_column', 'Chart')}"))
    
    # Additional options
    if chart_type_code == 'scatter':
        config['trendline'] = st.selectbox("Trendline (optional):", ['', 'ols', 'lowess'])
        if config['trendline'] == '':
            config['trendline'] = None
    
    # Create chart button
    if st.button("🎨 Create Chart", type="primary", key="create_custom_chart"):
        try:
            # Validate required fields
            required_filled = True
            if 'x_column' in config and not config['x_column']:
                required_filled = False
            if 'y_column' in config and config['y_column'] is not None and not config['y_column']:
                required_filled = False
            if 'column' in config and not config['column']:
                required_filled = False
            
            if not required_filled:
                st.error("Please fill in all required fields.")
            else:
                fig = viz_engine.create_chart(df, config)
                if fig:
                    st.session_state.visualizations.append({
                        'figure': fig,
                        'config': config.copy(),
                        'title': config['title'],
                        'type': 'custom'
                    })
                    st.success("Chart created successfully!")
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")

# Tab 3: Gallery
with tab3:
    st.subheader("📊 Visualization Gallery")
    
    if not st.session_state.visualizations:
        st.info("No visualizations created yet. Use the AI Suggestions or Chart Builder to create charts.")
    else:
        # Gallery controls
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**Total Charts:** {len(st.session_state.visualizations)}")
        with col2:
            if st.button("🗑️ Clear All", key="clear_all_viz"):
                st.session_state.visualizations = []
                st.rerun()
        with col3:
            export_format = st.selectbox("Export Format:", ["PNG", "HTML", "JSON"])
        
        st.markdown("---")
        
        # Display visualizations
        for i, viz in enumerate(st.session_state.visualizations):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.subheader(f"📈 {viz['title']}")
                    st.plotly_chart(viz['figure'], use_container_width=True)
                
                with col2:
                    st.write(f"**Type:** {viz['type'].replace('_', ' ').title()}")
                    st.write(f"**Chart:** {viz['config']['chart_type'].title()}")
                    
                    # Chart info
                    if 'x_column' in viz['config'] and viz['config']['x_column']:
                        st.write(f"**X-Axis:** {viz['config']['x_column']}")
                    if 'y_column' in viz['config'] and viz['config']['y_column']:
                        st.write(f"**Y-Axis:** {viz['config']['y_column']}")
                    
                    # Actions
                    st.markdown("**Actions:**")
                    
                    if st.button("🗑️ Delete", key=f"delete_viz_{i}"):
                        st.session_state.visualizations.pop(i)
                        st.rerun()
                    
                    # Export individual chart
                    if export_format == "PNG":
                        if st.button("📁 Export PNG", key=f"export_png_{i}"):
                            try:
                                img_bytes = viz['figure'].to_image(format="png", width=1200, height=800)
                                st.download_button(
                                    label="⬇️ Download PNG",
                                    data=img_bytes,
                                    file_name=f"{viz['title'].replace(' ', '_')}.png",
                                    mime="image/png",
                                    key=f"download_png_{i}"
                                )
                            except Exception as e:
                                st.error(f"Export failed: {str(e)}")
                    
                    elif export_format == "HTML":
                        if st.button("📁 Export HTML", key=f"export_html_{i}"):
                            html_str = viz['figure'].to_html(include_plotlyjs='cdn')
                            st.download_button(
                                label="⬇️ Download HTML",
                                data=html_str,
                                file_name=f"{viz['title'].replace(' ', '_')}.html",
                                mime="text/html",
                                key=f"download_html_{i}"
                            )
                
                st.markdown("---")

# Tab 4: Advanced
with tab4:
    st.subheader("🎨 Advanced Visualizations")
    
    # Quick analysis charts
    st.write("**Quick Analysis Charts:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Data Overview Dashboard"):
            # Create multiple charts for overview
            charts_created = 0
            
            # Correlation heatmap for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                config = {'chart_type': 'heatmap', 'title': 'Correlation Matrix'}
                fig = viz_engine.create_chart(df, config)
                if fig:
                    st.session_state.visualizations.append({
                        'figure': fig,
                        'config': config,
                        'title': 'Correlation Matrix',
                        'type': 'overview'
                    })
                    charts_created += 1
            
            # Distribution of numeric columns
            for col in numeric_cols[:3]:  # First 3 numeric columns
                config = {
                    'chart_type': 'histogram',
                    'x_column': col,
                    'title': f'Distribution of {col}',
                    'bins': 30
                }
                fig = viz_engine.create_chart(df, config)
                if fig:
                    st.session_state.visualizations.append({
                        'figure': fig,
                        'config': config,
                        'title': f'Distribution of {col}',
                        'type': 'overview'
                    })
                    charts_created += 1
            
            # Categorical distributions
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            for col in categorical_cols[:2]:  # First 2 categorical columns
                config = {
                    'chart_type': 'bar',
                    'x_column': col,
                    'title': f'Count by {col}'
                }
                fig = viz_engine.create_chart(df, config)
                if fig:
                    st.session_state.visualizations.append({
                        'figure': fig,
                        'config': config,
                        'title': f'Count by {col}',
                        'type': 'overview'
                    })
                    charts_created += 1
            
            if charts_created > 0:
                st.success(f"Created {charts_created} overview charts!")
                st.rerun()
            else:
                st.warning("Could not create overview charts with current data.")
    
    with col2:
        if st.button("🔍 Missing Values Analysis"):
            # Create visualizations for missing values
            null_counts = df.isnull().sum()
            null_data = null_counts[null_counts > 0]
            
            if len(null_data) > 0:
                # Bar chart of missing values
                fig = px.bar(
                    x=null_data.index,
                    y=null_data.values,
                    title='Missing Values by Column'
                )
                fig.update_layout(xaxis_title='Column', yaxis_title='Missing Count')
                
                st.session_state.visualizations.append({
                    'figure': fig,
                    'config': {'chart_type': 'bar', 'title': 'Missing Values by Column'},
                    'title': 'Missing Values Analysis',
                    'type': 'analysis'
                })
                st.success("Missing values chart created!")
                st.rerun()
            else:
                st.info("No missing values found in the dataset.")
    
    with col3:
        if st.button("📈 Data Quality Dashboard"):
            charts_created = 0
            
            # Numeric columns statistics
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Box plots for numeric columns
                for col in numeric_cols[:3]:
                    config = {
                        'chart_type': 'box',
                        'y_column': col,
                        'title': f'Box Plot - {col}'
                    }
                    fig = viz_engine.create_chart(df, config)
                    if fig:
                        st.session_state.visualizations.append({
                            'figure': fig,
                            'config': config,
                            'title': f'Box Plot - {col}',
                            'type': 'quality'
                        })
                        charts_created += 1
            
            if charts_created > 0:
                st.success(f"Created {charts_created} data quality charts!")
                st.rerun()
            else:
                st.warning("Could not create quality charts with current data.")
    
    st.markdown("---")
    
    # Custom multi-chart dashboard
    st.subheader("🎯 Custom Dashboard Builder")
    
    dashboard_cols = st.multiselect(
        "Select columns for dashboard analysis:",
        df.columns.tolist(),
        help="Choose 2-6 columns to create a focused dashboard"
    )
    
    if len(dashboard_cols) >= 2:
        if st.button("🚀 Create Custom Dashboard"):
            charts_created = 0
            
            # Create different charts for the selected columns
            numeric_dashboard_cols = [col for col in dashboard_cols if df[col].dtype in ['int64', 'float64']]
            categorical_dashboard_cols = [col for col in dashboard_cols if df[col].dtype in ['object', 'category']]
            
            # Scatter plots for numeric columns
            for i, col1 in enumerate(numeric_dashboard_cols):
                for col2 in numeric_dashboard_cols[i+1:]:
                    config = {
                        'chart_type': 'scatter',
                        'x_column': col1,
                        'y_column': col2,
                        'title': f'{col1} vs {col2}'
                    }
                    fig = viz_engine.create_chart(df, config)
                    if fig:
                        st.session_state.visualizations.append({
                            'figure': fig,
                            'config': config,
                            'title': f'{col1} vs {col2}',
                            'type': 'dashboard'
                        })
                        charts_created += 1
            
            # Distributions for selected columns
            for col in dashboard_cols[:4]:  # Limit to 4 distributions
                if df[col].dtype in ['int64', 'float64']:
                    config = {
                        'chart_type': 'histogram',
                        'x_column': col,
                        'title': f'Distribution: {col}',
                        'bins': 25
                    }
                else:
                    config = {
                        'chart_type': 'bar',
                        'x_column': col,
                        'title': f'Count: {col}'
                    }
                
                fig = viz_engine.create_chart(df, config)
                if fig:
                    st.session_state.visualizations.append({
                        'figure': fig,
                        'config': config,
                        'title': f'Distribution: {col}',
                        'type': 'dashboard'
                    })
                    charts_created += 1
            
            if charts_created > 0:
                st.success(f"Custom dashboard created with {charts_created} charts!")
                st.rerun()
            else:
                st.warning("Could not create dashboard charts.")

# Sidebar: Visualization Summary
with st.sidebar:
    st.header("📊 Visualization Summary")
    
    if st.session_state.visualizations:
        total_charts = len(st.session_state.visualizations)
        st.metric("Total Charts", total_charts)
        
        # Chart type breakdown
        chart_types = {}
        for viz in st.session_state.visualizations:
            chart_type = viz['config']['chart_type']
            chart_types[chart_type] = chart_types.get(chart_type, 0) + 1
        
        st.write("**Chart Types:**")
        for chart_type, count in chart_types.items():
            st.write(f"• {chart_type.title()}: {count}")
        
        # Source breakdown
        sources = {}
        for viz in st.session_state.visualizations:
            source = viz['type']
            sources[source] = sources.get(source, 0) + 1
        
        st.write("**Sources:**")
        for source, count in sources.items():
            st.write(f"• {source.replace('_', ' ').title()}: {count}")
    else:
        st.info("No visualizations yet")
    
    st.markdown("---")
    st.write("💡 **Tips:**")
    st.write("• Use AI suggestions for intelligent chart recommendations")
    st.write("• Try the overview dashboard for quick insights")
    st.write("• Export charts in multiple formats")
