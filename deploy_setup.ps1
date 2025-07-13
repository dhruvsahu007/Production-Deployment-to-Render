# Production Deployment Script for Render (Windows)
Write-Host "🚀 Starting deployment setup for Render..." -ForegroundColor Green

# Create .gitignore
Write-Host "📝 Creating .gitignore..." -ForegroundColor Yellow
@"
__pycache__/
*.py[cod]
*`$py.class
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
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8

# Initialize git repository
Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
git init

# Add all files
Write-Host "📁 Adding files to git..." -ForegroundColor Yellow
git add .

# Initial commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: E-commerce API for Render deployment

Features:
- FastAPI e-commerce API
- JWT authentication
- Product and order management
- SQLAlchemy ORM
- Production-ready configuration
- Render deployment setup"

Write-Host "✅ Deployment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Next steps:" -ForegroundColor Cyan
Write-Host "1. Create a GitHub repository" -ForegroundColor White
Write-Host "2. Add remote: git remote add origin https://github.com/yourusername/ecommerce-api.git" -ForegroundColor White
Write-Host "3. Push to GitHub: git push -u origin main" -ForegroundColor White
Write-Host "4. Deploy to Render using the GitHub repository" -ForegroundColor White
Write-Host ""
Write-Host "📋 Render Configuration:" -ForegroundColor Cyan
Write-Host "- Build Command: pip install -r requirements.txt" -ForegroundColor White
Write-Host "- Start Command: uvicorn main:app --host 0.0.0.0 --port `$PORT" -ForegroundColor White
Write-Host "- Environment Variables needed:" -ForegroundColor White
Write-Host "  * SECRET_KEY=your-super-secret-key-here" -ForegroundColor Gray
Write-Host "  * DATABASE_URL=postgresql://username:password@hostname:port/database" -ForegroundColor Gray
