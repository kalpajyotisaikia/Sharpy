# Overview

Sharpy Educational Platform is a comprehensive learning management system built with Python and Streamlit. The platform combines traditional educational tools with gamification elements to create an engaging learning environment. It features mobile authentication via OTP, class-specific course management, student progress tracking, and a coin-based reward system to motivate learners.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit-based web application with multi-page navigation
- **UI Design**: Responsive layout with custom CSS styling and gradient themes
- **Page Structure**: Five main sections - Home, Courses, Journey (Analytics), Notifications, and Educational Shorts
- **Session Management**: Streamlit session state for user authentication and data persistence

## Backend Architecture
- **Application Framework**: Python-based modular architecture with utility classes
- **Authentication System**: SHA-256 password hashing with phone number-based login
- **OTP Integration**: Twilio SMS service with fallback demo mode for development
- **Database Layer**: PostgreSQL with psycopg2 driver and fallback in-memory storage
- **Data Models**: Comprehensive schema including users, courses, enrollments, notifications, and analytics

## Database Design
- **Primary Database**: PostgreSQL with structured tables for users, courses, enrollments, test results, and notifications
- **Connection Management**: Direct connection string configuration with error handling
- **Fallback Strategy**: In-memory data storage when database is unavailable
- **Schema Features**: Role-based access control, premium user tracking, and coin economy system

## Authentication & Security
- **Phone Authentication**: Mobile number-based registration with OTP verification
- **Password Security**: SHA-256 encryption for password storage
- **Session Security**: Server-side session management with authentication state tracking
- **Device Management**: Configurable maximum login device limits per user

## Gamification System
- **Coin Economy**: Reward system for various user activities (video watching, test completion, referrals)
- **Progress Tracking**: Analytics for study time, content consumption, and test performance
- **Achievement System**: Visual progress indicators and performance metrics
- **Engagement Features**: Streak tracking and milestone celebrations

## Content Management
- **Course Hierarchy**: Class-based course organization with cross-class exploration
- **Video Integration**: YouTube video embedding with view tracking
- **Educational Shorts**: Quick learning content with filtering capabilities
- **Test Series**: Subject-wise assessments with score-based coin rewards

# External Dependencies

## Database Services
- **PostgreSQL**: Primary data storage with Render.com hosted database
- **Connection String**: Direct database URL configuration for production deployment

## Communication Services
- **Twilio SMS**: OTP delivery service for mobile authentication
- **Required Credentials**: Account SID, Auth Token, and Phone Number
- **Fallback Mode**: Demo OTP system when Twilio credentials unavailable

## Python Libraries
- **Streamlit**: Web application framework for UI rendering
- **psycopg2-binary**: PostgreSQL database connectivity
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive data visualization and analytics charts
- **python-dotenv**: Environment variable management

## Deployment Platform
- **Render.com**: Web service hosting with automatic deployment
- **Runtime**: Python 3.11 environment
- **Process Management**: Streamlit server with configurable port binding

## Development Tools
- **setuptools**: Package distribution and dependency management
- **pytest**: Testing framework for development workflow
- **black/flake8**: Code formatting and linting tools