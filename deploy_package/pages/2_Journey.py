import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from utils.database import DatabaseManager

st.set_page_config(page_title="My Journey", page_icon="🎯", layout="wide")

def show_journey_page():
    """Show user's learning journey and analytics"""
    if not st.session_state.authenticated:
        st.warning("Please login to view your learning journey.")
        return
    
    user_data = st.session_state.user_data
    db_manager = DatabaseManager()
    
    st.title("🎯 My Learning Journey")
    st.markdown(f"Track your progress and achievements, {user_data['name']}!")
    
    # User stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        coins = db_manager.get_user_coins(user_data['id'])
        st.metric("Total Coins Earned", f"🪙 {coins}")
    
    with col2:
        # Mock data for videos watched
        videos_watched = 45  # In real app, this would come from database
        st.metric("Videos Watched", f"📹 {videos_watched}")
    
    with col3:
        # Mock data for tests taken
        tests_taken = 12  # In real app, this would come from database
        st.metric("Tests Completed", f"📝 {tests_taken}")
    
    with col4:
        # Mock data for study time
        study_hours = 78  # In real app, this would come from database
        st.metric("Study Hours", f"⏰ {study_hours}h")
    
    st.markdown("---")
    
    # Journey sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "🏆 Achievements", "📈 Progress", "🎯 Goals"])
    
    with tab1:
        show_analytics_section(user_data, db_manager)
    
    with tab2:
        show_achievements_section(user_data, db_manager)
    
    with tab3:
        show_progress_section(user_data, db_manager)
    
    with tab4:
        show_goals_section(user_data, db_manager)

def show_analytics_section(user_data: dict, db_manager: DatabaseManager):
    """Show detailed analytics"""
    st.subheader("📊 Your Learning Analytics")
    
    # Daily activity chart
    st.write("### Daily Activity (Last 30 Days)")
    
    # Generate mock daily activity data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    activity_data = {
        'Date': dates,
        'Videos Watched': [max(0, int(5 * (0.5 + 0.5 * abs(hash(str(date)) % 100) / 100))) for date in dates],
        'Tests Taken': [max(0, int(2 * (0.3 + 0.7 * abs(hash(str(date) + 'test') % 100) / 100))) for date in dates],
        'Study Hours': [max(0, int(8 * (0.4 + 0.6 * abs(hash(str(date) + 'hours') % 100) / 100))) for date in dates]
    }
    
    df_activity = pd.DataFrame(activity_data)
    
    # Activity line chart
    fig_activity = go.Figure()
    
    fig_activity.add_trace(go.Scatter(
        x=df_activity['Date'], 
        y=df_activity['Videos Watched'],
        mode='lines+markers',
        name='Videos Watched',
        line=dict(color='#FF6B6B')
    ))
    
    fig_activity.add_trace(go.Scatter(
        x=df_activity['Date'], 
        y=df_activity['Tests Taken'],
        mode='lines+markers',
        name='Tests Taken',
        line=dict(color='#4ECDC4')
    ))
    
    fig_activity.add_trace(go.Scatter(
        x=df_activity['Date'], 
        y=df_activity['Study Hours'],
        mode='lines+markers',
        name='Study Hours',
        line=dict(color='#45B7D1')
    ))
    
    fig_activity.update_layout(
        title="Daily Learning Activity",
        xaxis_title="Date",
        yaxis_title="Count",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_activity, use_container_width=True)
    
    # Subject performance
    st.write("### Subject-wise Performance")
    
    subjects_data = {
        'Subject': ['Mathematics', 'Physics', 'Chemistry', 'Biology'],
        'Average Score': [78, 82, 75, 85],
        'Tests Taken': [4, 3, 2, 3]
    }
    
    df_subjects = pd.DataFrame(subjects_data)
    
    fig_subjects = px.bar(
        df_subjects, 
        x='Subject', 
        y='Average Score',
        color='Average Score',
        title="Average Scores by Subject",
        color_continuous_scale='Blues'
    )
    
    st.plotly_chart(fig_subjects, use_container_width=True)
    
    # Weekly pattern
    st.write("### Weekly Study Pattern")
    
    weekly_data = {
        'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Study Hours': [6, 5, 7, 6, 4, 8, 5]
    }
    
    fig_weekly = px.bar(
        x=weekly_data['Day'],
        y=weekly_data['Study Hours'],
        title="Study Hours by Day of Week",
        color=weekly_data['Study Hours'],
        color_continuous_scale='Greens'
    )
    
    st.plotly_chart(fig_weekly, use_container_width=True)

