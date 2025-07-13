#!/bin/bash

# Production Deployment Script for Render
echo "🚀 Starting deployment setup for Render..."

# Create .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << EOF
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
myenv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Environment variables
.env
.env.local
.env.production
EOF

# Initialize git repository
echo "📦 Initializing git repository..."
git init

# Add all files
echo "📁 Adding files to git..."
git add .

# Initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: E-commerce API for Render deployment

Features:
- FastAPI e-commerce API
- JWT authentication
- Product and order management
- SQLAlchemy ORM
- Production-ready configuration
- Render deployment setup"

echo "✅ Deployment setup complete!"
echo ""
echo "🔗 Next steps:"
echo "1. Create a GitHub repository"
echo "2. Add remote: git remote add origin https://github.com/yourusername/ecommerce-api.git"
echo "3. Push to GitHub: git push -u origin main"
echo "4. Deploy to Render using the GitHub repository"
echo ""
echo "📋 Render Configuration:"
echo "- Build Command: pip install -r requirements.txt"
echo "- Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "- Environment Variables needed:"
echo "  * SECRET_KEY=your-super-secret-key-here"
echo "  * DATABASE_URL=postgresql://username:password@hostname:port/database"
