# E-commerce API - Production Deployment to Render

A production-ready e-commerce FastAPI application deployed on Render with proper security, database integration, and monitoring.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Product Management**: CRUD operations for products
- **Order System**: Complete order management with inventory tracking
- **Security**: Input validation, authentication, and authorization
- **Database**: SQLAlchemy ORM with PostgreSQL support
- **Monitoring**: Health check endpoints and logging
- **CORS**: Cross-origin resource sharing enabled
- **Production Ready**: Configured for Render deployment

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login and get access token
- `GET /users/me` - Get current user information

### Products
- `GET /products` - Get all products (paginated)
- `GET /products/{id}` - Get specific product
- `POST /products` - Create new product (authenticated)

### Orders
- `POST /orders` - Create new order (authenticated)
- `GET /orders` - Get user's orders (authenticated)
- `GET /orders/{id}` - Get specific order (authenticated)

### Monitoring
- `GET /` - API status
- `GET /health` - Health check

## Deployment to Render

### 1. GitHub Repository Setup

1. Initialize git repository:
```bash
git init
git add .
git commit -m "Initial commit: E-commerce API for Render deployment"
```

2. Create GitHub repository and push:
```bash
git remote add origin https://github.com/yourusername/ecommerce-api.git
git branch -M main
git push -u origin main
```

### 2. Render Service Configuration

1. **Create New Web Service**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Service Settings**:
   - **Name**: `ecommerce-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables

Set these environment variables in Render:

```
SECRET_KEY=your-super-secret-key-here-min-32-chars
DATABASE_URL=postgresql://username:password@hostname:port/database
```

### 4. Database Setup

**Option A: Render PostgreSQL (Recommended)**
1. Create PostgreSQL database in Render
2. Copy the Internal Database URL
3. Set as `DATABASE_URL` environment variable

**Option B: External PostgreSQL**
1. Use services like ElephantSQL, Supabase, or AWS RDS
2. Get connection string
3. Set as `DATABASE_URL` environment variable

### 5. Production Considerations

#### Security
- Strong SECRET_KEY (32+ characters)
- Environment variables for secrets
- HTTPS enabled by default on Render
- Input validation with Pydantic
- JWT token expiration

#### Monitoring
- Health check endpoint at `/health`
- Structured logging
- Error handling and validation

#### Performance
- SQLAlchemy connection pooling
- Pagination for product listings
- Efficient database queries

## Local Development

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set Environment Variables**:
```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///./ecommerce.db"
```

3. **Run Application**:
```bash
uvicorn main:app --reload
```

4. **Access API Documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Usage Examples

### Register User
```bash
curl -X POST "https://your-app.onrender.com/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "securepassword"
  }'
```

### Login
```bash
curl -X POST "https://your-app.onrender.com/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepassword"
```

### Create Product
```bash
curl -X POST "https://your-app.onrender.com/products" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock_quantity": 10,
    "category": "Electronics"
  }'
```

### Create Order
```bash
curl -X POST "https://your-app.onrender.com/orders" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'
```

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render web service created
- [ ] Build and start commands configured
- [ ] Environment variables set
- [ ] Database configured
- [ ] Service deployed successfully
- [ ] Health check endpoint working
- [ ] API endpoints tested

## Monitoring and Maintenance

### Health Monitoring
- Use `/health` endpoint for uptime monitoring
- Monitor response times and error rates
- Set up alerts for service failures

### Logs
- Access logs through Render dashboard
- Monitor for errors and performance issues
- Set up log aggregation if needed

### Scaling
- Render auto-scales based on traffic
- Monitor resource usage
- Consider database scaling for high traffic

## Support

For issues and questions:
1. Check Render service logs
2. Verify environment variables
3. Test endpoints locally
4. Check database connectivity

## License

MIT License - See LICENSE file for details.
