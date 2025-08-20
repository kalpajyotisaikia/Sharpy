#!/bin/bash

# Sharpy Educational App - GitHub Deployment Script
echo "🚀 Preparing Sharpy Educational App for GitHub deployment..."

# Create deployment package
echo "📦 Creating deployment package..."
mkdir -p deploy_package
cp -r app.py utils/ pages/ deploy_package/
cp render_requirements.txt deploy_package/
cp Procfile deploy_package/
cp runtime.txt deploy_package/
cp .gitignore deploy_package/
cp README.md deploy_package/
cp DEPLOYMENT_GUIDE.md deploy_package/

echo "✅ Deployment package created in 'deploy_package' folder"
echo ""
echo "📋 Next steps:"
echo "1. Create a new GitHub repository"
echo "2. Upload the contents of 'deploy_package' folder"
echo "3. Follow DEPLOYMENT_GUIDE.md for Render.com deployment"
echo ""
echo "🔗 Your database is already configured for production!"
echo "Database URL: postgresql://frudent_db_user:***@dpg-d2hmfaemcj7s73br3hmg-a.oregon-postgres.render.com/frudent_db"