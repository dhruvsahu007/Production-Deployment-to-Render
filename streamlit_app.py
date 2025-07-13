"""
Simple Streamlit frontend for the E-commerce API
"""
import streamlit as st
import requests
import json

# Configuration
API_BASE_URL = st.sidebar.text_input("API Base URL", "http://localhost:8000")

st.title("🛒 E-commerce API Dashboard")
st.markdown("A simple frontend to interact with the E-commerce API")

# Session state for token
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def make_request(method, endpoint, data=None, headers=None):
    """Make API request"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        return response
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

# Sidebar for authentication
st.sidebar.header("🔐 Authentication")

if st.session_state.token is None:
    # Login/Register tabs
    auth_tab = st.sidebar.radio("Choose action:", ["Login", "Register"])
    
    if auth_tab == "Register":
        st.sidebar.subheader("Register")
        email = st.sidebar.text_input("Email")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Register"):
            if email and username and password:
                response = make_request("POST", "/register", {
                    "email": email,
                    "username": username,
                    "password": password
                })
                if response and response.status_code == 200:
                    st.sidebar.success("Registration successful! Please login.")
                else:
                    st.sidebar.error(f"Registration failed: {response.text if response else 'Unknown error'}")
    
    else:  # Login
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            if username and password:
                response = requests.post(f"{API_BASE_URL}/login", data={
                    "username": username,
                    "password": password
                })
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]
                    st.sidebar.success("Login successful!")
                    st.rerun()
                else:
                    st.sidebar.error(f"Login failed: {response.text}")

else:
    # User is logged in
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Get user info
    if st.session_state.user_info is None:
        response = make_request("GET", "/users/me", headers=headers)
        if response and response.status_code == 200:
            st.session_state.user_info = response.json()
    
    if st.session_state.user_info:
        st.sidebar.success(f"Welcome, {st.session_state.user_info['username']}!")
    
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user_info = None
        st.rerun()

# Main content
if st.session_state.token:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📦 Products", "🛒 Orders", "📊 Dashboard"])
    
    with tab1:
        st.header("Products")
        
        # Create product
        with st.expander("➕ Create New Product"):
            col1, col2 = st.columns(2)
            with col1:
                product_name = st.text_input("Product Name")
                product_price = st.number_input("Price", min_value=0.01, step=0.01)
                product_stock = st.number_input("Stock Quantity", min_value=0, step=1)
            with col2:
                product_description = st.text_area("Description")
                product_category = st.text_input("Category")
            
            if st.button("Create Product"):
                if all([product_name, product_description, product_price, product_category]):
                    response = make_request("POST", "/products", {
                        "name": product_name,
                        "description": product_description,
                        "price": float(product_price),
                        "stock_quantity": int(product_stock),
                        "category": product_category
                    }, headers=headers)
                    
                    if response and response.status_code == 200:
                        st.success("Product created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to create product: {response.text if response else 'Unknown error'}")
        
        # Display products
        st.subheader("All Products")
        response = make_request("GET", "/products")
        if response and response.status_code == 200:
            products = response.json()
            
            if products:
                for product in products:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**{product['name']}**")
                            st.write(f"*{product['description']}*")
                            st.write(f"Category: {product['category']}")
                        with col2:
                            st.write(f"**${product['price']}**")
                            st.write(f"Stock: {product['stock_quantity']}")
                        with col3:
                            if st.button(f"View Details", key=f"view_{product['id']}"):
                                st.session_state.selected_product = product['id']
                        st.divider()
            else:
                st.info("No products found. Create some products to get started!")
    
    with tab2:
        st.header("Orders")
        
        # Create order
        with st.expander("🛒 Create New Order"):
            # Get products for selection
            response = make_request("GET", "/products")
            if response and response.status_code == 200:
                products = response.json()
                
                if products:
                    st.write("Select products to order:")
                    order_items = []
                    
                    for product in products:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**{product['name']}** - ${product['price']}")
                            st.write(f"Available: {product['stock_quantity']}")
                        with col2:
                            quantity = st.number_input(
                                f"Quantity", 
                                min_value=0, 
                                max_value=product['stock_quantity'],
                                key=f"qty_{product['id']}"
                            )
                        with col3:
                            if quantity > 0:
                                order_items.append({
                                    "product_id": product['id'],
                                    "quantity": quantity
                                })
                                st.success(f"Added {quantity}")
                    
                    if order_items and st.button("Place Order"):
                        response = make_request("POST", "/orders", {
                            "items": order_items
                        }, headers=headers)
                        
                        if response and response.status_code == 200:
                            st.success("Order placed successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed to place order: {response.text if response else 'Unknown error'}")
                else:
                    st.info("No products available for ordering.")
        
        # Display orders
        st.subheader("Your Orders")
        response = make_request("GET", "/orders", headers=headers)
        if response and response.status_code == 200:
            orders = response.json()
            
            if orders:
                for order in orders:
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**Order #{order['id']}**")
                            st.write(f"Items: {len(order['items'])}")
                        with col2:
                            st.write(f"**${order['total_amount']}**")
                            st.write(f"Status: {order['status']}")
                        with col3:
                            st.write(f"Date: {order['created_at'][:10]}")
                        
                        # Show order items
                        with st.expander(f"View Order #{order['id']} Details"):
                            for item in order['items']:
                                st.write(f"- Product ID {item['product_id']}: {item['quantity']} × ${item['price']}")
                        st.divider()
            else:
                st.info("No orders found. Place your first order!")
    
    with tab3:
        st.header("Dashboard")
        
        # API Health Check
        st.subheader("🔍 System Status")
        response = make_request("GET", "/health")
        if response and response.status_code == 200:
            health_data = response.json()
            col1, col2 = st.columns(2)
            with col1:
                st.success("✅ API Status: Healthy")
            with col2:
                st.info(f"Last Check: {health_data.get('timestamp', 'Unknown')}")
        else:
            st.error("❌ API Status: Unhealthy")
        
        # User Statistics
        st.subheader("📊 Your Statistics")
        if st.session_state.user_info:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("User ID", st.session_state.user_info['id'])
                st.metric("Account Status", "Active" if st.session_state.user_info['is_active'] else "Inactive")
            with col2:
                st.metric("Email", st.session_state.user_info['email'])
                st.metric("Member Since", st.session_state.user_info['created_at'][:10])
        
        # Quick Stats
        response = make_request("GET", "/orders", headers=headers)
        if response and response.status_code == 200:
            orders = response.json()
            total_orders = len(orders)
            total_spent = sum(order['total_amount'] for order in orders)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Orders", total_orders)
            with col2:
                st.metric("Total Spent", f"${total_spent:.2f}")

else:
    # Not logged in
    st.info("👈 Please login or register using the sidebar to access the dashboard.")
    
    # Show API health
    st.subheader("🔍 API Health Check")
    response = make_request("GET", "/health")
    if response and response.status_code == 200:
        health_data = response.json()
        st.success("✅ API is healthy and running!")
        st.json(health_data)
    else:
        st.error("❌ API is not responding. Please check the URL.")

# Footer
st.markdown("---")
st.markdown("🚀 E-commerce API Dashboard | Built with Streamlit")
