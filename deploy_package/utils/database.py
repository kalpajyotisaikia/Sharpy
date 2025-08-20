import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date
import json

class DatabaseManager:
    """Manage database operations for the Sharpy Education app"""
    
    def __init__(self):
        # Use environment variable for production, fallback for development
        self.connection_string = os.getenv('DATABASE_URL') or "postgresql://frudent_db_user:AXNmaumb01w93rfozH5oXEPxVxFKgLhm@dpg-d2hmfaemcj7s73br3hmg-a.oregon-postgres.render.com/frudent_db"
        self.fallback_mode = False
        self.users_data = {}  # Fallback storage
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        try:
            if self.connection_string:
                return psycopg2.connect(self.connection_string)
            else:
                return None
        except Exception as e:
            print(f"Database connection error: {e}")
            self.fallback_mode = True
            return None
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = self.get_connection()
            if not conn:
                print("Database connection failed. Using fallback mode.")
                self.fallback_mode = True
                self._init_fallback_data()
                return
            
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
            self.fallback_mode = True
            self._init_fallback_data()
    
    def _init_fallback_data(self):
        """Initialize fallback data when database is not available"""
        self.users_data = {}
        self.subjects_data = [
            {'id': 1, 'name': 'Mathematics', 'class': 'Class 10', 'duration': 90, 'questions': 60},
            {'id': 2, 'name': 'Physics', 'class': 'Class 10', 'duration': 90, 'questions': 60},
            {'id': 3, 'name': 'Chemistry', 'class': 'Class 10', 'duration': 90, 'questions': 60},
            {'id': 4, 'name': 'Biology', 'class': 'Class 10', 'duration': 90, 'questions': 60},
        ]
        self.courses_data = [
            {'id': 1, 'name': 'Complete Mathematics Course', 'class': 'Class 10', 'price': 5000.00, 'is_premium': True},
            {'id': 2, 'name': 'Physics Mastery', 'class': 'Class 10', 'price': 4500.00, 'is_premium': True},
        ]
    
    def insert_sample_data(self):
        """Insert sample data for testing"""
        if self.fallback_mode:
            return
        
        try:
            conn = self.get_connection()
            if not conn:
                return
                
            cursor = conn.cursor()
            
            # Sample subjects
            sample_subjects = [
                ('Mathematics', 'Class 10', 90, 60),
                ('Physics', 'Class 10', 90, 60),
                ('Chemistry', 'Class 10', 90, 60),
                ('Biology', 'Class 10', 90, 60),
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
            ]
            
            cursor.execute("SELECT COUNT(*) FROM courses")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO courses (name, description, class, price, is_premium) VALUES (%s, %s, %s, %s, %s)",
                    sample_courses
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Sample data insertion error: {e}")
    
    def user_exists(self, phone: str) -> bool:
        """Check if user exists by phone number"""
        if self.fallback_mode:
            return phone in self.users_data
        
        try:
            conn = self.get_connection()
            if not conn:
                return False
                
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
        if self.fallback_mode:
            # Store in fallback
            user_id = len(self.users_data) + 1
            user_data['id'] = user_id
            self.users_data[user_data['phone']] = user_data
            return True
        
        try:
            conn = self.get_connection()
            if not conn:
                return False
                
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
        if self.fallback_mode:
            return self.users_data.get(phone)
        
        try:
            conn = self.get_connection()
            if not conn:
                return None
                
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
        if self.fallback_mode:
            for user in self.users_data.values():
                if user.get('id') == user_id:
                    return user.get('coins', 0)
            return 0
        
        try:
            conn = self.get_connection()
            if not conn:
                return 0
                
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
        if self.fallback_mode:
            for user in self.users_data.values():
                if user.get('id') == user_id:
                    user['coins'] = user.get('coins', 0) + coins
                    return True
            return False
        
        try:
            conn = self.get_connection()
            if not conn:
                return False
                
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
        if self.fallback_mode:
            for user in self.users_data.values():
                if user.get('id') == user_id:
                    return user.get('is_premium', False)
            return False
        
        try:
            conn = self.get_connection()
            if not conn:
                return False
                
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
        if self.fallback_mode:
            return [s for s in self.subjects_data if s['class'] == class_level]
        
        try:
            conn = self.get_connection()
            if not conn:
                return []
                
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
        # Return empty list for demo
        return []
    
    def get_user_courses(self, user_id: int) -> list:
        """Get user's enrolled courses"""
        # Return empty list for demo
        return []
    
    def add_notification(self, user_id: int, title: str, message: str, notification_type: str = 'info') -> bool:
        """Add notification for user"""
        return True  # Demo mode
    
    def get_user_notifications(self, user_id: int) -> list:
        """Get user's notifications"""
        return []  # Demo mode