def show_achievements_section(user_data: dict, db_manager: DatabaseManager):
    """Show user achievements and badges"""
    st.subheader("🏆 Your Achievements")
    
    # Achievement badges
    achievements = [
        {
            "title": "First Steps",
            "description": "Completed your first video lesson",
            "icon": "🌟",
            "earned": True,
            "date": "2024-01-15"
        },
        {
            "title": "Test Taker",
            "description": "Completed your first test",
            "icon": "📝",
            "earned": True,
            "date": "2024-01-18"
        },
        {
            "title": "Consistent Learner",
            "description": "Studied for 7 consecutive days",
            "icon": "🔥",
            "earned": True,
            "date": "2024-01-25"
        },
        {
            "title": "High Scorer",
            "description": "Scored above 90% in a test",
            "icon": "🎯",
            "earned": False,
            "date": None
        },
        {
            "title": "Video Master",
            "description": "Watched 50 video lessons",
            "icon": "📺",
            "earned": True,
            "date": "2024-02-10"
        },
        {
            "title": "Coin Collector",
            "description": "Earned 100 coins",
            "icon": "🪙",
            "earned": True,
            "date": "2024-02-05"
        }
    ]
    
    # Display achievements in grid
    cols = st.columns(3)
    for i, achievement in enumerate(achievements):
        with cols[i % 3]:
            if achievement['earned']:
                st.markdown(f"""
                <div style="
                    border: 2px solid #4CAF50;
                    border-radius: 15px;
                    padding: 20px;
                    margin: 10px 0;
                    background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%);
                    text-align: center;
                ">
                    <div style="font-size: 3rem;">{achievement['icon']}</div>
                    <h4 style="color: #4CAF50;">{achievement['title']}</h4>
                    <p>{achievement['description']}</p>
                    <small style="color: #666;">Earned on {achievement['date']}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    border: 2px solid #ddd;
                    border-radius: 15px;
                    padding: 20px;
                    margin: 10px 0;
                    background: #f9f9f9;
                    text-align: center;
                    opacity: 0.6;
                ">
                    <div style="font-size: 3rem; filter: grayscale(100%);">{achievement['icon']}</div>
                    <h4 style="color: #999;">{achievement['title']}</h4>
                    <p>{achievement['description']}</p>
                    <small style="color: #999;">Not earned yet</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Achievement progress
    earned_count = sum(1 for a in achievements if a['earned'])
    total_count = len(achievements)
    
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0;">
        <h3>Achievement Progress: {earned_count}/{total_count}</h3>
        <div style="background: #e0e0e0; border-radius: 10px; height: 20px; width: 100%; margin: 10px 0;">
            <div style="background: #4CAF50; height: 100%; width: {(earned_count/total_count)*100}%; border-radius: 10px;"></div>
        </div>
        <p>You've earned {earned_count} out of {total_count} achievements!</p>
    </div>
    """, unsafe_allow_html=True)

def show_progress_section(user_data: dict, db_manager: DatabaseManager):
    """Show learning progress"""
    st.subheader("📈 Learning Progress")
    
    # Course progress
    courses = db_manager.get_user_courses(user_data['id'])
    
    if courses:
        st.write("### Course Progress")
        for course in courses:
            st.write(f"**{course['name']}**")
            progress = course['progress']
            
            # Progress bar with animation effect
            progress_html = f"""
            <div style="background: #e0e0e0; border-radius: 10px; height: 25px; width: 100%; margin: 10px 0; position: relative;">
                <div style="
                    background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
                    height: 100%;
                    width: {progress}%;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    transition: width 1s ease-in-out;
                ">
                    {progress}%
                </div>
            </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)
    
    # Test performance over time
    st.write("### Test Performance Over Time")
    
    test_dates = pd.date_range(end=datetime.now(), periods=10, freq='W')
    test_scores = [65, 72, 78, 75, 82, 85, 88, 84, 90, 87]
    
    fig_progress = go.Figure()
    
    fig_progress.add_trace(go.Scatter(
        x=test_dates,
        y=test_scores,
        mode='lines+markers+text',
        text=test_scores,
        textposition="top center",
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8, color='#FF6B6B'),
        name='Test Scores'
    ))
    
    fig_progress.update_layout(
        title="Test Score Improvement",
        xaxis_title="Date",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0, 100]),
        showlegend=False
    )
    
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Study streak
    st.write("### Study Streak")
    current_streak = 15  # Mock data
    best_streak = 23  # Mock data
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Streak", f"🔥 {current_streak} days")
    with col2:
        st.metric("Best Streak", f"🏆 {best_streak} days")

def show_goals_section(user_data: dict, db_manager: DatabaseManager):
    """Show and manage learning goals"""
    st.subheader("🎯 Learning Goals")
    
    # Current goals
    goals = [
        {
            "title": "Study 2 hours daily",
            "current": 1.5,
            "target": 2.0,
            "unit": "hours"
        },
        {
            "title": "Complete 3 tests per week",
            "current": 2,
            "target": 3,
            "unit": "tests"
        },
        {
            "title": "Maintain 85% average score",
            "current": 82,
            "target": 85,
            "unit": "%"
        }
    ]
    
    for goal in goals:
        progress = min(100, (goal['current'] / goal['target']) * 100)
        
        st.write(f"**{goal['title']}**")
        st.write(f"Progress: {goal['current']}{goal['unit']} / {goal['target']}{goal['unit']}")
        
        color = "#4CAF50" if progress >= 100 else "#FF9800" if progress >= 75 else "#FF6B6B"
        
        progress_html = f"""
        <div style="background: #e0e0e0; border-radius: 10px; height: 20px; width: 100%; margin: 10px 0;">
            <div style="background: {color}; height: 100%; width: {progress}%; border-radius: 10px;"></div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
        st.markdown("---")
    
    # Add new goal
    st.write("### Set New Goal")
    with st.form("new_goal"):
        goal_title = st.text_input("Goal Description")
        target_value = st.number_input("Target Value", min_value=1)
        goal_unit = st.selectbox("Unit", ["hours", "tests", "videos", "days", "%"])
        
        if st.form_submit_button("Add Goal", type="primary"):
            st.success(f"Goal added: {goal_title}")
            st.info("Goal tracking will be implemented in future updates.")
    
    # Motivational message for non-premium users
    if not db_manager.is_premium_user(user_data['id']):
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
        ">
            <h3>🚀 It's time for you to study with Sharpy & Excel in your Life!</h3>
            <p>Unlock premium features to accelerate your learning journey</p>
            <button style="
                background: white;
                color: #667eea;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                cursor: pointer;
            ">Upgrade to Premium</button>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_journey_page()