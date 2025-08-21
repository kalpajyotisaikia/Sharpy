# Sharpy Educational Platform

## Overview

Sharpy Educational Platform is a comprehensive educational management system built with Python and Streamlit. It's designed to enhance learning experiences through interactive features, course management, and gamification elements. The platform supports multi-class educational content delivery with features like OTP-based authentication, progress tracking, coin-based rewards, and live class scheduling.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework providing a responsive, mobile-friendly interface
- **Multi-page Structure**: Organized using Streamlit's page routing system with dedicated pages for courses, journey tracking, notifications, and educational shorts
- **Session Management**: Client-side session state management for user authentication and navigation
- **Responsive Design**: Custom CSS styling with gradient themes and mobile-optimized layouts

### Backend Architecture
- **Language**: Python 3.11+ with object-oriented design patterns
- **Authentication System**: SHA-256 password hashing with OTP verification workflow
- **Business Logic**: Modular utility classes (AuthManager, DatabaseManager, OTPManager) following single responsibility principle
- **Session-based Security**: Server-side session management with device limitation controls
- **Fallback Architecture**: Graceful degradation to demo mode when external services are unavailable

### Data Storage Solutions
- **Primary Database**: PostgreSQL with connection pooling and optimized queries
- **Database Schema**: Comprehensive relational design supporting users, courses, enrollments, notifications, achievements, and analytics
- **Fallback Storage**: In-memory session storage for demo/development mode
- **Data Integrity**: Foreign key relationships and transaction management for data consistency

### Authentication and Authorization
- **Multi-factor Authentication**: Phone number + OTP verification for registration, password-based login for returning users
- **Role-based Access**: Premium vs. Standard user tiers with feature restrictions
- **Device Management**: Admin-controlled maximum login device limits per user
- **Session Security**: Secure session tokens with automatic expiry

### Gamification Engine
- **Coin Economy**: Points-based reward system for user engagement (videos watched, tests completed, referrals)
- **Achievement Tracking**: Progress analytics with visual dashboards using Plotly
- **Learning Analytics**: User journey tracking with study time, completion rates, and performance metrics
- **Referral System**: Built-in user acquisition mechanism with coin rewards

## External Dependencies

### Database Services
- **PostgreSQL**: Primary data persistence layer hosted on Render.com
- **psycopg2-binary**: PostgreSQL adapter for Python with binary optimizations

### Communication Services  
- **Twilio SMS API**: OTP delivery and verification service
- **Phone Number Validation**: International phone number format support

### Visualization Libraries
- **Plotly**: Interactive charts and analytics dashboards
- **Pandas**: Data manipulation and analysis for user metrics

### Deployment Platform
- **Render.com**: Cloud hosting platform for Python web applications
- **Streamlit Cloud**: Alternative deployment option with GitHub integration

### Development Dependencies
- **python-dotenv**: Environment variable management
- **setuptools**: Package distribution and dependency management