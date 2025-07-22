import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import base64
from datetime import datetime
import zipfile
from utils.visualization import VisualizationEngine

st.set_page_config(page_title="Share & Export", page_icon="🔗", layout="wide")

st.title("🔗 Share & Export")
st.markdown("Share your visualizations and export comprehensive analysis reports")

# Check if data is loaded
if st.session_state.data is None:
    st.warning("⚠️ No data loaded. Please go to the Data Import page first.")
    st.stop()

df = st.session_state.data
viz_engine = VisualizationEngine()

# Tabs for different sharing and export options
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualization Export", "📋 Analysis Report", "🔗 Shareable Links", "📱 Presentation Mode"])

# Tab 1: Visualization Export
with tab1:
    st.subheader("📊 Visualization Export")
    st.markdown("Export your visualizations in various formats for sharing and publication")
    
    if not st.session_state.get('visualizations'):
        st.info("No visualizations created yet. Go to the Visualizations page to create charts first.")
    else:
        # Visualization selector
        viz_titles = [f"{i+1}. {viz['title']}" for i, viz in enumerate(st.session_state.visualizations)]
        
        export_mode = st.radio(
            "Export mode:",
            ["Individual Charts", "All Charts", "Custom Selection"]
        )
        
        selected_vizs = []
        
        if export_mode == "Individual Charts":
            selected_idx = st.selectbox("Select visualization:", range(len(viz_titles)), format_func=lambda x: viz_titles[x])
            selected_vizs = [st.session_state.visualizations[selected_idx]]
        
        elif export_mode == "All Charts":
            selected_vizs = st.session_state.visualizations
        
        elif export_mode == "Custom Selection":
            selected_indices = st.multiselect(
                "Select visualizations to export:",
                range(len(viz_titles)),
                format_func=lambda x: viz_titles[x],
                default=list(range(min(3, len(viz_titles))))
            )
            selected_vizs = [st.session_state.visualizations[i] for i in selected_indices]
        
        if selected_vizs:
            st.write(f"**Selected:** {len(selected_vizs)} visualization(s)")
            
            # Export format options
            col1, col2 = st.columns(2)
            
            with col1:
                export_format = st.selectbox(
                    "Export format:",
                    ["PNG (High Quality)", "HTML (Interactive)", "PDF (Print Ready)", "SVG (Vector)", "JSON (Data)"]
                )
            
            with col2:
                if export_format == "PNG (High Quality)":
                    image_size = st.selectbox("Image size:", ["1200x800", "1920x1080", "800x600", "Custom"])
                    if image_size == "Custom":
                        width = st.number_input("Width (px):", value=1200, min_value=400, max_value=4000)
                        height = st.number_input("Height (px):", value=800, min_value=300, max_value=3000)
                        image_size = f"{width}x{height}"
            
            # Export button
            if st.button("🎨 Export Visualizations", type="primary"):
                try:
                    if export_format == "PNG (High Quality)":
                        width, height = map(int, image_size.split('x'))
                        
                        if len(selected_vizs) == 1:
                            # Single image export
                            viz = selected_vizs[0]
                            img_bytes = viz['figure'].to_image(format="png", width=width, height=height, scale=2)
                            
                            st.download_button(
                                label="📥 Download PNG",
                                data=img_bytes,
                                file_name=f"{viz['title'].replace(' ', '_')}.png",
                                mime="image/png"
                            )
                        else:
                            # Multiple images in ZIP
                            zip_buffer = io.BytesIO()
                            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                for i, viz in enumerate(selected_vizs):
                                    img_bytes = viz['figure'].to_image(format="png", width=width, height=height, scale=2)
                                    filename = f"{i+1:02d}_{viz['title'].replace(' ', '_')}.png"
                                    zip_file.writestr(filename, img_bytes)
                            
                            zip_buffer.seek(0)
                            st.download_button(
                                label="📥 Download PNG Archive",
                                data=zip_buffer.getvalue(),
                                file_name=f"visualizations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                                mime="application/zip"
                            )
                    
                    elif export_format == "HTML (Interactive)":
                        if len(selected_vizs) == 1:
                            # Single HTML export
                            viz = selected_vizs[0]
                            html_str = viz['figure'].to_html(
                                include_plotlyjs='cdn',
                                config={'displayModeBar': True, 'responsive': True}
                            )
                            
                            st.download_button(
                                label="📥 Download HTML",
                                data=html_str,
                                file_name=f"{viz['title'].replace(' ', '_')}.html",
                                mime="text/html"
                            )
                        else:
                            # Multiple HTML files in ZIP or combined dashboard
                            dashboard_option = st.radio("HTML export option:", ["Combined Dashboard", "Separate Files"])
                            
                            if dashboard_option == "Combined Dashboard":
                                # Create combined HTML dashboard
                                dashboard_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .chart-container {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 20px; border-radius: 5px; }}
        .chart-title {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
        .dashboard-header {{ text-align: center; margin-bottom: 40px; }}
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>Data Analysis Dashboard</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
                                
                                for i, viz in enumerate(selected_vizs):
                                    chart_div = f"chart_{i}"
                                    dashboard_html += f"""
    <div class="chart-container">
        <div class="chart-title">{viz['title']}</div>
        <div id="{chart_div}"></div>
    </div>
"""
                                
                                dashboard_html += "\n<script>\n"
                                
                                for i, viz in enumerate(selected_vizs):
                                    chart_div = f"chart_{i}"
                                    fig_json = viz['figure'].to_json()
                                    dashboard_html += f"""
var figure_{i} = {fig_json};
Plotly.newPlot('{chart_div}', figure_{i}.data, figure_{i}.layout, {{responsive: true}});
"""
                                
                                dashboard_html += """
</script>
</body>
</html>
"""
                                
                                st.download_button(
                                    label="📥 Download Dashboard HTML",
                                    data=dashboard_html,
                                    file_name=f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                                    mime="text/html"
                                )
                            else:
                                # Separate HTML files
                                zip_buffer = io.BytesIO()
                                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                    for i, viz in enumerate(selected_vizs):
                                        html_str = viz['figure'].to_html(include_plotlyjs='cdn')
                                        filename = f"{i+1:02d}_{viz['title'].replace(' ', '_')}.html"
                                        zip_file.writestr(filename, html_str)
                                
                                zip_buffer.seek(0)
                                st.download_button(
                                    label="📥 Download HTML Archive",
                                    data=zip_buffer.getvalue(),
                                    file_name=f"visualizations_html_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                                    mime="application/zip"
                                )
                    
                    elif export_format == "JSON (Data)":
                        # Export chart configurations and data
                        export_data = {
                            "metadata": {
                                "exported_at": datetime.now().isoformat(),
                                "tool": "DevData Analytics",
                                "dataset_info": {
                                    "rows": len(df),
                                    "columns": len(df.columns)
                                }
                            },
                            "visualizations": []
                        }
                        
                        for viz in selected_vizs:
                            viz_data = {
                                "title": viz['title'],
                                "config": viz['config'],
                                "type": viz['type'],
                                "figure_data": viz['figure'].to_dict()
                            }
                            export_data["visualizations"].append(viz_data)
                        
                        json_str = json.dumps(export_data, indent=2, default=str)
                        
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name=f"visualizations_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    st.success("✅ Export prepared! Use the download button above.")
                    
                except Exception as e:
                    st.error(f"❌ Export failed: {str(e)}")

# Tab 2: Analysis Report
with tab2:
    st.subheader("📋 Comprehensive Analysis Report")
    st.markdown("Generate professional analysis reports with insights, visualizations, and recommendations")
    
    # Report configuration
    st.write("**Report Configuration:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_executive_summary = st.checkbox("Executive Summary", value=True)
        include_data_overview = st.checkbox("Dataset Overview", value=True)
        include_ai_insights = st.checkbox("AI-Generated Insights", value=True)
        include_visualizations = st.checkbox("Key Visualizations", value=True)
    
    with col2:
        include_methodology = st.checkbox("Methodology Section", value=True)
        include_recommendations = st.checkbox("Recommendations", value=True)
        include_appendix = st.checkbox("Technical Appendix", value=False)
        include_code_snippets = st.checkbox("Code Examples", value=False)
    
    # Report format
    report_format = st.selectbox("Report format:", ["HTML", "Markdown", "Text"])
    
    if st.button("📊 Generate Analysis Report", type="primary"):
        with st.spinner("Generating comprehensive analysis report..."):
            try:
                # Get analysis data
                analysis_results = st.session_state.get('analysis_results', {})
                visualizations = st.session_state.get('visualizations', [])
                data_source = st.session_state.get('data_source', {})
                
                if report_format == "HTML":
                    report_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; color: #333; }}
        .header {{ text-align: center; border-bottom: 3px solid #007acc; padding-bottom: 20px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #007acc; border-left: 4px solid #007acc; padding-left: 10px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
        .insight {{ background: #e8f4fd; padding: 15px; border-left: 4px solid #007acc; margin: 10px 0; }}
        .recommendation {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 10px 0; }}
        .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Data Analysis Report</h1>
        <p>Generated by DevData Analytics on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
"""
                
                    if include_executive_summary:
                        summary = analysis_results.get('summary', 'This analysis provides insights into the dataset characteristics, patterns, and recommendations for further investigation.')
                        report_content += f"""
    <div class="section">
        <h2>Executive Summary</h2>
        <p>{summary}</p>
    </div>
"""
                    
                    if include_data_overview:
                        numeric_cols = len(df.select_dtypes(include=['int64', 'float64']).columns)
                        categorical_cols = len(df.select_dtypes(include=['object', 'category']).columns)
                        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
                        null_count = df.isnull().sum().sum()
                        
                        report_content += f"""
    <div class="section">
        <h2>Dataset Overview</h2>
        <div class="metric">
            <strong>Total Records:</strong> {len(df):,}
        </div>
        <div class="metric">
            <strong>Total Columns:</strong> {len(df.columns)}
        </div>
        <div class="metric">
            <strong>Numeric Columns:</strong> {numeric_cols}
        </div>
        <div class="metric">
            <strong>Categorical Columns:</strong> {categorical_cols}
        </div>
        <div class="metric">
            <strong>Memory Usage:</strong> {memory_mb:.1f} MB
        </div>
        <div class="metric">
            <strong>Missing Values:</strong> {null_count:,}
        </div>
        
        <h3>Column Information</h3>
        <ul>
"""
                        for col in df.columns:
                            dtype = str(df[col].dtype)
                            null_pct = (df[col].isnull().sum() / len(df)) * 100
                            report_content += f"<li><strong>{col}</strong> ({dtype}) - {null_pct:.1f}% missing</li>"
                        
                        report_content += "</ul></div>"
                    
                    if include_ai_insights and analysis_results:
                        report_content += """
    <div class="section">
        <h2>AI-Generated Insights</h2>
"""
                        
                        if 'key_insights' in analysis_results:
                            for insight in analysis_results['key_insights']:
                                report_content += f'<div class="insight">{insight}</div>'
                        
                        if 'data_quality' in analysis_results:
                            report_content += f"""
        <h3>Data Quality Assessment</h3>
        <p>{analysis_results['data_quality']}</p>
"""
                        
                        report_content += "</div>"
                    
                    if include_visualizations and visualizations:
                        report_content += f"""
    <div class="section">
        <h2>Key Visualizations</h2>
        <p>This analysis includes {len(visualizations)} visualizations:</p>
        <ul>
"""
                        for viz in visualizations:
                            report_content += f"<li><strong>{viz['title']}</strong> - {viz['config']['chart_type'].title()} chart</li>"
                        
                        report_content += "</ul></div>"
                    
                    if include_recommendations and analysis_results.get('recommended_analyses'):
                        report_content += """
    <div class="section">
        <h2>Recommendations</h2>
"""
                        for rec in analysis_results['recommended_analyses']:
                            report_content += f'<div class="recommendation">{rec}</div>'
                        
                        report_content += "</div>"
                    
                    if include_methodology:
                        report_content += f"""
    <div class="section">
        <h2>Methodology</h2>
        <p>This analysis was conducted using DevData Analytics, an AI-powered data analysis tool. The methodology included:</p>
        <ul>
            <li>Data import and validation from {data_source.get('type', 'unknown').title()} source</li>
            <li>Automated data profiling and quality assessment</li>
            <li>AI-powered pattern recognition and insight generation using GPT-4o</li>
            <li>Interactive visualization creation using Plotly</li>
            <li>Statistical analysis and correlation detection</li>
        </ul>
    </div>
"""
                    
                    report_content += f"""
    <div class="footer">
        <p>Report generated by <strong>DevData Analytics</strong><br>
        AI-Powered Data Analysis Tool</p>
    </div>
</body>
</html>
"""
                
                elif report_format == "Markdown":
                    report_content = f"""# Data Analysis Report

*Generated by DevData Analytics on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*

---

"""
                    
                    if include_executive_summary:
                        summary = analysis_results.get('summary', 'This analysis provides insights into the dataset characteristics, patterns, and recommendations for further investigation.')
                        report_content += f"""## Executive Summary

{summary}

"""
                    
                    if include_data_overview:
                        numeric_cols = len(df.select_dtypes(include=['int64', 'float64']).columns)
                        categorical_cols = len(df.select_dtypes(include=['object', 'category']).columns)
                        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
                        null_count = df.isnull().sum().sum()
                        
                        report_content += f"""## Dataset Overview

| Metric | Value |
|--------|-------|
| Total Records | {len(df):,} |
| Total Columns | {len(df.columns)} |
| Numeric Columns | {numeric_cols} |
| Categorical Columns | {categorical_cols} |
| Memory Usage | {memory_mb:.1f} MB |
| Missing Values | {null_count:,} |

### Column Information

"""
                        for col in df.columns:
                            dtype = str(df[col].dtype)
                            null_pct = (df[col].isnull().sum() / len(df)) * 100
                            report_content += f"- **{col}** ({dtype}) - {null_pct:.1f}% missing\n"
                        
                        report_content += "\n"
                    
                    if include_ai_insights and analysis_results:
                        report_content += "## AI-Generated Insights\n\n"
                        
                        if 'key_insights' in analysis_results:
                            for insight in analysis_results['key_insights']:
                                report_content += f"> {insight}\n\n"
                        
                        if 'data_quality' in analysis_results:
                            report_content += f"### Data Quality Assessment\n\n{analysis_results['data_quality']}\n\n"
                    
                    if include_visualizations and visualizations:
                        report_content += f"## Key Visualizations\n\nThis analysis includes {len(visualizations)} visualizations:\n\n"
                        for viz in visualizations:
                            report_content += f"- **{viz['title']}** - {viz['config']['chart_type'].title()} chart\n"
                        report_content += "\n"
                    
                    if include_recommendations and analysis_results.get('recommended_analyses'):
                        report_content += "## Recommendations\n\n"
                        for rec in analysis_results['recommended_analyses']:
                            report_content += f"- {rec}\n"
                        report_content += "\n"
                    
                    report_content += "---\n*Report generated by **DevData Analytics** - AI-Powered Data Analysis Tool*\n"
                
                else:  # Text format
                    report_content = f"""DATA ANALYSIS REPORT
{'='*50}

Generated by DevData Analytics on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

"""
                    
                    if include_executive_summary:
                        summary = analysis_results.get('summary', 'This analysis provides insights into the dataset characteristics, patterns, and recommendations for further investigation.')
                        report_content += f"""EXECUTIVE SUMMARY
{'-'*20}

{summary}

"""
                    
                    if include_data_overview:
                        numeric_cols = len(df.select_dtypes(include=['int64', 'float64']).columns)
                        categorical_cols = len(df.select_dtypes(include=['object', 'category']).columns)
                        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
                        null_count = df.isnull().sum().sum()
                        
                        report_content += f"""DATASET OVERVIEW
{'-'*20}

Total Records: {len(df):,}
Total Columns: {len(df.columns)}
Numeric Columns: {numeric_cols}
Categorical Columns: {categorical_cols}
Memory Usage: {memory_mb:.1f} MB
Missing Values: {null_count:,}

COLUMN INFORMATION:
"""
                        for col in df.columns:
                            dtype = str(df[col].dtype)
                            null_pct = (df[col].isnull().sum() / len(df)) * 100
                            report_content += f"- {col} ({dtype}) - {null_pct:.1f}% missing\n"
                        
                        report_content += "\n"
                    
                    if include_ai_insights and analysis_results:
                        report_content += f"""AI-GENERATED INSIGHTS
{'-'*20}

"""
                        if 'key_insights' in analysis_results:
                            for i, insight in enumerate(analysis_results['key_insights'], 1):
                                report_content += f"{i}. {insight}\n"
                        report_content += "\n"
                    
                    if include_recommendations and analysis_results.get('recommended_analyses'):
                        report_content += f"""RECOMMENDATIONS
{'-'*20}

"""
                        for rec in analysis_results['recommended_analyses']:
                            report_content += f"- {rec}\n"
                        report_content += "\n"
                    
                    report_content += f"""
{'-'*50}
Report generated by DevData Analytics
AI-Powered Data Analysis Tool
"""
                
                # Display preview
                st.success("✅ Report generated successfully!")
                
                # Show preview
                with st.expander("📋 Report Preview", expanded=True):
                    if report_format == "HTML":
                        st.components.v1.html(report_content, height=600, scrolling=True)
                    else:
                        st.text(report_content[:2000] + "..." if len(report_content) > 2000 else report_content)
                
                # Download button
                file_extension = {"HTML": "html", "Markdown": "md", "Text": "txt"}[report_format]
                mime_type = {"HTML": "text/html", "Markdown": "text/markdown", "Text": "text/plain"}[report_format]
                
                st.download_button(
                    label=f"📥 Download {report_format} Report",
                    data=report_content,
                    file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}",
                    mime=mime_type
                )
                
                # Report statistics
                word_count = len(report_content.split())
                char_count = len(report_content)
                st.info(f"📊 Report contains {word_count:,} words and {char_count:,} characters")
                
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")

# Tab 3: Shareable Links
with tab3:
    st.subheader("🔗 Shareable Links & Embeds")
    st.markdown("Create shareable links and embed codes for your visualizations")
    
    if not st.session_state.get('visualizations'):
        st.info("No visualizations available for sharing. Create visualizations first.")
    else:
        # Select visualization for sharing
        viz_options = [f"{i+1}. {viz['title']}" for i, viz in enumerate(st.session_state.visualizations)]
        selected_viz_idx = st.selectbox("Select visualization to share:", range(len(viz_options)), format_func=lambda x: viz_options[x])
        
        selected_viz = st.session_state.visualizations[selected_viz_idx]
        
        st.write("**Sharing Options:**")
        
        # Generate different sharing formats
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📱 Standalone HTML**")
            
            if st.button("Generate Standalone HTML", key="standalone_html"):
                html_content = selected_viz['figure'].to_html(
                    include_plotlyjs='cdn',
                    config={
                        'displayModeBar': True,
                        'responsive': True,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': selected_viz['title'],
                            'height': 600,
                            'width': 800,
                            'scale': 2
                        }
                    },
                    div_id="chart-container"
                )
                
                # Add custom styling and metadata
                enhanced_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{selected_viz['title']} - DevData Analytics</title>
    <meta name="description" content="Interactive data visualization created with DevData Analytics">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #007acc;
            padding-bottom: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
        #chart-container {{
            min-height: 400px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{selected_viz['title']}</h1>
            <p>Interactive data visualization</p>
        </div>
        
        {html_content}
        
        <div class="footer">
            <p>Created with <strong>DevData Analytics</strong> on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </div>
</body>
</html>
"""
                
                st.download_button(
                    label="📥 Download Shareable HTML",
                    data=enhanced_html,
                    file_name=f"shareable_{selected_viz['title'].replace(' ', '_')}.html",
                    mime="text/html"
                )
        
        with col2:
            st.write("**🔗 Embed Code**")
            
            if st.button("Generate Embed Code", key="embed_code"):
                # Create embeddable iframe code
                chart_json = selected_viz['figure'].to_json()
                
                embed_html = f"""
<!-- DevData Analytics Chart Embed -->
<div id="devdata-chart-{selected_viz_idx}" style="width:100%;height:400px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
    var chartData = {chart_json};
    Plotly.newPlot('devdata-chart-{selected_viz_idx}', chartData.data, chartData.layout, {{responsive: true}});
</script>
<p style="font-size:12px;color:#666;text-align:center;">
    Chart created with <a href="#" target="_blank">DevData Analytics</a>
</p>
"""
                
                st.code(embed_html, language='html')
                
                st.download_button(
                    label="📥 Download Embed Code",
                    data=embed_html,
                    file_name=f"embed_{selected_viz['title'].replace(' ', '_')}.html",
                    mime="text/html"
                )
        
        # Preview the selected visualization
        st.markdown("---")
        st.subheader("📊 Preview")
        st.plotly_chart(selected_viz['figure'], use_container_width=True)
        
        # Sharing instructions
        st.markdown("---")
        st.subheader("📋 Sharing Instructions")
        
        st.write("""
        **How to share your visualizations:**
        
        1. **Standalone HTML**: Download and host on any web server or share directly
        2. **Embed Code**: Copy the HTML code and paste into any website or blog
        3. **Social Media**: Take screenshots using the camera icon in the chart toolbar
        4. **Email**: Attach the HTML file or include screenshots
        
        **Tips for sharing:**
        - HTML files work in any modern web browser
        - Embed codes work in most content management systems
        - Charts are fully interactive when shared as HTML
        - Use PNG export for static sharing on social media
        """)

# Tab 4: Presentation Mode
with tab4:
    st.subheader("📱 Presentation Mode")
    st.markdown("Create presentation-ready views of your analysis")
    
    if not st.session_state.get('visualizations'):
        st.info("No visualizations available. Create visualizations first.")
    else:
        # Presentation configuration
        st.write("**Presentation Configuration:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            presentation_style = st.selectbox(
                "Presentation style:",
                ["Clean & Minimal", "Professional Report", "Dashboard Style", "Academic Paper"]
            )
        
        with col2:
            chart_size = st.selectbox(
                "Chart size:",
                ["Large (800px)", "Extra Large (1000px)", "Full Width", "Custom"]
            )
        
        # Color theme
        color_theme = st.selectbox(
            "Color theme:",
            ["Default", "Dark Mode", "High Contrast", "Print Friendly"]
        )
        
        # Chart selection for presentation
        selected_charts = st.multiselect(
            "Select charts for presentation:",
            range(len(st.session_state.visualizations)),
            format_func=lambda x: f"{x+1}. {st.session_state.visualizations[x]['title']}",
            default=list(range(min(4, len(st.session_state.visualizations))))
        )
        
        if st.button("🎨 Generate Presentation", type="primary") and selected_charts:
            try:
                # Apply styling based on presentation style
                if presentation_style == "Clean & Minimal":
                    bg_color = "white"
                    text_color = "#333"
                    grid_color = "#f0f0f0"
                elif presentation_style == "Professional Report":
                    bg_color = "#f8f9fa"
                    text_color = "#2c3e50"
                    grid_color = "#dee2e6"
                elif presentation_style == "Dashboard Style":
                    bg_color = "#1e1e1e"
                    text_color = "white"
                    grid_color = "#3a3a3a"
                else:  # Academic Paper
                    bg_color = "white"
                    text_color = "black"
                    grid_color = "#e0e0e0"
                
                # Create presentation HTML
                presentation_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analysis Presentation</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: {bg_color};
            color: {text_color};
        }}
        .slide {{
            min-height: 100vh;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            page-break-after: always;
        }}
        .chart-container {{
            margin: 20px 0;
            text-align: center;
        }}
        .chart-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }}
        .navigation {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
        }}
        .nav-button {{
            background: #007acc;
            color: white;
            border: none;
            padding: 10px 15px;
            margin: 0 5px;
            border-radius: 5px;
            cursor: pointer;
        }}
        @media print {{
            .navigation {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="navigation">
        <button class="nav-button" onclick="previousSlide()">❮ Previous</button>
        <button class="nav-button" onclick="nextSlide()">Next ❯</button>
        <button class="nav-button" onclick="window.print()">🖨️ Print</button>
    </div>
"""
                
                # Add title slide
                presentation_html += f"""
    <div class="slide" id="slide-0">
        <div style="text-align: center;">
            <h1 style="font-size: 48px; margin-bottom: 20px;">Data Analysis Presentation</h1>
            <h2 style="font-size: 24px; opacity: 0.8;">Generated by DevData Analytics</h2>
            <p style="font-size: 18px; margin-top: 40px;">{datetime.now().strftime('%B %d, %Y')}</p>
            <div style="margin-top: 60px;">
                <p><strong>Dataset:</strong> {len(df):,} rows × {len(df.columns)} columns</p>
                <p><strong>Charts:</strong> {len(selected_charts)} visualizations</p>
            </div>
        </div>
    </div>
"""
                
                # Add chart slides
                for i, chart_idx in enumerate(selected_charts):
                    viz = st.session_state.visualizations[chart_idx]
                    
                    # Update chart styling for presentation
                    fig = viz['figure']
                    fig.update_layout(
                        plot_bgcolor=bg_color,
                        paper_bgcolor=bg_color,
                        font_color=text_color,
                        xaxis=dict(gridcolor=grid_color),
                        yaxis=dict(gridcolor=grid_color),
                        height=600 if chart_size == "Large (800px)" else 800
                    )
                    
                    chart_json = fig.to_json()
                    
                    presentation_html += f"""
    <div class="slide" id="slide-{i+1}">
        <div class="chart-title">{viz['title']}</div>
        <div class="chart-container">
            <div id="chart-{i}" style="height: {'600px' if chart_size == 'Large (800px)' else '800px'};"></div>
        </div>
    </div>
"""
                
                # Add JavaScript for interactivity
                presentation_html += """
    <script>
        let currentSlide = 0;
        const totalSlides = """ + str(len(selected_charts) + 1) + """;
        
        function showSlide(n) {
            const slides = document.querySelectorAll('.slide');
            if (n >= totalSlides) currentSlide = 0;
            if (n < 0) currentSlide = totalSlides - 1;
            
            slides.forEach(slide => slide.style.display = 'none');
            slides[currentSlide].style.display = 'flex';
        }
        
        function nextSlide() {
            currentSlide++;
            showSlide(currentSlide);
        }
        
        function previousSlide() {
            currentSlide--;
            showSlide(currentSlide);
        }
        
        // Initialize charts
        document.addEventListener('DOMContentLoaded', function() {
            showSlide(0);
"""
                
                # Add chart initialization
                for i, chart_idx in enumerate(selected_charts):
                    viz = st.session_state.visualizations[chart_idx]
                    fig = viz['figure']
                    fig.update_layout(
                        plot_bgcolor=bg_color,
                        paper_bgcolor=bg_color,
                        font_color=text_color,
                        height=600 if chart_size == "Large (800px)" else 800
                    )
                    chart_json = fig.to_json()
                    
                    presentation_html += f"""
            var chartData{i} = {chart_json};
            Plotly.newPlot('chart-{i}', chartData{i}.data, chartData{i}.layout, {{responsive: true}});
"""
                
                presentation_html += """
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
            if (e.key === 'ArrowLeft') previousSlide();
        });
    </script>
</body>
</html>
"""
                
                st.success("✅ Presentation generated successfully!")
                
                # Download button
                st.download_button(
                    label="📥 Download Presentation",
                    data=presentation_html,
                    file_name=f"presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
                
                # Instructions
                st.info("""
                **Presentation Instructions:**
                - Use arrow keys or navigation buttons to move between slides
                - Press spacebar to advance to next slide
                - Click the print button for printer-friendly version
                - Charts are fully interactive in presentation mode
                """)
                
            except Exception as e:
                st.error(f"❌ Error generating presentation: {str(e)}")

# Sidebar: Sharing Summary
with st.sidebar:
    st.header("🔗 Sharing Summary")
    
    # Available content for sharing
    viz_count = len(st.session_state.get('visualizations', []))
    has_analysis = bool(st.session_state.get('analysis_results'))
    
    st.metric("Visualizations", viz_count)
    
    if has_analysis:
        st.success("✅ AI Analysis Available")
    else:
        st.info("ℹ️ No AI analysis yet")
    
    st.write("**Available Exports:**")
    st.write("• Individual chart images")
    st.write("• Interactive HTML files")
    st.write("• Comprehensive reports")
    st.write("• Presentation slides")
    st.write("• Embed codes")
    
    st.markdown("---")
    st.write("**💡 Sharing Tips:**")
    st.write("• HTML files preserve interactivity")
    st.write("• PNG exports work for presentations")
    st.write("• Use embed codes for websites")
    st.write("• Reports are great for stakeholders")
    
    # Quick action buttons
    if viz_count > 0:
        st.markdown("---")
        st.write("**🚀 Quick Actions:**")
        
        if st.button("📸 Export All as PNG", key="quick_png"):
            st.info("Use the Visualization Export tab to download PNG files")
        
        if st.button("📄 Generate Report", key="quick_report"):
            st.info("Use the Analysis Report tab to create comprehensive reports")
