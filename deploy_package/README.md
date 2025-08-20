# Sharpy Educational App

A comprehensive educational platform built with Streamlit featuring mobile authentication, course management, student journey tracking with rewards, and live classes.

## Features

### 🔐 Authentication System
- Phone number-based registration
- Password authentication with secure hashing
- OTP support (Twilio integration ready)
- Premium/Non-premium user differentiation

### 📚 Course Management
- Class-specific course catalog
- Course enrollment and progress tracking
- Video lecture support
- Chapter-based learning structure

### 🎯 Student Journey Tracking
- Interactive progress dashboard with analytics
- Coin-based reward system
- Achievement badges and gamification
- Learning goal setting and tracking

### 📺 Video Content
- Educational shorts and reels
- Video streaming capabilities
- Interactive content browsing

### 🔔 Notifications & Communication
- Real-time notification system
- Live class scheduling and reminders
- User engagement tracking

### 📊 Analytics & Insights
- Learning progress visualization
- Performance tracking with Plotly charts
- Educational analytics dashboard

## Tech Stack

- **Frontend:** Streamlit web application
- **Database:** PostgreSQL with psycopg2
- **Authentication:** SHA-256 password hashing
- **Visualization:** Plotly for interactive charts
- **SMS Integration:** Twilio (optional)
- **Deployment:** Render.com ready

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r render_requirements.txt

# Run the application
streamlit run app.py
```

### Database Setup
The app automatically creates required database tables on first run:
- users
- courses
- subjects
- user_enrollments
- live_classes
- notifications

### Environment Variables
```bash
DATABASE_URL=postgresql://username:password@host:port/database
TWILIO_ACCOUNT_SID=your_account_sid (optional)
TWILIO_AUTH_TOKEN=your_auth_token (optional)
TWILIO_PHONE_NUMBER=your_phone_number (optional)
```

## Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to Render.com.

## Project Structure

```
sharpy-educational-app/
├── app.py                 # Main Streamlit application
├── utils/
│   ├── auth.py           # Authentication utilities
│   ├── database.py       # Database operations
│   └── otp_manager.py    # OTP management (Twilio)
├── pages/
│   ├── 1_Courses.py      # Course catalog and management
│   ├── 2_Journey.py      # Student progress tracking
│   ├── 3_Notifications.py # Notification center
│   └── 4_Shorts.py       # Educational video content
├── render_requirements.txt # Python dependencies
├── Procfile              # Render.com process configuration
├── runtime.txt           # Python version
└── README.md             # This file
```

## Key Features Details

### Authentication Flow
1. User registration with phone number validation
2. Secure password hashing with SHA-256
3. Optional OTP verification via Twilio
4. Session management with Streamlit

### Course System
- Hierarchical course structure (Class → Subject → Course → Chapters)
- Progress tracking with percentage completion
- Premium content access control
- Enrollment management

### Gamification
- Coin-based reward system for engagement
- Achievement badges for milestones
- Progress visualization with charts
- Learning streak tracking

### Database Schema
The app uses a comprehensive PostgreSQL schema with proper relationships:
- User management with profile data
- Course catalog with enrollment tracking
- Notification system for engagement
- Live class scheduling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please create an issue in the GitHub repository.