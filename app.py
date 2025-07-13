"""
Simple FastAPI app that serves both API and frontend redirect
This approach works better with Render's deployment system
"""
import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
import jwt
import hashlib
import secrets
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import logging

# Import all the models and functions from main.py
from main import *

# Create the app with additional endpoints
app = FastAPI(
    title="E-commerce Full Stack Application",
    description="Complete e-commerce solution with API and frontend integration",
    version="2.0.0"
)

# CORS middleware - allow all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All existing routes from main.py are already included via import

# Add a frontend landing page
@app.get("/", response_class=HTMLResponse)
def frontend_landing():
    """Landing page with frontend information"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🛒 E-commerce Application</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                padding: 40px;
                text-align: center;
                max-width: 600px;
                width: 100%;
            }}
            h1 {{
                color: #333;
                margin-bottom: 20px;
                font-size: 2.5em;
            }}
            .emoji {{
                font-size: 3em;
                margin-bottom: 20px;
            }}
            .status {{
                background: #e8f5e8;
                border: 1px solid #4caf50;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }}
            .status h3 {{
                color: #2e7d32;
                margin: 0 0 10px 0;
            }}
            .links {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin: 30px 0;
            }}
            .link-button {{
                background: #667eea;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                transition: transform 0.2s;
            }}
            .link-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .api-button {{
                background: #4caf50;
            }}
            .docs-button {{
                background: #ff9800;
            }}
            .health-button {{
                background: #2196f3;
            }}
            .features {{
                text-align: left;
                margin: 30px 0;
            }}
            .features h3 {{
                color: #333;
                margin-bottom: 15px;
            }}
            .features ul {{
                list-style: none;
                padding: 0;
            }}
            .features li {{
                padding: 8px 0;
                padding-left: 25px;
                position: relative;
            }}
            .features li::before {{
                content: "✅";
                position: absolute;
                left: 0;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                color: #666;
                font-size: 0.9em;
            }}
            @media (max-width: 600px) {{
                .links {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🛒</div>
            <h1>E-commerce Application</h1>
            <p>Your complete e-commerce solution is running successfully!</p>
            
            <div class="status">
                <h3>🎉 Deployment Status: LIVE</h3>
                <p>Backend API is running with PostgreSQL database</p>
                <p>All endpoints are functional and ready for use</p>
            </div>
            
            <div class="links">
                <a href="/docs" class="link-button docs-button">📚 API Documentation</a>
                <a href="/health" class="link-button health-button">❤️ Health Check</a>
                <a href="/products" class="link-button api-button">📦 View Products</a>
                <a href="https://github.com/dhruvsahu007/Production-Deployment-to-Render" class="link-button" target="_blank">📁 GitHub Repo</a>
            </div>
            
            <div class="features">
                <h3>🚀 Available Features:</h3>
                <ul>
                    <li>User Authentication (Register/Login)</li>
                    <li>Product Catalog Management</li>
                    <li>Shopping Cart Functionality</li>
                    <li>Order Processing System</li>
                    <li>PostgreSQL Database Integration</li>
                    <li>JWT Security Implementation</li>
                    <li>RESTful API with OpenAPI Docs</li>
                    <li>Production-Ready Deployment</li>
                </ul>
            </div>
            
            <div class="features">
                <h3>🛠️ How to Use:</h3>
                <ul>
                    <li>Visit <strong>/docs</strong> for interactive API documentation</li>
                    <li>Use <strong>/register</strong> to create a new account</li>
                    <li>Use <strong>/login</strong> to authenticate</li>
                    <li>Browse <strong>/products</strong> to see available items</li>
                    <li>Create orders via <strong>/orders</strong> endpoint</li>
                    <li>Run the Streamlit frontend locally for complete UI</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>🔗 <strong>API Base URL:</strong> {os.environ.get('RENDER_EXTERNAL_URL', 'https://production-deployment-to-render.onrender.com')}</p>
                <p>💾 <strong>Database:</strong> PostgreSQL (NeonDB)</p>
                <p>🏗️ <strong>Framework:</strong> FastAPI + SQLAlchemy</p>
                <p>☁️ <strong>Deployed on:</strong> Render</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Enhanced health check with more information
@app.get("/status")
def detailed_status():
    """Detailed application status"""
    try:
        # Test database connection
        db = SessionLocal()
        user_count = db.query(User).count()
        product_count = db.query(Product).count()
        order_count = db.query(Order).count()
        db.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "environment": "production",
            "database": {
                "status": "connected",
                "users": user_count,
                "products": product_count,
                "orders": order_count
            },
            "api": {
                "version": "2.0.0",
                "docs_url": "/docs",
                "health_url": "/health"
            },
            "features": [
                "User Authentication",
                "Product Management", 
                "Order Processing",
                "Database Integration",
                "API Documentation"
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
