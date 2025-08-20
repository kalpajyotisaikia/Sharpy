import streamlit as st
from utils.database import DatabaseManager

st.set_page_config(page_title="Educational Shorts", page_icon="🎬", layout="wide")

def show_shorts_page():
    """Show educational shorts/videos page"""
    if not st.session_state.authenticated:
        st.warning("Please login to access educational shorts.")
        return
    
    user_data = st.session_state.user_data
    db_manager = DatabaseManager()
    
    st.title("🎬 Educational Shorts")
    st.markdown("Quick learning videos to boost your knowledge!")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        subject_filter = st.selectbox("Subject", 
            ["All", "Mathematics", "Physics", "Chemistry", "Biology", "English"])
    
    with col2:
        duration_filter = st.selectbox("Duration", 
            ["All", "Under 2 min", "2-5 min", "5-10 min"])
    
    with col3:
        difficulty_filter = st.selectbox("Difficulty", 
            ["All", "Beginner", "Intermediate", "Advanced"])
    
    st.markdown("---")
    
    # Educational shorts content
    show_shorts_grid(user_data, db_manager, subject_filter, duration_filter, difficulty_filter)

def show_shorts_grid(user_data: dict, db_manager: DatabaseManager, subject: str, duration: str, difficulty: str):
    """Display shorts in a grid format"""
    
    # Sample educational shorts data
    shorts = [
        {
            "id": 1,
            "title": "Quadratic Formula in 60 Seconds",
            "subject": "Mathematics",
            "duration": "1:00",
            "difficulty": "Intermediate",
            "thumbnail": "📊",
            "views": "12.5K",
            "likes": "1.2K",
            "description": "Master the quadratic formula quickly with this short explanation!",
            "coins_reward": 8
        },
        {
            "id": 2,
            "title": "Newton's Laws Explained",
            "subject": "Physics",
            "duration": "2:30",
            "difficulty": "Beginner",
            "thumbnail": "🔬",
            "views": "25.3K",
            "likes": "2.8K",
            "description": "Understanding Newton's three laws of motion in simple terms.",
            "coins_reward": 10
        },
        {
            "id": 3,
            "title": "Periodic Table Tricks",
            "subject": "Chemistry",
            "duration": "1:45",
            "difficulty": "Beginner",
            "thumbnail": "⚗️",
            "views": "18.7K",
            "likes": "1.9K",
            "description": "Memory tricks to remember the periodic table easily!",
            "coins_reward": 9
        },
        {
            "id": 4,
            "title": "DNA Structure Quick Review",
            "subject": "Biology",
            "duration": "2:15",
            "difficulty": "Intermediate",
            "thumbnail": "🧬",
            "views": "15.2K",
            "likes": "1.5K",
            "description": "Quick overview of DNA structure and its components.",
            "coins_reward": 11
        },
        {
            "id": 5,
            "title": "Calculus Limits Simplified",
            "subject": "Mathematics",
            "duration": "3:20",
            "difficulty": "Advanced",
            "thumbnail": "📈",
            "views": "8.9K",
            "likes": "934",
            "description": "Understanding limits in calculus with simple examples.",
            "coins_reward": 15
        },
        {
            "id": 6,
            "title": "Electromagnetic Waves Basics",
            "subject": "Physics",
            "duration": "2:45",
            "difficulty": "Intermediate",
            "thumbnail": "📡",
            "views": "11.4K",
            "likes": "1.1K",
            "description": "Introduction to electromagnetic spectrum and properties.",
            "coins_reward": 12
        }
    ]
    
    # Filter shorts based on selection
    filtered_shorts = filter_shorts(shorts, subject, duration, difficulty)
    
    if not filtered_shorts:
        st.info("No shorts match your current filters. Try adjusting your selection!")
        return
    
    # Display shorts in responsive grid
    cols_per_row = 2
    rows = len(filtered_shorts) // cols_per_row + (1 if len(filtered_shorts) % cols_per_row else 0)
    
    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            short_idx = row * cols_per_row + col_idx
            if short_idx < len(filtered_shorts):
                short = filtered_shorts[short_idx]
                with cols[col_idx]:
                    show_short_card(short, user_data, db_manager)

