# Sharpy Educational Platform

## Overview

Sharpy Educational Platform is a comprehensive web-based learning management system built with Streamlit that combines traditional educational tools with gamification elements. The platform features mobile authentication via OTP, hierarchical course management, student journey tracking with a coin-based reward system, video content delivery, and real-time notifications. It's designed to enhance learning experiences through interactive features and intelligent tracking systems.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with multi-page architecture using a main `app.py` and separate page modules in the `pages/` directory
- **Layout**: Wide layout with responsive design and custom CSS styling featuring gradient headers and styled navigation buttons
- **Navigation**: Button-based navigation system with session state management for user authentication and data persistence
- **UI Components**: Custom styled cards, progress bars, floating action buttons, and interactive charts using Plotly
- **State Management**: Streamlit session state for user authentication, current page tracking, and user data storage

### Backend Architecture
- **Database**: PostgreSQL with comprehensive schema including users, courses, enrollments, notifications, and analytics tables
- **Authentication**: Multi-layered security with SHA-256 password hashing and OTP support via Twilio integration
- **User Management**: Role-based access control differentiating premium and non-premium users with configurable device limits
- **Gamification System**: Coin-based reward mechanism for user engagement (6 coins for videos, 5-10 coins for tests, 1 coin for shorts, 30 coins for referrals)
- **Fallback Mode**: Graceful degradation to in-memory storage when database connection fails

### Data Architecture
- **Users Table**: Comprehensive user profiles with educational details, premium status, and coin balances
- **Courses Table**: Hierarchical course structure with class-specific content and pricing
- **Progress Tracking**: Enrollment tracking, test results, and learning analytics
- **Notification System**: Multi-type notifications for test results, referrals, and admin announcements

### Key Design Patterns
- **Authentication-First Design**: All main features require user authentication with graceful redirects
- **Modular Database Operations**: Centralized DatabaseManager class with utility methods for all data operations
- **Premium Differentiation**: Different user experiences and content access based on premium status
- **Session-Based State**: Streamlit session state for maintaining user context across page navigation
- **Error Handling**: Comprehensive try-catch blocks with fallback modes for external service failures

## External Dependencies

### Core Dependencies
- **Streamlit** (≥1.28.0): Primary web framework for the application interface
- **PostgreSQL with psycopg2-binary** (≥2.9.7): Primary database for user data, courses, and analytics
- **Pandas** (≥2.0.0): Data manipulation and analysis for user analytics and reporting
- **Plotly** (≥5.15.0): Interactive charts and visualizations for learning analytics dashboard

### Communication Services
- **Twilio** (≥8.2.0): SMS service for OTP authentication and notifications (optional with demo fallback)

### Deployment Infrastructure
- **Render.com**: Cloud hosting platform with PostgreSQL database integration
- **Python 3.11**: Runtime environment specified for consistent deployment

### Development Tools
- **python-dotenv**: Environment variable management for configuration
- **setuptools**: Package management and distribution setup

### Database Configuration
- **Production Database**: Render PostgreSQL instance with connection string management
- **Development Fallback**: In-memory data storage when database is unavailable
- **Connection Pooling**: Managed through psycopg2 with error handling and reconnection logic