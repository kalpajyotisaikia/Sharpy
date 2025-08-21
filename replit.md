# Overview

Sharpy Educational Platform is a comprehensive learning management system built with Python and Streamlit. The platform combines traditional educational tools with gamification elements to create an engaging learning environment. It features phone number-based authentication with OTP verification, class-specific course management, student analytics tracking, and a coin-based reward system. The application supports both premium and standard users with different content access levels and includes educational video streaming, test series, notifications, and quick learning shorts.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit-based web application with multi-page navigation system
- **UI Design**: Responsive layout with custom CSS styling, gradient themes, and mobile-friendly design
- **Page Structure**: Five main sections organized as separate pages - Home, Courses, Journey (Analytics), Notifications, and Educational Shorts
- **Session Management**: Streamlit session state for maintaining user authentication and data persistence across page navigation
- **Navigation**: Multi-tab interfaces within each page for organized content delivery and user experience optimization

## Backend Architecture
- **Application Framework**: Modular Python architecture with utility classes for authentication, database operations, and OTP management
- **Authentication System**: SHA-256 password hashing with phone number-based login and multi-device session control
- **Database Layer**: PostgreSQL with psycopg2 driver and intelligent fallback to in-memory storage when database is unavailable
- **Data Models**: Comprehensive relational schema including users, courses, enrollments, test results, notifications, and user analytics
- **Error Handling**: Graceful degradation with fallback modes for database connectivity issues

## Database Design
- **Primary Database**: PostgreSQL with structured tables for user management, course hierarchy, enrollment tracking, and analytics
- **Schema Features**: Role-based access control, premium user differentiation, coin economy tracking, and device management
- **Connection Strategy**: Direct connection string configuration with automatic fallback to demo data when database is unavailable
- **Data Relationships**: Normalized schema with proper foreign key relationships between users, courses, enrollments, and activity tracking

## Authentication & Security
- **Phone Authentication**: Mobile number-based user registration with OTP verification as primary authentication method
- **Password Security**: SHA-256 encryption for password storage with secure session management
- **Device Management**: Configurable maximum login device limits per user with admin control capabilities
- **Session Security**: Server-side session state management with authentication persistence across page navigation

## Gamification System
- **Coin Economy**: Comprehensive reward system with different coin values for various activities (6 coins for video watching, 5-10 coins for tests based on performance, 1 coin for educational shorts, 30 coins for successful referrals)
- **Progress Tracking**: Real-time analytics for study time, content consumption, test performance, and learning streaks
- **Achievement System**: Visual progress indicators, performance metrics, and milestone celebrations
- **Engagement Features**: User journey analytics with animated progress displays and motivational messaging

## Content Management
- **Course Hierarchy**: Class-based course organization (Classes 6-12, Engineering/Medical Entrance) with cross-class exploration capabilities
- **Video Integration**: YouTube video embedding with view tracking and thumbnail-based navigation
- **Educational Content**: Multi-format learning resources including full courses, quick shorts, and interactive assessments
- **Test Series**: Subject-wise assessments with performance-based coin rewards and result tracking

# External Dependencies

## Database Services
- **PostgreSQL**: Primary database hosted on Render.com with direct connection string configuration
- **Connection String**: Hardcoded Render PostgreSQL URL for production deployment
- **Backup Strategy**: In-memory fallback storage when PostgreSQL is unavailable

## Communication Services
- **Twilio SMS API**: OTP delivery service for phone number verification during registration and login
- **Fallback Mode**: Demo OTP system when Twilio credentials are not available
- **Phone Number Management**: International phone number support with validation

## Development & Deployment
- **Streamlit Framework**: Web application framework for Python with built-in hosting capabilities
- **Render.com**: Cloud deployment platform with automatic builds from GitHub repositories
- **Environment Variables**: Configuration management for database URLs and Twilio API credentials

## Data Visualization
- **Plotly**: Interactive charts and graphs for user analytics, progress tracking, and performance visualization
- **Pandas**: Data manipulation and analysis for user statistics and learning analytics

## Package Management
- **Python 3.11**: Runtime environment with specific version pinning for consistent deployment
- **Requirements Management**: Separate requirement files for local development and production deployment
- **Dependencies**: Core libraries include psycopg2-binary for PostgreSQL, Twilio for SMS, and Plotly for visualizations