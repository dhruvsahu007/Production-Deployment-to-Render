"""
Test script for the E-commerce API
Run this to test all endpoints after deployment
"""
import requests
import json
import time

# Configuration
BASE_URL = "https://your-app-name.onrender.com"  # Replace with your Render URL
# For local testing, use: BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("\n👤 Testing user registration...")
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        if response.status_code == 200:
            print(f"✅ User registered successfully: {response.json()}")
            return True
        else:
            print(f"⚠️ Registration response: {response.status_code} - {response.text}")
            return response.status_code == 400  # User might already exist
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return False

def test_user_login():
    """Test user login and return token"""
    print("\n🔐 Testing user login...")
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login successful: {token_data}")
            return token_data["access_token"]
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return None

def test_get_user_info(token):
    """Test getting current user info"""
    print("\n👤 Testing get user info...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        if response.status_code == 200:
            print(f"✅ User info retrieved: {response.json()}")
            return True
        else:
            print(f"❌ Get user info failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get user info failed: {e}")
        return False

def test_create_product(token):
    """Test creating a product"""
    print("\n📦 Testing product creation...")
    product_data = {
        "name": "Test Laptop",
        "description": "A high-performance test laptop",
        "price": 999.99,
        "stock_quantity": 5,
        "category": "Electronics"
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/products", json=product_data, headers=headers)
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product created: {product}")
            return product["id"]
        else:
            print(f"❌ Product creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Product creation failed: {e}")
        return None

def test_get_products():
    """Test getting all products"""
    print("\n📦 Testing get all products...")
    try:
        response = requests.get(f"{BASE_URL}/products")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Products retrieved: {len(products)} products found")
            return products
        else:
            print(f"❌ Get products failed: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ Get products failed: {e}")
        return []

def test_get_product(product_id):
    """Test getting a specific product"""
    print(f"\n📦 Testing get product {product_id}...")
    try:
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product retrieved: {product}")
            return True
        else:
            print(f"❌ Get product failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get product failed: {e}")
        return False

def test_create_order(token, product_id):
    """Test creating an order"""
    print("\n🛒 Testing order creation...")
    order_data = {
        "items": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        if response.status_code == 200:
            order = response.json()
            print(f"✅ Order created: {order}")
            return order["id"]
        else:
            print(f"❌ Order creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Order creation failed: {e}")
        return None

def test_get_orders(token):
    """Test getting user orders"""
    print("\n🛒 Testing get user orders...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/orders", headers=headers)
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Orders retrieved: {len(orders)} orders found")
            return orders
        else:
            print(f"❌ Get orders failed: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ Get orders failed: {e}")
        return []

def test_get_order(token, order_id):
    """Test getting a specific order"""
    print(f"\n🛒 Testing get order {order_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=headers)
        if response.status_code == 200:
            order = response.json()
            print(f"✅ Order retrieved: {order}")
            return True
        else:
            print(f"❌ Get order failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get order failed: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("🚀 Starting E-commerce API Tests")
    print(f"📍 Testing URL: {BASE_URL}")
    print("=" * 50)
    
    # Test health check
    if not test_health_check():
        print("❌ Health check failed. Stopping tests.")
        return
    
    # Test user registration
    if not test_user_registration():
        print("❌ User registration failed. Stopping tests.")
        return
    
    # Test login
    token = test_user_login()
    if not token:
        print("❌ Login failed. Stopping tests.")
        return
    
    # Test get user info
    if not test_get_user_info(token):
        print("❌ Get user info failed.")
    
    # Test product creation
    product_id = test_create_product(token)
    if not product_id:
        print("❌ Product creation failed.")
        # Try to get existing products for order test
        products = test_get_products()
        if products:
            product_id = products[0]["id"]
    
    # Test get products
    products = test_get_products()
    
    # Test get specific product
    if product_id:
        test_get_product(product_id)
    
    # Test order creation
    if product_id:
        order_id = test_create_order(token, product_id)
        
        # Test get orders
        test_get_orders(token)
        
        # Test get specific order
        if order_id:
            test_get_order(token, order_id)
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("📊 Check the results above for any failures.")

if __name__ == "__main__":
    # Prompt user for URL
    url_input = input(f"Enter your Render URL (or press Enter for {BASE_URL}): ").strip()
    if url_input:
        BASE_URL = url_input.rstrip('/')
    
    run_all_tests()
