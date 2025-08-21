import streamlit as st
import pandas as pd
import os
from utils.auth import AuthManager
from utils.database import DatabaseManager
from utils.otp_manager import OTPManager

# Configure page
st.set_page_config(
    page_title="Sharpy Education",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="auto"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Initialize managers
auth_manager = AuthManager()
db_manager = DatabaseManager()
otp_manager = OTPManager()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .nav-button {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .nav-button:hover {
        background: #5a67d8;
    }
    .course-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .coins-display {
        background: #ffd700;
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .floating-buttons {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    .floating-btn {
        background: #25d366;
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        margin: 5px;
        cursor: pointer;
        font-size: 20px;
    }
    .floating-btn.call {
        background: #007bff;
    }
</style>
""", unsafe_allow_html=True)

def show_auth_page():
    """Show authentication page"""
    st.markdown('<div class="main-header"><h1>📚 Welcome to Sharpy Education</h1><p>Your Gateway to Academic Excellence</p></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        # Login form
        with st.form("login_form"):
            phone = st.text_input("Phone Number", placeholder="+91XXXXXXXXXX")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", type="primary"):
                if auth_manager.login_user(phone, password):
                    st.session_state.authenticated = True
                    st.session_state.user_data = auth_manager.get_user_data(phone)
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        
        st.markdown("---")
        if st.button("Login with OTP"):
            st.session_state.show_otp_login = True
            st.rerun()
        
        # OTP Login Section
        if st.session_state.get('show_otp_login', False):
            show_otp_login_section()
    
    with tab2:
        st.subheader("Create New Account")
        
        # Registration form
        with st.form("register_form"):
            st.write("**Personal Information**")
            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number", placeholder="+91XXXXXXXXXX")
            email = st.text_input("Email Address")
            
            st.write("**Educational Details**")
            school = st.text_input("School Name")
            class_level = st.selectbox("Class", [
                "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", 
                "Class 11", "Class 12", "Engineering Entrance", "Medical Entrance"
            ])
            address = st.text_area("Address")
            
            st.write("**Account Security**")
            password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            agree_terms = st.checkbox("I agree to the Terms and Conditions")
            
            if st.form_submit_button("Register", type="primary"):
                if password != confirm_password:
                    st.error("Passwords don't match!")
                elif not agree_terms:
                    st.error("Please agree to the terms and conditions.")
                elif auth_manager.register_user(name, phone, email, school, class_level, address, password):
                    st.success("Registration successful! Please login with your credentials.")
                    # Clear registration form
                    st.session_state.registration_success = True
                else:
                    st.error("Registration failed. Phone number might already exist.")

def show_navigation():
    """Show navigation for authenticated users"""
    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
    
    with col1:
        if st.button("🏠 Home", key="nav_home"):
            st.session_state.current_page = 'home'
            st.rerun()
    
    with col2:
        if st.button("📚 Courses", key="nav_courses"):
            st.session_state.current_page = 'courses'
            st.rerun()
    
    with col3:
        if st.button("🎯 My Journey", key="nav_journey"):
            st.session_state.current_page = 'journey'
            st.rerun()
    
    with col4:
        if st.button("🔔 Notifications", key="nav_notifications"):
            st.session_state.current_page = 'notifications'
            st.rerun()
    
    with col5:
        if st.button("🎬 Shorts", key="nav_shorts"):
            st.session_state.current_page = 'shorts'
            st.rerun()
    
    with col6:
        if st.button("🚪 Logout", key="logout"):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.session_state.current_page = 'home'
            st.rerun()

def show_home_page():
    """Show home page based on user premium status"""
    user_data = st.session_state.user_data
    
    # Header with user info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="main-header"><h2>Welcome back, {user_data["name"]}!</h2></div>', unsafe_allow_html=True)
    
    with col2:
        coins = db_manager.get_user_coins(user_data['id'])
        st.markdown(f'<div class="coins-display">🪙 {coins} Coins</div>', unsafe_allow_html=True)
    
    is_premium = db_manager.is_premium_user(user_data['id'])
    
    if not is_premium:
        # Non-premium user home page
        st.subheader("🎯 Unlock Your Potential with Sharpy Premium!")
        
        # Promotional banner
        st.info("Join thousands of successful students who have transformed their academic journey with Sharpy's comprehensive courses!")
        
        # Free test series
        st.subheader("📝 Free Test Series")
        if st.button("Apply For A Test", type="primary"):
            show_test_series_selection()
        
        # YouTube videos section
        st.subheader("📹 Featured Video Lessons")
        show_video_thumbnails()
        
        # Testimonials
        st.subheader("🌟 SHARPY-ত পঢ়া Student-ৰ মনৰ ভাৱ")
        show_testimonials()
        
    else:
        # Premium user home page
        # Scheduled live classes
        st.subheader("🎥 Today's Live Classes")
        show_live_classes()
        
        # Enrolled courses
        st.subheader("📚 Your Enrolled Courses")
        show_enrolled_courses()
        
        # YouTube videos section
        st.subheader("📹 Latest Video Lessons")
        show_video_thumbnails()
        
        # Testimonials
        st.subheader("🌟 SHARPY-ত পঢ়া Student-ৰ মনৰ ভাৱ")
        show_testimonials()

def show_test_series_selection():
    """Show subject-wise test series for the user's class"""
    user_data = st.session_state.user_data
    class_level = user_data['class']
    
    st.subheader(f"📝 Test Series for {class_level}")
    
    # Get subjects based on class
    subjects = db_manager.get_subjects_by_class(class_level)
    
    col1, col2, col3 = st.columns(3)
    for i, subject in enumerate(subjects):
        with [col1, col2, col3][i % 3]:
            with st.container():
                st.markdown(f'<div class="course-card">', unsafe_allow_html=True)
                st.write(f"**{subject['name']}**")
                st.write(f"Duration: {subject.get('duration', '60')} minutes")
                st.write(f"Questions: {subject.get('questions', '50')}")
                
                if st.button(f"Start {subject['name']} Test", key=f"test_{subject['id']}"):
                    st.success(f"Starting {subject['name']} test...")
                    # Award coins for test attempt
                    db_manager.add_user_coins(user_data['id'], 5)
                    st.info("You earned 5 coins for attempting the test!")
                
                st.markdown('</div>', unsafe_allow_html=True)

def show_video_thumbnails():
    """Show swipeable video thumbnails"""
    videos = [
        {"title": "Mathematics Basics", "thumbnail": "📊", "duration": "15:30"},
        {"title": "Physics Concepts", "thumbnail": "🔬", "duration": "22:45"},
        {"title": "Chemistry Formulas", "thumbnail": "⚗️", "duration": "18:20"},
        {"title": "Biology Systems", "thumbnail": "🧬", "duration": "25:10"},
    ]
    
    cols = st.columns(len(videos))
    for i, video in enumerate(videos):
        with cols[i]:
            st.markdown(f"""
            <div class="course-card" style="text-align: center;">
                <div style="font-size: 3rem;">{video['thumbnail']}</div>
                <h4>{video['title']}</h4>
                <p>Duration: {video['duration']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Watch", key=f"video_{i}"):
                st.success(f"Playing: {video['title']}")
                # Award coins for watching video
                db_manager.add_user_coins(st.session_state.user_data['id'], 6)
                st.info("You earned 6 coins for watching this video!")

def show_testimonials():
    """Show student testimonials"""
    testimonials = [
        {"name": "Rahul Sharma", "class": "Class 12", "text": "Sharpy helped me improve my marks by 40%!"},
        {"name": "Priya Das", "class": "Class 10", "text": "The live classes are amazing and interactive."},
        {"name": "Amit Singh", "class": "Engineering", "text": "Best platform for competitive exam preparation."},
    ]
    
    for testimonial in testimonials:
        st.markdown(f"""
        <div class="course-card">
            <h4>"{testimonial['text']}"</h4>
            <p><strong>- {testimonial['name']}</strong>, {testimonial['class']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_live_classes():
    """Show scheduled live classes for premium users"""
    classes = db_manager.get_today_live_classes(st.session_state.user_data['id'])
    
    if not classes:
        st.info("No live classes scheduled for today.")
        return
    
    for class_info in classes:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{class_info['subject']} - {class_info['topic']}**")
            st.write(f"Teacher: {class_info['teacher']}")
        
        with col2:
            st.write(f"⏰ {class_info['time']}")
        
        with col3:
            if st.button("Join Class", key=f"class_{class_info['id']}"):
                st.success("Joining live class...")

def show_enrolled_courses():
    """Show user's enrolled courses"""
    courses = db_manager.get_user_courses(st.session_state.user_data['id'])
    
    if not courses:
        st.info("You haven't enrolled in any courses yet.")
        return
    
    cols = st.columns(3)
    for i, course in enumerate(courses):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="course-card">
                <h4>{course['name']}</h4>
                <p>Progress: {course['progress']}%</p>
                <div style="background: #e2e8f0; border-radius: 10px; height: 10px;">
                    <div style="background: #667eea; height: 100%; width: {course['progress']}%; border-radius: 10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Continue Learning", key=f"course_{course['id']}"):
                st.success(f"Opening {course['name']}...")

def show_floating_buttons():
    """Show floating action buttons for call and WhatsApp"""
    st.markdown("""
    <div class="floating-buttons">
        <button class="floating-btn call" onclick="window.open('tel:+919876543210')" title="Call Us">📞</button>
        <button class="floating-btn" onclick="window.open('https://wa.me/919876543210')" title="WhatsApp">📱</button>
    </div>
    """, unsafe_allow_html=True)

# Main application logic
def main():
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        show_navigation()
        
        if st.session_state.current_page == 'home':
            show_home_page()
        elif st.session_state.current_page == 'courses':
            exec(open('pages/1_Courses.py').read())
        elif st.session_state.current_page == 'journey':
            exec(open('pages/2_Journey.py').read())
        elif st.session_state.current_page == 'notifications':
            exec(open('pages/3_Notifications.py').read())
        elif st.session_state.current_page == 'shorts':
            exec(open('pages/4_Shorts.py').read())
        
        show_floating_buttons()
    
    # Show footer on all pages
    show_footer()

def show_footer():
    """Show footer with copyright and developer information"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; color: #666; font-size: 14px; margin-top: 50px;'>
            <p><strong>© 2025 Sharpy. All rights reserved.</strong></p>
            <p>Developed by <strong>DG Developers</strong></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

def show_otp_login_section():
    """Show OTP-based login interface"""
    st.subheader("🔐 Login with OTP")
    
    # Initialize OTP session states
    if 'otp_step' not in st.session_state:
        st.session_state.otp_step = 'phone_input'
    if 'otp_phone' not in st.session_state:
        st.session_state.otp_phone = ''
    
    if st.session_state.otp_step == 'phone_input':
        with st.form("otp_phone_form"):
            phone = st.text_input("Enter your registered phone number", placeholder="+91XXXXXXXXXX")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.form_submit_button("Send OTP", type="primary"):
                    # Format and validate phone number
                    formatted_phone = otp_manager.format_phone_number(phone)
                    
                    if not otp_manager.is_valid_phone_number(formatted_phone):
                        st.error("Please enter a valid phone number (e.g., +919876543210)")
                    elif not db_manager.user_exists(formatted_phone):
                        st.error("Phone number not registered. Please create an account first.")
                    else:
                        # Generate and send OTP
                        otp = otp_manager.generate_otp()
                        if otp_manager.send_otp(formatted_phone, otp):
                            otp_manager.store_otp(formatted_phone, otp)
                            st.session_state.otp_phone = formatted_phone
                            st.session_state.otp_step = 'otp_input'
                            st.rerun()
                        else:
                            st.error("Failed to send OTP. Please try again.")
            
            with col2:
                if st.form_submit_button("Back to Login"):
                    st.session_state.show_otp_login = False
                    st.rerun()
    
    elif st.session_state.otp_step == 'otp_input':
        st.info(f"OTP sent to {st.session_state.otp_phone}")
        
        with st.form("otp_verify_form"):
            otp_input = st.text_input("Enter 6-digit OTP", max_chars=6)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.form_submit_button("Verify OTP", type="primary"):
                    if len(otp_input) != 6 or not otp_input.isdigit():
                        st.error("Please enter a valid 6-digit OTP")
                    else:
                        success, message = otp_manager.verify_otp(st.session_state.otp_phone, otp_input)
                        if success:
                            # Login successful
                            st.session_state.authenticated = True
                            st.session_state.user_data = auth_manager.get_user_data(st.session_state.otp_phone)
                            
                            # Clear OTP session states
                            st.session_state.otp_step = 'phone_input'
                            st.session_state.otp_phone = ''
                            st.session_state.show_otp_login = False
                            
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error(message)
            
            with col2:
                if st.form_submit_button("Resend OTP"):
                    success, message = otp_manager.resend_otp(st.session_state.otp_phone)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            with col3:
                if st.form_submit_button("Change Number"):
                    st.session_state.otp_step = 'phone_input'
                    st.session_state.otp_phone = ''
                    st.rerun()

if __name__ == "__main__":
    main()