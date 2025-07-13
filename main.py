"""
E-commerce FastAPI Application for Render Deployment
"""
import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI app
app = FastAPI(
    title="E-commerce API",
    description="A production-ready e-commerce API deployed on Render",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category: str

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    category: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Security
security = HTTPBearer()

def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return get_password_hash(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    """Database dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Routes
@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "message": "E-commerce API is running on Render!",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    """Health check for monitoring."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"New user registered: {user.username}")
    return db_user

@app.post("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new product."""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    logger.info(f"New product created: {product.name} by user {current_user.username}")
    return db_product

@app.get("/products", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all products."""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new order."""
    total_amount = 0
    order_items = []
    
    # Validate products and calculate total
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        item_total = product.price * item.quantity
        total_amount += item_total
        order_items.append({
            "product": product,
            "quantity": item.quantity,
            "price": item_total
        })
    
    # Create order
    db_order = Order(
        user_id=current_user.id,
        total_amount=total_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items and update stock
    for item_data in order_items:
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item_data["product"].id,
            quantity=item_data["quantity"],
            price=item_data["price"]
        )
        db.add(db_order_item)
        
        # Update product stock
        item_data["product"].stock_quantity -= item_data["quantity"]
    
    db.commit()
    
    # Refresh to get items
    db.refresh(db_order)
    
    logger.info(f"New order created: {db_order.id} by user {current_user.username}")
    return db_order

@app.get("/orders", response_model=List[OrderResponse])
def read_user_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's orders."""
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get a specific order."""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
