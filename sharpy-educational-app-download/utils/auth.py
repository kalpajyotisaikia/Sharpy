import hashlib
import os
from utils.database import DatabaseManager

class AuthManager:
    """Handle user authentication and registration"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, name: str, phone: str, email: str, school: str, class_level: str, address: str, password: str) -> bool:
        """Register a new user"""
        try:
            # Check if phone number already exists
            if self.db.user_exists(phone):
                return False
            
            hashed_password = self.hash_password(password)
            
            # Insert user into database
            user_data = {
                'name': name,
                'phone': phone,
                'email': email,
                'school': school,
                'class': class_level,
                'address': address,
                'password': hashed_password,
                'is_premium': False,
                'coins': 0,
                'max_devices': 2  # Default maximum login devices
            }
            
            return self.db.create_user(user_data)
            
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    def login_user(self, phone: str, password: str) -> bool:
        """Authenticate user login"""
        try:
            user = self.db.get_user_by_phone(phone)
            if not user:
                return False
            
            hashed_password = self.hash_password(password)
            return user['password'] == hashed_password
            
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def get_user_data(self, phone: str) -> dict:
        """Get user data by phone number"""
        return self.db.get_user_by_phone(phone)
    
    def send_otp(self, phone: str) -> bool:
        """Send OTP to phone number (placeholder for Twilio integration)"""
        # This would integrate with Twilio API
        # For now, return True as placeholder
        return True
    
    def verify_otp(self, phone: str, otp: str) -> bool:
        """Verify OTP (placeholder for Twilio integration)"""
        # This would integrate with Twilio API
        # For now, return True as placeholder
        return True