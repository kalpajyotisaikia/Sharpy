import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date
import json

class DatabaseManager:
    """Manage database operations for the Sharpy Education app"""
    
    def __init__(self):
        self.connection_string = os.getenv('DATABASE_URL')
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.connection_string)
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(20) UNIQUE NOT NULL,
                    email VARCHAR(255),
                    school VARCHAR(255),
                    class VARCHAR(50),
                    address TEXT,
                    password VARCHAR(255) NOT NULL,
                    is_premium BOOLEAN DEFAULT FALSE,
                    coins INTEGER DEFAULT 0,
                    max_devices INTEGER DEFAULT 2,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Courses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    class VARCHAR(50) NOT NULL,
                    price DECIMAL(10,2) DEFAULT 0,
                    is_premium BOOLEAN DEFAULT FALSE,
                    thumbnail_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Subjects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    class VARCHAR(50) NOT NULL,
                    duration INTEGER DEFAULT 60,
                    questions INTEGER DEFAULT 50,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User enrollments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_enrollments (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    course_id INTEGER REFERENCES courses(id),
                    progress INTEGER DEFAULT 0,
                    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Live classes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS live_classes (
                    id SERIAL PRIMARY KEY,
                    subject VARCHAR(255) NOT NULL,
                    topic VARCHAR(255) NOT NULL,
                    teacher VARCHAR(255) NOT NULL,
                    class_date DATE NOT NULL,
                    class_time TIME NOT NULL,
                    duration INTEGER DEFAULT 60,
                    class VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User activities table (for coins tracking)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_activities (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    activity_type VARCHAR(50) NOT NULL,
                    coins_earned INTEGER DEFAULT 0,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Test results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_results (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    subject_id INTEGER REFERENCES subjects(id),
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    time_taken INTEGER,
                    coins_earned INTEGER DEFAULT 0,
                    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Notifications table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    type VARCHAR(50) DEFAULT 'info',
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Insert sample data
            self.insert_sample_data()
            
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def insert_sample_data(self):
        """Insert sample data for testing"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Sample subjects
            sample_subjects = [
                ('Mathematics', 'Class 10', 90, 60),
                ('Physics', 'Class 10', 90, 60),
                ('Chemistry', 'Class 10', 90, 60),
                ('Biology', 'Class 10', 90, 60),
                ('Mathematics', 'Class 12', 120, 80),
                ('Physics', 'Class 12', 120, 80),
                ('Chemistry', 'Class 12', 120, 80),
                ('Biology', 'Class 12', 120, 80),
            ]
            
            cursor.execute("SELECT COUNT(*) FROM subjects")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO subjects (name, class, duration, questions) VALUES (%s, %s, %s, %s)",
                    sample_subjects
                )
            
            # Sample courses
            sample_courses = [
                ('Complete Mathematics Course', 'Comprehensive math course for Class 10', 'Class 10', 5000.00, True),
                ('Physics Mastery', 'Master physics concepts for Class 10', 'Class 10', 4500.00, True),
                ('Chemistry Fundamentals', 'Essential chemistry for Class 10', 'Class 10', 4000.00, True),
                ('Biology Basics', 'Complete biology course for Class 10', 'Class 10', 3500.00, True),
                ('Advanced Mathematics', 'Advanced math for Class 12', 'Class 12', 8000.00, True),
                ('Physics for JEE', 'Physics preparation for JEE', 'Class 12', 7500.00, True),
            ]
            
            cursor.execute("SELECT COUNT(*) FROM courses")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO courses (name, description, class, price, is_premium) VALUES (%s, %s, %s, %s, %s)",
                    sample_courses
                )
            
            # Sample live classes for today
            today = date.today()
            sample_classes = [
                ('Mathematics', 'Quadratic Equations', 'Dr. Sharma', today, '10:00:00', 60, 'Class 10'),
                ('Physics', 'Light and Reflection', 'Prof. Patel', today, '14:00:00', 60, 'Class 10'),
                ('Chemistry', 'Acids and Bases', 'Dr. Singh', today, '16:00:00', 60, 'Class 10'),
            ]
            
            cursor.execute("DELETE FROM live_classes WHERE class_date = %s", (today,))
            cursor.executemany(
                "INSERT INTO live_classes (subject, topic, teacher, class_date, class_time, duration, class) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                sample_classes
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Sample data insertion error: {e}")
    
    def user_exists(self, phone: str) -> bool:
        """Check if user exists by phone number"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result is not None
        except Exception as e:
            print(f"User exists check error: {e}")
            return False
    
    def create_user(self, user_data: dict) -> bool:
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, phone, email, school, class, address, password, is_premium, coins, max_devices)
                VALUES (%(name)s, %(phone)s, %(email)s, %(school)s, %(class)s, %(address)s, %(password)s, %(is_premium)s, %(coins)s, %(max_devices)s)
            """, user_data)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Create user error: {e}")
            return False
    
    def get_user_by_phone(self, phone: str) -> dict:
        """Get user data by phone number"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM users WHERE phone = %s", (phone,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Get user error: {e}")
            return None
    
    def get_user_coins(self, user_id: int) -> int:
        """Get user's current coin balance"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT coins FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Get user coins error: {e}")
            return 0
    
    def add_user_coins(self, user_id: int, coins: int) -> bool:
        """Add coins to user account"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET coins = coins + %s WHERE id = %s", (coins, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Add user coins error: {e}")
            return False
    
    def is_premium_user(self, user_id: int) -> bool:
        """Check if user is premium"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT is_premium FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else False
        except Exception as e:
            print(f"Is premium user error: {e}")
            return False
    
    def get_subjects_by_class(self, class_level: str) -> list:
        """Get subjects for a specific class"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM subjects WHERE class = %s", (class_level,))
            subjects = cursor.fetchall()
            cursor.close()
            conn.close()
            return [dict(subject) for subject in subjects]
        except Exception as e:
            print(f"Get subjects error: {e}")
            return []
    
    def get_today_live_classes(self, user_id: int) -> list:
        """Get today's live classes for user's class"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get user's class first
            cursor.execute("SELECT class FROM users WHERE id = %s", (user_id,))
            user_class = cursor.fetchone()
            if not user_class:
                return []
            
            today = date.today()
            cursor.execute("""
                SELECT * FROM live_classes 
                WHERE class_date = %s AND class = %s
                ORDER BY class_time
            """, (today, user_class['class']))
            
            classes = cursor.fetchall()
            cursor.close()
            conn.close()
            return [dict(cls) for cls in classes]
        except Exception as e:
            print(f"Get live classes error: {e}")
            return []
    
    def get_user_courses(self, user_id: int) -> list:
        """Get user's enrolled courses"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT c.id, c.name, c.description, ue.progress
                FROM courses c
                JOIN user_enrollments ue ON c.id = ue.course_id
                WHERE ue.user_id = %s
            """, (user_id,))
            courses = cursor.fetchall()
            cursor.close()
            conn.close()
            return [dict(course) for course in courses]
        except Exception as e:
            print(f"Get user courses error: {e}")
            return []
    
    def add_notification(self, user_id: int, title: str, message: str, notification_type: str = 'info') -> bool:
        """Add notification for user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notifications (user_id, title, message, type)
                VALUES (%s, %s, %s, %s)
            """, (user_id, title, message, notification_type))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Add notification error: {e}")
            return False
    
    def get_user_notifications(self, user_id: int) -> list:
        """Get user's notifications"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM notifications 
                WHERE user_id = %s 
                ORDER BY created_at DESC
                LIMIT 50
            """, (user_id,))
            notifications = cursor.fetchall()
            cursor.close()
            conn.close()
            return [dict(notif) for notif in notifications]
        except Exception as e:
            print(f"Get notifications error: {e}")
            return []