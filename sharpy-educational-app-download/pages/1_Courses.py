import streamlit as st
from utils.database import DatabaseManager

st.set_page_config(page_title="Courses", page_icon="📚", layout="wide")

def show_courses_page():
    """Show courses page with class-specific and other classes courses"""
    if not st.session_state.authenticated:
        st.warning("Please login to access courses.")
        return
    
    user_data = st.session_state.user_data
    db_manager = DatabaseManager()
    
    st.title("📚 Courses")
    st.markdown("Explore our comprehensive course offerings")
    
    # Tabs for current class and other classes
    tab1, tab2, tab3 = st.tabs(["My Class Courses", "Other Classes", "Enrolled Courses"])
    
    with tab1:
        st.subheader(f"Courses for {user_data['class']}")
        show_class_courses(user_data['class'], db_manager, user_data['id'])
    
    with tab2:
        st.subheader("Explore Other Classes")
        
        # Class selector
        all_classes = [
            "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", 
            "Class 11", "Class 12", "Engineering Entrance", "Medical Entrance"
        ]
        
        other_classes = [cls for cls in all_classes if cls != user_data['class']]
        selected_class = st.selectbox("Select Class:", other_classes)
        
        if selected_class:
            show_class_courses(selected_class, db_manager, user_data['id'])
    
    with tab3:
        st.subheader("Your Enrolled Courses")
        show_enrolled_courses(db_manager, user_data['id'])

def show_class_courses(class_level: str, db_manager: DatabaseManager, user_id: int):
    """Display courses for a specific class"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, 
                   CASE WHEN ue.user_id IS NOT NULL THEN TRUE ELSE FALSE END as is_enrolled
            FROM courses c
            LEFT JOIN user_enrollments ue ON c.id = ue.course_id AND ue.user_id = %s
            WHERE c.class = %s
            ORDER BY c.name
        """, (user_id, class_level))
        
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not courses:
            st.info(f"No courses available for {class_level} yet.")
            return
        
        # Display courses in grid
        cols = st.columns(2)
        for i, course in enumerate(courses):
            with cols[i % 2]:
                with st.container():
                    st.markdown("""
                    <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; margin: 10px 0; background: white;">
                    """, unsafe_allow_html=True)
                    
                    st.subheader(course[1])  # course name
                    st.write(course[2])  # description
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.write(f"**Class:** {course[3]}")
                        st.write(f"**Price:** ₹{course[4]:,.2f}")
                    
                    with col2:
                        if course[5]:  # is_premium
                            st.markdown("🌟 **Premium Course**")
                        else:
                            st.markdown("🆓 **Free Course**")
                    
                    # Enrollment button
                    if course[7]:  # is_enrolled
                        st.success("✅ Already Enrolled")
                        if st.button("Continue Learning", key=f"continue_{course[0]}"):
                            st.success(f"Opening {course[1]}...")
                    else:
                        if st.button(f"Enroll Now", key=f"enroll_{course[0]}", type="primary"):
                            if enroll_user_in_course(db_manager, user_id, course[0]):
                                st.success("Successfully enrolled! Refreshing page...")
                                st.rerun()
                            else:
                                st.error("Enrollment failed. Please try again.")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
    except Exception as e:
        st.error(f"Error loading courses: {e}")

def show_enrolled_courses(db_manager: DatabaseManager, user_id: int):
    """Display user's enrolled courses with progress"""
    courses = db_manager.get_user_courses(user_id)
    
    if not courses:
        st.info("You haven't enrolled in any courses yet. Check out our course offerings!")
        return
    
    for course in courses:
        with st.container():
            st.markdown("""
            <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; margin: 10px 0; background: white;">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.subheader(course['name'])
                st.write(course['description'])
            
            with col2:
                st.write(f"**Progress: {course['progress']}%**")
                # Progress bar
                progress_html = f"""
                <div style="background: #e0e0e0; border-radius: 10px; height: 20px; width: 100%;">
                    <div style="background: #4CAF50; height: 100%; width: {course['progress']}%; border-radius: 10px;"></div>
                </div>
                """
                st.markdown(progress_html, unsafe_allow_html=True)
            
            with col3:
                if st.button("Continue", key=f"continue_enrolled_{course['id']}"):
                    show_course_content(course)
            
            st.markdown("</div>", unsafe_allow_html=True)

def enroll_user_in_course(db_manager: DatabaseManager, user_id: int, course_id: int) -> bool:
    """Enroll user in a course"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_enrollments (user_id, course_id, progress)
            VALUES (%s, %s, 0)
        """, (user_id, course_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Add notification
        db_manager.add_notification(
            user_id, 
            "Course Enrollment", 
            "Successfully enrolled in new course!", 
            "success"
        )
        
        return True
    except Exception as e:
        print(f"Enrollment error: {e}")
        return False

def show_course_content(course: dict):
    """Show course content structure"""
    st.subheader(f"📖 {course['name']}")
    
    # Sample course structure
    chapters = [
        {
            "name": "Introduction to Concepts",
            "lectures": [
                {"name": "Getting Started", "duration": "15:30", "completed": True},
                {"name": "Basic Principles", "duration": "22:45", "completed": True},
                {"name": "Practice Problems", "duration": "18:20", "completed": False},
            ]
        },
        {
            "name": "Advanced Topics",
            "lectures": [
                {"name": "Complex Theories", "duration": "25:10", "completed": False},
                {"name": "Real-world Applications", "duration": "20:35", "completed": False},
                {"name": "Case Studies", "duration": "30:15", "completed": False},
            ]
        },
        {
            "name": "Assessment and Practice",
            "lectures": [
                {"name": "Practice Test 1", "duration": "60:00", "completed": False},
                {"name": "Mock Exam", "duration": "120:00", "completed": False},
            ]
        }
    ]
    
    for chapter in chapters:
        with st.expander(f"📚 {chapter['name']}"):
            for lecture in chapter['lectures']:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    if lecture['completed']:
                        st.write(f"✅ {lecture['name']}")
                    else:
                        st.write(f"📹 {lecture['name']}")
                
                with col2:
                    st.write(f"⏱️ {lecture['duration']}")
                
                with col3:
                    if lecture['completed']:
                        if st.button("Review", key=f"review_{lecture['name']}"):
                            st.success(f"Reviewing: {lecture['name']}")
                    else:
                        if st.button("Start", key=f"start_{lecture['name']}", type="primary"):
                            st.success(f"Starting: {lecture['name']}")
                            # Award coins for watching
                            db_manager = DatabaseManager()
                            db_manager.add_user_coins(st.session_state.user_data['id'], 6)

if __name__ == "__main__":
    show_courses_page()