def show_short_card(short: dict, user_data: dict, db_manager: DatabaseManager):
    """Display individual short card"""
    
    # Short card with custom styling
    st.markdown(f"""
    <div style="
        border: 1px solid #e0e0e0;
        border-radius: 15px;
        padding: 0;
        margin: 15px 0;
        background: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        overflow: hidden;
        transition: transform 0.2s;
    ">
        <!-- Video thumbnail area -->
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        ">
            <div style="font-size: 4rem; color: white;">{short['thumbnail']}</div>
            <div style="
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: bold;
            ">
                {short['duration']}
            </div>
            <div style="
                position: absolute;
                bottom: 10px;
                right: 10px;
                background: #FFD700;
                color: #333;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
            ">
                +{short['coins_reward']} coins
            </div>
        </div>
        
        <!-- Content area -->
        <div style="padding: 15px;">
            <h4 style="margin: 0 0 10px 0; color: #333; font-size: 16px;">{short['title']}</h4>
            <p style="margin: 0 0 10px 0; color: #666; font-size: 13px; line-height: 1.4;">
                {short['description']}
            </p>
            
            <!-- Stats -->
            <div style="display: flex; justify-content: space-between; margin: 10px 0; font-size: 12px; color: #999;">
                <span>👀 {short['views']} views</span>
                <span>👍 {short['likes']} likes</span>
                <span>📚 {short['subject']}</span>
            </div>
            
            <!-- Difficulty badge -->
            <div style="margin: 10px 0;">
                <span style="
                    background: {get_difficulty_color(short['difficulty'])};
                    color: white;
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: bold;
                ">
                    {short['difficulty']}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Watch button
    if st.button(f"▶️ Watch Now", key=f"watch_{short['id']}", type="primary"):
        show_video_player(short, user_data, db_manager)

def show_video_player(short: dict, user_data: dict, db_manager: DatabaseManager):
    """Show video player interface"""
    
    st.markdown("---")
    
    # Video player area
    st.subheader(f"🎬 {short['title']}")
    
    # Mock video player
    st.markdown(f"""
    <div style="
        background: #000;
        height: 400px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
        position: relative;
    ">
        <div style="text-align: center; color: white;">
            <div style="font-size: 6rem;">{short['thumbnail']}</div>
            <h3>Now Playing: {short['title']}</h3>
            <p>Duration: {short['duration']} • Subject: {short['subject']}</p>
        </div>
        
        <!-- Play controls -->
        <div style="
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 30px;
            backdrop-filter: blur(10px);
        ">
            <span style="color: white; font-size: 14px;">▶️ Playing • 🔊 Audio On • ⚡ {short['coins_reward']} coins to earn</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Video completion actions
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("👍 Like", key=f"like_{short['id']}"):
            st.success("Liked!")
    
    with col2:
        if st.button("💾 Save", key=f"save_{short['id']}"):
            st.success("Saved to your collection!")
    
    with col3:
        if st.button("✅ Mark Complete", key=f"complete_{short['id']}", type="primary"):
            # Award coins for completing video
            db_manager.add_user_coins(user_data['id'], short['coins_reward'])
            st.success(f"Great! You earned {short['coins_reward']} coins! 🪙")
            
            # Add achievement notification
            db_manager.add_notification(
                user_data['id'],
                "Video Completed!",
                f"You completed '{short['title']}' and earned {short['coins_reward']} coins!",
                "success"
            )
    
    # Related shorts
    st.markdown("---")
    st.subheader("📚 Related Shorts")
    
    related_subjects = ["Mathematics", "Physics", "Chemistry", "Biology"]
    related_subject = short['subject']
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    
    for i in range(3):
        with cols[i]:
            st.markdown(f"""
            <div style="
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 10px;
                text-align: center;
                background: white;
            ">
                <div style="font-size: 2rem;">🎬</div>
                <h5>Related {related_subject} Short {i+1}</h5>
                <small>Duration: 2:{15+i*10}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Watch", key=f"related_{i}"):
                st.info(f"Loading related video {i+1}...")

def filter_shorts(shorts: list, subject: str, duration: str, difficulty: str) -> list:
    """Filter shorts based on user selection"""
    filtered = shorts.copy()
    
    if subject != "All":
        filtered = [s for s in filtered if s['subject'] == subject]
    
    if duration != "All":
        # In a real app, you'd properly parse duration and filter
        pass
    
    if difficulty != "All":
        filtered = [s for s in filtered if s['difficulty'] == difficulty]
    
    return filtered

def get_difficulty_color(difficulty: str) -> str:
    """Get color for difficulty level"""
    colors = {
        "Beginner": "#4CAF50",
        "Intermediate": "#FF9800",
        "Advanced": "#F44336"
    }
    return colors.get(difficulty, "#666")

if __name__ == "__main__":
    show_shorts_page()