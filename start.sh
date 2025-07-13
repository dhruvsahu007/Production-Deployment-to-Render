#!/bin/bash
# Start script for unified deployment

echo "🚀 Starting E-commerce Full Stack Application..."

# Start FastAPI backend on port $PORT
echo "📡 Starting FastAPI backend..."
uvicorn main:app --host 0.0.0.0 --port $PORT &
FASTAPI_PID=$!

# Wait for FastAPI to start
sleep 5

# Start Streamlit frontend on port 8501
echo "🌐 Starting Streamlit frontend..."
streamlit run ecommerce_frontend.py --server.port 8501 --server.headless true &
STREAMLIT_PID=$!

echo "✅ Both services started:"
echo "   Backend API: Port $PORT"
echo "   Frontend: Port 8501"

# Wait for any process to exit
wait $FASTAPI_PID $STREAMLIT_PID
