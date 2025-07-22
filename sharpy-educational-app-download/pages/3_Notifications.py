import streamlit as st
from datetime import datetime
from utils.database import DatabaseManager

st.set_page_config(page_title="Notifications", page_icon="🔔", layout="wide")

def show_notifications_page():
    """Show user notifications and messaging"""
    if not st.session_state.authenticated:
        st.warning("Please login to view notifications.")
        return
    
    user_data = st.session_state.user_data
    db_manager = DatabaseManager()
    
    st.title("🔔 Notifications")
    
    # Notification tabs
    tab1, tab2, tab3 = st.tabs(["📬 All Notifications", "🎥 Live Classes", "📢 Announcements"])
    
    with tab1:
        show_all_notifications(user_data, db_manager)
    
    with tab2:
        show_live_class_notifications(user_data, db_manager)
    
    with tab3:
        show_announcements(user_data, db_manager)

def show_all_notifications(user_data: dict, db_manager: DatabaseManager):
    """Show all user notifications"""
    st.subheader("📬 Your Notifications")
    
    notifications = db_manager.get_user_notifications(user_data['id'])
    
    if not notifications:
        st.info("No notifications yet. We'll notify you about important updates!")
        return
    
    # Mark all as read button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Mark All Read", type="secondary"):
            st.success("All notifications marked as read!")
    
    # Display notifications
    for notification in notifications:
        # Notification card styling based on type and read status
        card_style = get_notification_card_style(notification['type'], notification['is_read'])
        
        st.markdown(f"""
        <div style="{card_style}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 10px 0; color: #333;">{get_notification_icon(notification['type'])} {notification['title']}</h4>
                    <p style="margin: 0 0 10px 0; color: #666;">{notification['message']}</p>
                    <small style="color: #999;">{format_notification_time(notification['created_at'])}</small>
                </div>
                <div>
                    {get_notification_badge(notification['type'])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_live_class_notifications(user_data: dict, db_manager: DatabaseManager):
    """Show live class notifications and reminders"""
    st.subheader("🎥 Live Class Updates")
    
    # Today's live classes
    live_classes = db_manager.get_today_live_classes(user_data['id'])
    
    if live_classes:
        st.write("### Today's Schedule")
        for class_info in live_classes:
            st.markdown(f"""
            <div style="
                border-left: 4px solid #FF6B6B;
                background: #fff5f5;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            ">
                <h4 style="margin: 0; color: #FF6B6B;">🎥 {class_info['subject']} - {class_info['topic']}</h4>
                <p style="margin: 5px 0;">👨‍🏫 Teacher: {class_info['teacher']}</p>
                <p style="margin: 5px 0;">⏰ Time: {class_info['time']}</p>
                <p style="margin: 5px 0;">📚 Duration: {class_info['duration']} minutes</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button(f"Join Now", key=f"join_{class_info['id']}", type="primary"):
                    st.success("Joining live class...")
                    # Award coins for attending live class
                    db_manager.add_user_coins(user_data['id'], 10)
                    st.info("You earned 10 coins for attending the live class!")
    else:
        st.info("No live classes scheduled for today.")
    
    # Notification preferences
    st.markdown("---")
    st.write("### Notification Preferences")
    
    col1, col2 = st.columns(2)
    with col1:
        live_class_reminder = st.checkbox("Live Class Reminders", value=True)
        new_content_alert = st.checkbox("New Content Alerts", value=True)
    
    with col2:
        test_reminder = st.checkbox("Test Reminders", value=True)
        achievement_notification = st.checkbox("Achievement Notifications", value=True)
    
    if st.button("Save Preferences"):
        st.success("Notification preferences saved!")

def show_announcements(user_data: dict, db_manager: DatabaseManager):
    """Show important announcements"""
    st.subheader("📢 Important Announcements")
    
    # Sample announcements
    announcements = [
        {
            "title": "New Course Launch: Advanced Mathematics",
            "content": "We're excited to announce the launch of our Advanced Mathematics course for Class 12 students. Enroll now to get early bird discount!",
            "date": "2024-07-20",
            "type": "course",
            "priority": "high"
        },
        {
            "title": "System Maintenance Scheduled",
            "content": "Scheduled maintenance on July 25th from 2:00 AM to 4:00 AM IST. The platform will be temporarily unavailable.",
            "date": "2024-07-18",
            "type": "system",
            "priority": "medium"
        },
        {
            "title": "New Achievement Badges Available",
            "content": "Check out the new achievement badges in your journey section. Complete challenges to earn exclusive rewards!",
            "date": "2024-07-15",
            "type": "feature",
            "priority": "low"
        },
        {
            "title": "Live Doubt Clearing Session",
            "content": "Join our special doubt clearing session this weekend. Get your questions answered by expert teachers.",
            "date": "2024-07-22",
            "type": "event",
            "priority": "high"
        }
    ]
    
    for announcement in announcements:
        priority_color = {
            "high": "#FF6B6B",
            "medium": "#FFB366", 
            "low": "#4ECDC4"
        }
        
        st.markdown(f"""
        <div style="
            border: 1px solid {priority_color[announcement['priority']]};
            border-left: 5px solid {priority_color[announcement['priority']]};
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                <h4 style="margin: 0; color: {priority_color[announcement['priority']]};">
                    {get_announcement_icon(announcement['type'])} {announcement['title']}
                </h4>
                <span style="
                    background: {priority_color[announcement['priority']]};
                    color: white;
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                ">
                    {announcement['priority'].upper()}
                </span>
            </div>
            <p style="color: #666; margin: 10px 0;">{announcement['content']}</p>
            <small style="color: #999;">📅 {announcement['date']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Subscribe to announcements
    st.markdown("---")
    st.write("### Stay Updated")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        email_notifications = st.checkbox("Email Notifications", value=True)
        sms_notifications = st.checkbox("SMS Notifications", value=False)
    
    with col2:
        if st.button("Update Subscription", type="primary"):
            st.success("Subscription preferences updated!")

def get_notification_card_style(notification_type: str, is_read: bool) -> str:
    """Get CSS style for notification card"""
    opacity = "0.7" if is_read else "1.0"
    border_color = {
        "info": "#4ECDC4",
        "success": "#4CAF50",
        "warning": "#FFB366",
        "error": "#FF6B6B"
    }.get(notification_type, "#ddd")
    
    return f"""
        border: 1px solid {border_color};
        border-left: 4px solid {border_color};
        background: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        opacity: {opacity};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    """

def get_notification_icon(notification_type: str) -> str:
    """Get icon for notification type"""
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "course": "📚",
        "test": "📝",
        "achievement": "🏆"
    }
    return icons.get(notification_type, "📢")

def get_notification_badge(notification_type: str) -> str:
    """Get badge for notification type"""
    colors = {
        "info": "#4ECDC4",
        "success": "#4CAF50",
        "warning": "#FFB366",
        "error": "#FF6B6B"
    }
    
    color = colors.get(notification_type, "#ddd")
    return f"""
    <span style="
        background: {color};
        color: white;
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 10px;
        font-weight: bold;
    ">
        {notification_type.upper()}
    </span>
    """

def get_announcement_icon(announcement_type: str) -> str:
    """Get icon for announcement type"""
    icons = {
        "course": "📚",
        "system": "⚙️",
        "feature": "✨",
        "event": "🎯"
    }
    return icons.get(announcement_type, "📢")

def format_notification_time(timestamp) -> str:
    """Format notification timestamp"""
    # In a real app, this would properly parse the timestamp
    return "2 hours ago"  # Placeholder

if __name__ == "__main__":
    show_notifications_page()