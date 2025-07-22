# Sharpy Educational App

A comprehensive educational platform with mobile authentication, course management, student journey tracking, and gamification features.

## Features

- 📱 **Mobile Authentication**: OTP-based login with Twilio integration
- 📚 **Course Management**: Class-specific courses with enrollment tracking
- 🎯 **Student Journey**: Analytics, achievements, and progress tracking
- 🔔 **Notifications**: Live class alerts and announcements
- 🎬 **Educational Shorts**: Quick learning videos with rewards
- 🪙 **Gamification**: Coin-based reward system

## Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with PostgreSQL database
- **Authentication**: Password hashing + OTP via Twilio
- **Visualizations**: Plotly for analytics charts
- **Database**: PostgreSQL with comprehensive schema

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Twilio account (optional, works in demo mode)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd sharpy-educational-app
```

2. **Install dependencies**
```bash
pip install streamlit psycopg2-binary twilio plotly pandas
```

3. **Set up environment variables**
Create a `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/sharpy_db
TWILIO_ACCOUNT_SID=your_twilio_sid (optional)
TWILIO_AUTH_TOKEN=your_twilio_token (optional)
TWILIO_PHONE_NUMBER=your_twilio_phone (optional)
```

4. **Run the application**
```bash
streamlit run app.py --server.port 5000
```

## Project Structure

```
sharpy-educational-app/
├── app.py                 # Main application file
├── utils/
│   ├── auth.py           # Authentication management
│   ├── database.py       # Database operations
│   └── otp_manager.py    # OTP handling with Twilio
├── pages/
│   ├── 1_Courses.py      # Course management
│   ├── 2_Journey.py      # Student analytics
│   ├── 3_Notifications.py # Notification system
│   └── 4_Shorts.py       # Educational videos
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md
```

## Database Schema

The app automatically creates these tables:
- `users` - User profiles and authentication
- `courses` - Course catalog and details
- `subjects` - Test subjects by class
- `user_enrollments` - Course enrollment tracking
- `live_classes` - Scheduled live sessions
- `user_activities` - Activity and coin tracking
- `test_results` - Test scores and results
- `notifications` - User notifications

## Features Overview

### Authentication System
- Username/password login
- OTP-based mobile authentication
- Secure password hashing
- Demo mode when Twilio not configured

### Course Management
- Class-specific course catalogs
- Cross-class course exploration
- Enrollment tracking with progress
- Chapter-based content structure

### Student Journey
- Learning analytics with charts
- Achievement badge system
- Progress tracking across courses
- Personal goal setting

### Gamification
- Coin rewards for activities:
  - Watching videos: 6 coins
  - Taking tests: 5 coins
  - Attending live classes: 10 coins
  - Completing shorts: 8-15 coins

## Usage

1. **Registration**: Create account with educational details
2. **Login**: Use password or OTP authentication
3. **Explore Courses**: Browse class-specific or other courses
4. **Track Progress**: View analytics in Journey section
5. **Earn Rewards**: Complete activities to earn coins
6. **Stay Updated**: Check notifications for announcements

## Development

### Running in Development Mode
```bash
streamlit run app.py --server.port 5000 --server.headless false
```

### Database Reset
The app automatically initializes the database with sample data on first run.

## Mobile App Version

For Android Studio development, see the `mobile-app/` directory for React Native or Flutter implementation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.