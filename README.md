# 🛒 Complete E-commerce Application - Production Deployment

A full-stack e-commerce application with FastAPI backend and Streamlit frontend, deployed on Render with PostgreSQL database.

## 🌐 **Live Deployment**

- **Backend API:** https://production-deployment-to-render.onrender.com
- **API Documentation:** https://production-deployment-to-render.onrender.com/docs
- **Health Check:** https://production-deployment-to-render.onrender.com/health

## ✨ **Complete Features**

### 🔐 **User Authentication**
- User registration and login
- JWT-based authentication
- Secure password hashing
- Protected user sessions

### 🛍️ **Product Catalog**
- Browse products by category
- Search functionality
- Product details with images
- Stock quantity tracking
- Price management

### 🛒 **Shopping Cart**
- Add/remove items from cart
- Quantity management
- Real-time cart updates
- Cart persistence during session

### 📋 **Order Management**
- Place orders with multiple items
- Order history tracking
- Order status updates
- Inventory management

### 🎨 **Frontend Features**
- Responsive web interface
- Product catalog with search and filters
- Shopping cart functionality
- User account management
- Order tracking
- Modern UI with custom styling

## 🏗️ **Architecture**

### **Backend (FastAPI)**
- RESTful API with OpenAPI documentation
- PostgreSQL database with SQLAlchemy ORM
- JWT authentication system
- CORS enabled for frontend integration
- Production-ready configuration

### **Frontend (Streamlit)**
- Interactive web application
- Real-time API integration
- Shopping cart with session management
- User-friendly interface
- Responsive design

### **Database (NeonDB PostgreSQL)**
- Production PostgreSQL database
- Automated table creation
- Sample data for testing
- Relationship management

## 🚀 **Quick Start**

### **1. Run Frontend Locally**
```bash
# Windows
run_frontend.bat

# Or manually
streamlit run ecommerce_frontend.py
```

### **2. Access Application**
- **Frontend:** http://localhost:8501
- **Backend API:** https://production-deployment-to-render.onrender.com

### **3. Test the Application**
1. **Browse Products** - View 5 sample products
2. **Register Account** - Create a new user account  
3. **Add to Cart** - Add products to shopping cart
4. **Place Order** - Complete checkout process
5. **View Orders** - Track order history

## 📊 **API Endpoints**

### **Authentication**
- `POST /register` - User registration
- `POST /login` - User login
- `GET /users/me` - Get current user

### **Products**
- `GET /products` - List all products
- `GET /products/{id}` - Get specific product
- `POST /products` - Create product (authenticated)

### **Orders**
- `POST /orders` - Create new order
- `GET /orders` - Get user orders
- `GET /orders/{id}` - Get specific order

### **Monitoring**
- `GET /` - API status
- `GET /health` - Health check

## 🧪 **Testing**

### **Automated API Testing**
```bash
python test_api.py
```

### **Manual Testing**
1. **Frontend Testing:**
   - Product browsing and search
   - Cart functionality
   - User registration/login
   - Order placement

2. **API Testing:**
   - Use Swagger UI at `/docs`
   - Test all endpoints
   - Verify authentication

## 🔧 **Development Setup**

### **Local Development**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run backend
uvicorn main:app --reload

# 3. Run frontend (in another terminal)
streamlit run ecommerce_frontend.py
```

### **Environment Variables**
```bash
SECRET_KEY=4znmMa7AfIGyDkL1ur-PG3_J_vwS0DIdRlYJER7dvtE
DATABASE_URL=postgresql://neondb_owner:npg_vDR8zMLVfj4r@ep-wispy-dust-a1wv2of0-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

## 🌐 **Deployment**

### **Backend Deployment (Render)**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables:** SECRET_KEY, DATABASE_URL

### **Frontend Deployment Options**
1. **Streamlit Cloud** - Deploy frontend separately
2. **Local Hosting** - Run frontend locally, connect to deployed API
3. **Docker** - Containerize both frontend and backend

## 📱 **Frontend Features**

### **Home Page - Product Catalog**
- Grid layout of products
- Search by name/description
- Filter by category
- Add to cart functionality
- Stock status indicators

### **Shopping Cart**
- View cart items
- Modify quantities
- Remove items
- Calculate totals
- Checkout process

### **User Account**
- Registration form
- Login system
- User profile display
- Order history

### **Order Management**
- Place orders
- View order details
- Track order status
- Order history

## 🔒 **Security Features**

- JWT token authentication
- Secure password hashing
- Environment variable protection
- CORS configuration
- Input validation

## 📊 **Database Schema**

```sql
-- Users table
users (id, email, username, hashed_password, is_active, created_at)

-- Products table  
products (id, name, description, price, stock_quantity, category, created_at)

-- Orders table
orders (id, user_id, total_amount, status, created_at)

-- Order Items table
order_items (id, order_id, product_id, quantity, price)
```

## 🎯 **Sample Data**

The application includes 5 sample products:
- Laptop Pro ($1299.99)
- Wireless Headphones ($199.99)
- Coffee Maker ($89.99)
- Running Shoes ($129.99)
- Smartphone ($899.99)

## 📈 **Monitoring**

- Health check endpoint for uptime monitoring
- Structured logging for debugging
- Error handling with user-friendly messages
- API response time tracking

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 **License**

MIT License - Feel free to use for educational and commercial purposes.

---

## 🎉 **Success Metrics**

✅ **Backend Deployed** - API running on Render
✅ **Database Connected** - PostgreSQL with sample data  
✅ **Frontend Created** - Complete Streamlit application
✅ **Authentication Working** - User registration/login
✅ **E-commerce Features** - Cart, orders, products
✅ **Production Ready** - Environment configuration
✅ **Documentation** - Complete API docs and guides

**Your complete e-commerce application is ready for production use!** 🚀
