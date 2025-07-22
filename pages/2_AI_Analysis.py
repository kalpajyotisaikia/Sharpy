import streamlit as st
import pandas as pd
import numpy as np
from utils.ai_analyzer import AIAnalyzer
from utils.data_loader import DataLoader
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="AI Analysis", page_icon="🤖", layout="wide")

st.title("🤖 AI-Powered Analysis")
st.markdown("Get intelligent insights about your data using advanced AI models")

# Check if data is loaded
if st.session_state.data is None:
    st.warning("⚠️ No data loaded. Please go to the Data Import page first.")
    st.stop()

# Initialize AI analyzer
ai_analyzer = AIAnalyzer()

# Check if AI is available
if not ai_analyzer.is_available():
    st.error("❌ OpenAI API key not available. AI features are disabled.")
    st.info("Please ensure the OPENAI_API_KEY environment variable is set.")
    st.stop()

df = st.session_state.data
data_loader = DataLoader()
data_info = data_loader.get_data_info(df)

# Analysis tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview Analysis", "🔍 Column Analysis", "🔗 Correlations", "📊 Custom Insights"])

# Tab 1: Overview Analysis
with tab1:
    st.subheader("📋 Dataset Overview Analysis")
    
    if st.button("🚀 Generate AI Analysis", type="primary", key="overview_analysis"):
        with st.spinner("🤖 AI is analyzing your dataset..."):
            analysis_results = ai_analyzer.analyze_dataset_overview(df, data_info)
            
            if "error" in analysis_results:
                st.error(f"❌ {analysis_results['error']}")
            else:
                # Store results in session state
                st.session_state.analysis_results = analysis_results
                
                # Display results
                st.success("✅ Analysis complete!")
                
                # Summary
                if 'summary' in analysis_results:
                    st.subheader("📝 Summary")
                    st.info(analysis_results['summary'])
                
                # Key Insights
                if 'key_insights' in analysis_results:
                    st.subheader("💡 Key Insights")
                    for i, insight in enumerate(analysis_results['key_insights'], 1):
                        st.write(f"{i}. {insight}")
                
                # Data Quality Assessment
                if 'data_quality' in analysis_results:
                    st.subheader("✅ Data Quality")
                    st.write(analysis_results['data_quality'])
                
                # Recommended Analyses
                if 'recommended_analyses' in analysis_results:
                    st.subheader("🎯 Recommended Analyses")
                    for analysis in analysis_results['recommended_analyses']:
                        st.write(f"• {analysis}")
                
                # Visualization Suggestions
                if 'visualization_suggestions' in analysis_results:
                    st.subheader("📈 Visualization Suggestions")
                    for suggestion in analysis_results['visualization_suggestions']:
                        st.write(f"• {suggestion}")
                
                # Business Questions
                if 'business_questions' in analysis_results:
                    st.subheader("❓ Business Questions This Data Can Answer")
                    for question in analysis_results['business_questions']:
                        st.write(f"• {question}")
    
    # Show existing analysis if available
    if st.session_state.analysis_results and 'error' not in st.session_state.analysis_results:
        analysis_results = st.session_state.analysis_results
        
        st.markdown("---")
        st.subheader("📊 Current Analysis Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'summary' in analysis_results:
                st.write("**📝 Summary:**")
                st.info(analysis_results['summary'])
            
            if 'key_insights' in analysis_results:
                st.write("**💡 Key Insights:**")
                for i, insight in enumerate(analysis_results['key_insights'], 1):
                    st.write(f"{i}. {insight}")
        
        with col2:
            if 'data_quality' in analysis_results:
                st.write("**✅ Data Quality:**")
                st.write(analysis_results['data_quality'])
            
            if 'recommended_analyses' in analysis_results:
                st.write("**🎯 Recommended:**")
                for analysis in analysis_results['recommended_analyses']:
                    st.write(f"• {analysis}")

# Tab 2: Column Analysis
with tab2:
    st.subheader("🔍 Individual Column Analysis")
    
    # Column selector
    selected_column = st.selectbox("Select a column to analyze:", df.columns.tolist())
    
    if st.button("🔬 Analyze Column", type="primary", key="column_analysis"):
        with st.spinner(f"🤖 Analyzing column '{selected_column}'..."):
            column_analysis = ai_analyzer.generate_insights_for_column(df, selected_column)
            
            if "error" in column_analysis:
                st.error(f"❌ {column_analysis['error']}")
            else:
                st.success("✅ Column analysis complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Column Statistics
                    if 'column_stats' in column_analysis:
                        st.subheader("📊 Column Statistics")
                        stats = column_analysis['column_stats']
                        
                        st.write(f"**Type:** {stats['dtype']}")
                        st.write(f"**Total Count:** {stats['total_count']:,}")
                        st.write(f"**Unique Values:** {stats['unique_count']:,}")
                        st.write(f"**Null Count:** {stats['null_count']:,}")
                        
                        if 'mean' in stats:
                            st.write(f"**Mean:** {stats['mean']:.2f}")
                            st.write(f"**Median:** {stats['median']:.2f}")
                            st.write(f"**Std Dev:** {stats['std']:.2f}")
                
                with col2:
                    # AI Insights
                    if 'summary' in column_analysis:
                        st.subheader("🤖 AI Summary")
                        st.info(column_analysis['summary'])
                
                # Data Quality
                if 'data_quality' in column_analysis:
                    st.subheader("✅ Data Quality Assessment")
                    st.write(column_analysis['data_quality'])
                
                # Distribution Insights
                if 'distribution_insights' in column_analysis:
                    st.subheader("📈 Distribution Insights")
                    st.write(column_analysis['distribution_insights'])
                
                # Anomalies
                if 'anomalies' in column_analysis:
                    st.subheader("⚠️ Anomalies Detected")
                    st.write(column_analysis['anomalies'])
                
                # Recommendations
                if 'recommendations' in column_analysis:
                    st.subheader("💡 Recommendations")
                    for rec in column_analysis['recommendations']:
                        st.write(f"• {rec}")
    
    # Quick column visualization
    st.markdown("---")
    st.subheader("📊 Quick Column Visualization")
    
    if selected_column:
        col_data = df[selected_column]
        
        if col_data.dtype in ['int64', 'float64']:
            # Numeric column
            fig = px.histogram(df, x=selected_column, title=f'Distribution of {selected_column}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Categorical column
            value_counts = col_data.value_counts().head(15)
            fig = px.bar(x=value_counts.index, y=value_counts.values, 
                        title=f'Top Values in {selected_column}')
            fig.update_layout(xaxis_title=selected_column, yaxis_title='Count')
            st.plotly_chart(fig, use_container_width=True)

# Tab 3: Correlations
with tab3:
    st.subheader("🔗 Correlation Analysis")
    
    # Check if there are numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_columns) < 2:
        st.warning("⚠️ Need at least 2 numeric columns for correlation analysis.")
    else:
        if st.button("🔍 Analyze Correlations", type="primary", key="correlation_analysis"):
            with st.spinner("🤖 Analyzing correlations..."):
                correlation_analysis = ai_analyzer.analyze_correlations(df)
                
                if "error" in correlation_analysis:
                    st.error(f"❌ {correlation_analysis['error']}")
                else:
                    st.success("✅ Correlation analysis complete!")
                    
                    # Correlation Matrix Visualization
                    st.subheader("📊 Correlation Matrix")
                    corr_matrix = pd.DataFrame(correlation_analysis['correlation_matrix'])
                    
                    fig = px.imshow(
                        corr_matrix,
                        title='Correlation Heatmap',
                        color_continuous_scale='RdBu',
                        aspect='auto',
                        text_auto=True
                    )
                    fig.update_layout(height=600)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Strong Correlations
                        if 'strong_correlations' in correlation_analysis:
                            st.subheader("💪 Strong Correlations")
                            strong_corr = correlation_analysis['strong_correlations']
                            
                            if strong_corr:
                                for corr in strong_corr:
                                    correlation_val = corr['correlation']
                                    correlation_str = f"{correlation_val:+.3f}"
                                    color = "🔴" if correlation_val > 0 else "🔵"
                                    st.write(f"{color} **{corr['col1']}** ↔ **{corr['col2']}**: {correlation_str}")
                            else:
                                st.info("No strong correlations found (>0.7 or <-0.7)")
                    
                    with col2:
                        # AI Insights
                        if 'correlation_insights' in correlation_analysis:
                            st.subheader("🤖 AI Insights")
                            for insight in correlation_analysis['correlation_insights']:
                                st.write(f"• {insight}")
                    
                    # Strongest Relationships
                    if 'strongest_relationships' in correlation_analysis:
                        st.subheader("🎯 Strongest Relationships Analysis")
                        st.write(correlation_analysis['strongest_relationships'])
                    
                    # Potential Causations
                    if 'potential_causations' in correlation_analysis:
                        st.subheader("🔗 Potential Causal Relationships")
                        for causation in correlation_analysis['potential_causations']:
                            st.write(f"• {causation}")
                    
                    # Recommendations
                    if 'recommendations' in correlation_analysis:
                        st.subheader("💡 Follow-up Recommendations")
                        for rec in correlation_analysis['recommendations']:
                            st.write(f"• {rec}")

# Tab 4: Custom Insights
with tab4:
    st.subheader("📊 Custom AI Insights")
    st.markdown("Ask specific questions about your data and get AI-powered answers.")
    
    # Custom question input
    custom_question = st.text_area(
        "Ask a question about your data:",
        placeholder="e.g., What are the main trends in this dataset? Which columns are most important? What patterns should I investigate further?",
        height=100
    )
    
    # Column subset selector
    st.write("**Focus on specific columns (optional):**")
    selected_columns = st.multiselect(
        "Select columns to focus the analysis on:",
        df.columns.tolist(),
        help="Leave empty to analyze all columns"
    )
    
    if st.button("🎯 Get Custom Insights", type="primary", key="custom_insights"):
        if not custom_question.strip():
            st.warning("Please enter a question about your data.")
        else:
            with st.spinner("🤖 AI is analyzing your question..."):
                try:
                    # Prepare data summary for the custom question
                    analysis_data = {
                        'question': custom_question,
                        'columns': selected_columns if selected_columns else df.columns.tolist(),
                        'shape': df.shape,
                        'sample_data': df.head(5).to_dict(),
                        'data_types': df.dtypes.to_dict(),
                        'basic_stats': {}
                    }
                    
                    # Add basic statistics for numeric columns
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    for col in numeric_cols:
                        if not selected_columns or col in selected_columns:
                            analysis_data['basic_stats'][col] = {
                                'mean': float(df[col].mean()),
                                'std': float(df[col].std()),
                                'min': float(df[col].min()),
                                'max': float(df[col].max())
                            }
                    
                    # Use OpenAI for custom analysis
                    from openai import OpenAI
                    import json
                    import os
                    
                    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    
                    prompt = f"""
                    Analyze this dataset and answer the user's question with specific insights:
                    
                    User Question: {custom_question}
                    
                    Dataset Information:
                    {json.dumps(analysis_data, indent=2, default=str)}
                    
                    Please provide a comprehensive answer in JSON format with these keys:
                    - "answer": Direct answer to the user's question
                    - "specific_insights": List of specific findings related to the question
                    - "data_evidence": Evidence from the data that supports your insights
                    - "recommendations": Actionable recommendations based on the analysis
                    - "follow_up_questions": Suggested follow-up questions for deeper analysis
                    """
                    
                    response = client.chat.completions.create(
                        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
                        # do not change this unless explicitly requested by the user
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are an expert data analyst. Provide detailed, actionable insights based on the data provided."},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.3
                    )
                    
                    custom_insights = json.loads(response.choices[0].message.content)
                    
                    st.success("✅ Custom analysis complete!")
                    
                    # Display results
                    if 'answer' in custom_insights:
                        st.subheader("💬 Answer")
                        st.info(custom_insights['answer'])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if 'specific_insights' in custom_insights:
                            st.subheader("🔍 Specific Insights")
                            for insight in custom_insights['specific_insights']:
                                st.write(f"• {insight}")
                        
                        if 'data_evidence' in custom_insights:
                            st.subheader("📊 Data Evidence")
                            for evidence in custom_insights['data_evidence']:
                                st.write(f"• {evidence}")
                    
                    with col2:
                        if 'recommendations' in custom_insights:
                            st.subheader("💡 Recommendations")
                            for rec in custom_insights['recommendations']:
                                st.write(f"• {rec}")
                        
                        if 'follow_up_questions' in custom_insights:
                            st.subheader("❓ Follow-up Questions")
                            for question in custom_insights['follow_up_questions']:
                                st.write(f"• {question}")
                
                except Exception as e:
                    st.error(f"❌ Error generating custom insights: {str(e)}")

# Sidebar: Quick Stats
with st.sidebar:
    st.header("📈 Dataset Quick Stats")
    st.metric("Rows", f"{len(df):,}")
    st.metric("Columns", len(df.columns))
    
    # Memory usage
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    st.metric("Memory", f"{memory_mb:.1f} MB")
    
    # Null values
    total_nulls = df.isnull().sum().sum()
    st.metric("Null Values", f"{total_nulls:,}")
    
    # Data types
    st.write("**Column Types:**")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        st.write(f"• {dtype}: {count}")
    
    st.markdown("---")
    st.write("💡 **Tip:** Start with the Overview Analysis to get comprehensive insights about your dataset!")
