# Sharpy Educational App - Deployment Guide

## GitHub Export & Render.com Deployment

### Step 1: Export to GitHub

1. **Create a new GitHub repository:**
   - Go to [GitHub.com](https://github.com) and create a new repository
   - Name it "sharpy-educational-app" or similar
   - Make it public or private (your choice)
   - Don't initialize with README since we have files

2. **Download project files:**
   - Go to your development environment file explorer
   - Download all project files as a zip archive
   - Extract the zip file on your computer

3. **Upload to GitHub:**
   - Clone your new GitHub repository to your computer
   - Copy all project files to the repository folder
   - Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit - Sharpy Educational App"
   git push origin main
   ```

### Step 2: Deploy on Render.com

1. **Create Render.com account:**
   - Go to [Render.com](https://render.com)
   - Sign up or log in

2. **Create new Web Service:**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure deployment settings:**
   ```
   Name: sharpy-educational-app
   Environment: Python 3
   Build Command: pip install -r render_requirements.txt
   Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

4. **Set environment variables:**
   - In Render dashboard, go to your service
   - Click "Environment" tab
   - Add these variables:
   ```
   DATABASE_URL = postgresql://frudent_db_user:AXNmaumb01w93rfozH5oXEPxVxFKgLhm@dpg-d2hmfaemcj7s73br3hmg-a.oregon-postgres.render.com/frudent_db
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - You'll get a URL like: `https://sharpy-educational-app.onrender.com`

### Step 3: Optional - Custom Domain

1. **In Render dashboard:**
   - Go to your service settings
   - Click "Custom Domains"
   - Add your domain name
   - Follow DNS configuration instructions

### Files Created for Deployment:

- `render_requirements.txt` - Python dependencies for Render
- `Procfile` - Process configuration for deployment
- `runtime.txt` - Python version specification
- `.gitignore` - Files to exclude from Git
- `DEPLOYMENT_GUIDE.md` - This guide

### Important Notes:

1. **Database:** The app uses your existing Render PostgreSQL database
2. **Environment Variables:** Database URL is set via environment variables in production
3. **Port Configuration:** App automatically uses Render's assigned port
4. **Dependencies:** All required packages are listed in render_requirements.txt

### Troubleshooting:

- **Build fails:** Check render_requirements.txt for correct package versions
- **App won't start:** Verify the start command in Render settings
- **Database connection:** Ensure DATABASE_URL environment variable is set correctly
- **Authentication issues:** Check if database tables are created properly

### Local Development:

To run locally after GitHub export:
```bash
pip install -r render_requirements.txt
streamlit run app.py
```

The app will automatically connect to your Render database or use fallback mode for testing.