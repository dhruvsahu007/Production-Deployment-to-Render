@echo off
echo 🚀 Starting E-commerce API deployment setup...
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🔗 Next steps for Render deployment:
echo 1. Run: git init
echo 2. Run: git add .
echo 3. Run: git commit -m "Initial commit"
echo 4. Create GitHub repository
echo 5. Run: git remote add origin https://github.com/yourusername/ecommerce-api.git
echo 6. Run: git push -u origin main
echo 7. Deploy to Render using the GitHub repository
echo.
echo 📋 Render Configuration:
echo - Build Command: pip install -r requirements.txt
echo - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
echo - Environment Variables:
echo   * SECRET_KEY=your-super-secret-key-here
echo   * DATABASE_URL=postgresql://username:password@hostname:port/database
echo.
echo 🧪 To test locally:
echo - Run: uvicorn main:app --reload
echo - Open: http://localhost:8000/docs
echo.
pause
