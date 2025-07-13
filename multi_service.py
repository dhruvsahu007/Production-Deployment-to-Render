"""
Multi-service application launcher for Render deployment
Serves both FastAPI backend and Streamlit frontend
"""
import os
import subprocess
import threading
import time
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

class MultiServiceApp:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_fastapi(self):
        """Start FastAPI backend"""
        try:
            port = os.environ.get("PORT", "8000")
            print(f"🚀 Starting FastAPI backend on port {port}...")
            
            process = subprocess.Popen([
                "uvicorn", "main:app",
                "--host", "0.0.0.0",
                "--port", port
            ])
            self.processes.append(process)
            process.wait()
            
        except Exception as e:
            print(f"❌ Error starting FastAPI: {e}")
    
    def start_streamlit(self):
        """Start Streamlit frontend"""
        try:
            # Wait for FastAPI to start
            time.sleep(5)
            
            print("🌐 Starting Streamlit frontend on port 8501...")
            
            # Update the frontend to connect to the correct API URL
            api_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost:8000')}"
            
            # Set environment variable for frontend
            os.environ['API_BASE_URL'] = api_url
            
            process = subprocess.Popen([
                "streamlit", "run", "ecommerce_frontend.py",
                "--server.port", "8501",
                "--server.headless", "true",
                "--server.enableCORS", "false",
                "--server.enableXsrfProtection", "false",
                "--server.address", "0.0.0.0"
            ])
            self.processes.append(process)
            process.wait()
            
        except Exception as e:
            print(f"❌ Error starting Streamlit: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("🛑 Shutting down services...")
        self.running = False
        for process in self.processes:
            try:
                process.terminate()
            except:
                pass
        sys.exit(0)
    
    def run(self):
        """Run both services"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🚀 Starting E-commerce Full Stack Application...")
        
        # Use ThreadPoolExecutor to run both services
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Start both services
            fastapi_future = executor.submit(self.start_fastapi)
            streamlit_future = executor.submit(self.start_streamlit)
            
            try:
                # Wait for both to complete
                fastapi_future.result()
                streamlit_future.result()
            except KeyboardInterrupt:
                print("🛑 Received interrupt signal")
                self.signal_handler(None, None)

if __name__ == "__main__":
    app = MultiServiceApp()
    app.run()
