"""
Unified application that serves both FastAPI backend and Streamlit frontend
"""
import os
import subprocess
import threading
import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn

# Import your existing FastAPI app
from main import app as fastapi_app

# Create a new unified app
app = FastAPI(
    title="E-commerce Full Stack Application",
    description="Complete e-commerce solution with API and frontend",
    version="1.0.0"
)

# Mount the existing FastAPI app
app.mount("/api", fastapi_app)

def run_streamlit():
    """Run Streamlit in a separate thread"""
    try:
        # Wait a bit for FastAPI to start
        time.sleep(3)
        
        # Start Streamlit on port 8501
        subprocess.run([
            "streamlit", "run", "ecommerce_frontend.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ])
    except Exception as e:
        print(f"Error starting Streamlit: {e}")

@app.get("/")
def root():
    """Redirect to frontend"""
    return RedirectResponse(url="/frontend")

@app.get("/frontend")
def frontend():
    """Serve frontend info"""
    return {
        "message": "Frontend is running",
        "frontend_url": "http://localhost:8501",
        "api_url": "/api",
        "docs_url": "/api/docs"
    }

@app.get("/health")
def health_check():
    """Combined health check"""
    return {
        "status": "healthy",
        "backend": "running",
        "frontend": "available at port 8501",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    # Start Streamlit in background thread
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Start FastAPI
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
