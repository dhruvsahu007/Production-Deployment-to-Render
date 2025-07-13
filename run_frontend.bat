@echo off
echo 🚀 Starting E-commerce Frontend Application...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo 🌐 Starting Streamlit frontend...
echo Frontend will be available at: http://localhost:8501
echo Backend API: https://production-deployment-to-render.onrender.com
echo.

streamlit run ecommerce_frontend.py
