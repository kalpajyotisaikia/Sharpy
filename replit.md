# Sharpy Educational App

## Overview

Sharpy Educational App is a comprehensive educational platform built with Streamlit that provides mobile authentication via OTP, course management, student journey tracking with coins/rewards, video streaming capabilities, test series functionality, and live classes with notifications. The application serves both premium and non-premium users with differentiated experiences.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with multi-page architecture
- **Layout**: Wide layout with responsive design and custom CSS styling
- **Navigation**: Button-based navigation with session state management
- **State Management**: Session state for user authentication and data persistence
- **UI Components**: Custom styled cards, progress bars, floating action buttons

### Backend Architecture
- **Database**: PostgreSQL with comprehensive user management and course data
- **Authentication**: Password hashing with SHA-256 and OTP support (Twilio integration ready)
- **User Management**: Role-based access with premium/non-premium differentiation
- **Rewards System**: Coin-based gamification for student engagement

### Key Design Patterns
- **Authentication-First**: User authentication required for main features
- **Gamification**: Coins and achievements system for user engagement
- **Premium Differentiation**: Different experiences for premium vs non-premium users
- **Modular Database Operations**: Centralized database management with utility classes

## Key Components

### 1. Main Application (app.py)
- **Authentication System**: Login/registration with password and OTP support
- **Home Dashboard**: Different experiences for premium/non-premium users
- **Navigation System**: Button-based page navigation
- **User Interface**: Custom CSS styling with responsive design
- **Session Management**: User authentication and data persistence

### 2. Authentication Module (utils/auth.py)
- **User Registration**: Comprehensive signup with educational details
- **Password Security**: SHA-256 password hashing
- **OTP Integration**: Ready for Twilio SMS authentication
- **User Validation**: Phone number uniqueness and credential verification

### 3. Database Management (utils/database.py)
- **PostgreSQL Integration**: Complete database schema and operations
- **User Management**: Registration, authentication, and profile data
- **Course System**: Course enrollment and progress tracking
- **Rewards System**: Coins, achievements, and activity tracking
- **Live Classes**: Scheduling and enrollment management
- **Notifications**: User notification system

### 4. Courses Page (pages/1_Courses.py)
- **Course Catalog**: Class-specific and cross-class course browsing
- **Enrollment System**: Course registration and progress tracking
- **Content Structure**: Chapter-based learning with video lectures
- **Premium Features**: Differentiated access for premium users

### 5. Journey Tracking (pages/2_Journey.py)
- **Analytics Dashboard**: Learning progress visualization with Plotly
- **Achievement System**: Badge-based gamification
- **Progress Tracking**: Course completion and performance metrics
- **Goal Setting**: Personal learning objectives and tracking

## Data Flow

### 1. Data Ingestion
1. User uploads file or connects to data source
2. DataLoader validates and processes data
3. Data stored in session state for persistence
4. Basic statistics calculated and displayed

### 2. AI Analysis Pipeline
1. Data summary prepared for AI consumption
2. OpenAI API called with structured prompts
3. AI responses parsed and formatted
4. Results stored in session state
5. Insights displayed with actionable recommendations

### 3. Visualization Workflow
1. User selects chart type or requests AI suggestions
2. VisualizationEngine creates Plotly figures
3. Charts rendered with interactive capabilities
4. Visualizations saved to session state gallery
5. Export options provided for sharing

### 4. Code Generation Process
1. User selects components to include
2. CodeGenerator creates reproducible Python code
3. Jupyter notebooks generated with markdown documentation
4. SQL queries created for database operations
5. Complete packages exported as ZIP files

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework and UI components
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and array operations
- **Plotly**: Interactive visualization library

### AI Integration
- **OpenAI**: GPT-4o model for intelligent analysis and suggestions
- **JSON**: Data serialization for AI prompt formatting

### Database Support
- **SQLAlchemy**: Database abstraction layer for multiple database types
- **Requests**: HTTP client for API data import

### File Processing
- **IO**: File handling and streaming
- **ZipFile**: Archive creation for export packages
- **Base64**: Encoding for file downloads

## Deployment Strategy

### Environment Configuration
- **API Keys**: OpenAI API key via environment variables
- **Database**: Optional database connections via environment variables
- **Debug Mode**: Streamlit development server for local testing

### Production Considerations
- **Security**: API key validation and secure handling
- **Performance**: Session state optimization for large datasets
- **Scalability**: Modular architecture allows for easy feature expansion
- **Error Handling**: Comprehensive error messages and graceful degradation

### Replit-Specific Setup
- Environment variables for API keys
- File upload handling for temporary storage
- Session state persistence across page navigation
- Responsive layout for various screen sizes

## Development Notes

The application follows a modular architecture with clear separation of concerns. Each utility module handles specific functionality, making the codebase maintainable and extensible. The AI integration is designed to be optional, allowing the application to function with limited features when API keys are not available.

The session state management ensures data persistence across page navigation, providing a seamless user experience. The code generation features make the tool valuable for both exploratory analysis and production workflows.