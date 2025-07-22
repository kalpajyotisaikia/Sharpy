import os
import random
import string
from datetime import datetime, timedelta
import streamlit as st
from twilio.rest import Client

class OTPManager:
    """Handle OTP generation and verification with Twilio"""
    
    def __init__(self):
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN') 
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        # Initialize Twilio client if credentials are available
        if self.twilio_account_sid and self.twilio_auth_token:
            self.client = Client(self.twilio_account_sid, self.twilio_auth_token)
        else:
            self.client = None
    
    def generate_otp(self, length: int = 6) -> str:
        """Generate random OTP"""
        return ''.join(random.choices(string.digits, k=length))
    
    def send_otp(self, phone_number: str, otp: str) -> bool:
        """Send OTP via SMS using Twilio"""
        if not self.client:
            # Fallback: store OTP in session for demo purposes
            st.session_state.demo_otp = otp
            st.session_state.demo_phone = phone_number
            st.info(f"Demo Mode: Your OTP is {otp} (This would normally be sent via SMS)")
            return True
        
        try:
            message = self.client.messages.create(
                body=f"Your Sharpy Education verification code is: {otp}. Valid for 5 minutes.",
                from_=self.twilio_phone_number,
                to=phone_number
            )
            return True
        except Exception as e:
            print(f"SMS sending error: {e}")
            return False
    
    def store_otp(self, phone_number: str, otp: str) -> None:
        """Store OTP with expiry time"""
        expiry_time = datetime.now() + timedelta(minutes=5)
        
        # Store in session state (in production, use Redis or database)
        if 'otp_data' not in st.session_state:
            st.session_state.otp_data = {}
        
        st.session_state.otp_data[phone_number] = {
            'otp': otp,
            'expiry': expiry_time,
            'attempts': 0
        }
    
    def verify_otp(self, phone_number: str, entered_otp: str) -> tuple[bool, str]:
        """Verify OTP and return status with message"""
        
        # Check demo mode first
        if hasattr(st.session_state, 'demo_otp') and hasattr(st.session_state, 'demo_phone'):
            if st.session_state.demo_phone == phone_number and st.session_state.demo_otp == entered_otp:
                # Clear demo OTP after successful verification
                delattr(st.session_state, 'demo_otp')
                delattr(st.session_state, 'demo_phone')
                return True, "OTP verified successfully!"
            else:
                return False, "Invalid OTP. Please try again."
        
        # Check if OTP data exists
        if 'otp_data' not in st.session_state or phone_number not in st.session_state.otp_data:
            return False, "No OTP found. Please request a new OTP."
        
        otp_info = st.session_state.otp_data[phone_number]
        
        # Check if OTP has expired
        if datetime.now() > otp_info['expiry']:
            del st.session_state.otp_data[phone_number]
            return False, "OTP has expired. Please request a new one."
        
        # Check attempt limit
        if otp_info['attempts'] >= 3:
            del st.session_state.otp_data[phone_number]
            return False, "Too many failed attempts. Please request a new OTP."
        
        # Verify OTP
        if otp_info['otp'] == entered_otp:
            del st.session_state.otp_data[phone_number]
            return True, "OTP verified successfully!"
        else:
            # Increment attempts
            st.session_state.otp_data[phone_number]['attempts'] += 1
            remaining_attempts = 3 - st.session_state.otp_data[phone_number]['attempts']
            return False, f"Invalid OTP. {remaining_attempts} attempts remaining."
    
    def resend_otp(self, phone_number: str) -> tuple[bool, str]:
        """Resend OTP to phone number"""
        # Generate new OTP
        new_otp = self.generate_otp()
        
        # Send OTP
        if self.send_otp(phone_number, new_otp):
            self.store_otp(phone_number, new_otp)
            return True, "New OTP sent successfully!"
        else:
            return False, "Failed to send OTP. Please try again."
    
    def is_valid_phone_number(self, phone_number: str) -> bool:
        """Validate phone number format"""
        # Basic validation for Indian phone numbers
        if not phone_number.startswith('+91'):
            return False
        
        # Remove country code and check if remaining digits are valid
        number_part = phone_number[3:]
        if len(number_part) != 10 or not number_part.isdigit():
            return False
        
        return True
    
    def format_phone_number(self, phone_number: str) -> str:
        """Format phone number to standard format"""
        # Remove any spaces or special characters
        cleaned_number = ''.join(filter(str.isdigit, phone_number))
        
        # Add country code if missing
        if len(cleaned_number) == 10:
            return f"+91{cleaned_number}"
        elif len(cleaned_number) == 12 and cleaned_number.startswith('91'):
            return f"+{cleaned_number}"
        else:
            return phone_number
    
    def cleanup_expired_otps(self) -> None:
        """Clean up expired OTPs from session"""
        if 'otp_data' not in st.session_state:
            return
        
        current_time = datetime.now()
        expired_phones = []
        
        for phone, otp_info in st.session_state.otp_data.items():
            if current_time > otp_info['expiry']:
                expired_phones.append(phone)
        
        for phone in expired_phones:
            del st.session_state.otp_data[phone]