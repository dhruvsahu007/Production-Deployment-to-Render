"""
Complete E-commerce Frontend Application
A full-featured e-commerce web application using Streamlit
"""
import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time

# Configuration
API_BASE_URL = "https://production-deployment-to-render.onrender.com"

# Page configuration
st.set_page_config(
    page_title="🛒 E-Commerce Store",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .product-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .price-tag {
        font-size: 24px;
        font-weight: bold;
        color: #e74c3c;
    }
    .stock-info {
        color: #27ae60;
        font-weight: bold;
    }
    .out-of-stock {
        color: #e74c3c;
        font-weight: bold;
    }
    .cart-item {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #3498db;
    }
    .order-summary {
        background: #e8f6f3;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #1abc9c;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

def make_request(method, endpoint, data=None, headers=None):
    """Make API request with error handling"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        return response
    except Exception as e:
        st.error(f"API request failed: {e}")
        return None

def get_auth_headers():
    """Get authentication headers"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return None

def add_to_cart(product):
    """Add product to cart"""
    # Check if product already in cart
    for item in st.session_state.cart:
        if item['id'] == product['id']:
            if item['quantity'] < product['stock_quantity']:
                item['quantity'] += 1
                st.success(f"Added another {product['name']} to cart!")
            else:
                st.warning(f"Cannot add more {product['name']} - insufficient stock!")
            return
    
    # Add new item to cart
    st.session_state.cart.append({
        'id': product['id'],
        'name': product['name'],
        'price': product['price'],
        'quantity': 1,
        'max_stock': product['stock_quantity']
    })
    st.success(f"Added {product['name']} to cart!")

def remove_from_cart(product_id):
    """Remove product from cart"""
    st.session_state.cart = [item for item in st.session_state.cart if item['id'] != product_id]
    st.success("Item removed from cart!")

def get_cart_total():
    """Calculate cart total"""
    return sum(item['price'] * item['quantity'] for item in st.session_state.cart)

def get_cart_count():
    """Get total items in cart"""
    return sum(item['quantity'] for item in st.session_state.cart)

# Header
st.title("🛒 E-Commerce Store")
st.markdown("*Your one-stop shop for amazing products!*")

# Navigation
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

with col1:
    if st.session_state.user_info:
        st.write(f"👋 Welcome, **{st.session_state.user_info['username']}**!")
    else:
        st.write("👋 Welcome to our store!")

with col2:
    if st.button("🏠 Home"):
        st.session_state.current_page = "home"

with col3:
    cart_count = get_cart_count()
    if st.button(f"🛒 Cart ({cart_count})"):
        st.session_state.current_page = "cart"

with col4:
    if st.session_state.token:
        if st.button("📋 Orders"):
            st.session_state.current_page = "orders"
    else:
        if st.button("🔐 Login"):
            st.session_state.current_page = "auth"

with col5:
    if st.session_state.token:
        if st.button("🚪 Logout"):
            st.session_state.token = None
            st.session_state.user_info = None
            st.session_state.cart = []
            st.session_state.current_page = "home"
            st.rerun()

st.markdown("---")

# Page routing
if st.session_state.current_page == "home":
    # HOME PAGE - Product Catalog
    st.header("🛍️ Product Catalog")
    
    # Fetch products
    response = make_request("GET", "/products")
    if response and response.status_code == 200:
        products = response.json()
        
        if products:
            # Filter and search
            col1, col2 = st.columns([3, 1])
            with col1:
                search_term = st.text_input("🔍 Search products...", placeholder="Enter product name or category")
            with col2:
                categories = list(set([p['category'] for p in products]))
                selected_category = st.selectbox("📂 Category", ["All"] + categories)
            
            # Filter products
            filtered_products = products
            if search_term:
                filtered_products = [p for p in filtered_products if 
                                   search_term.lower() in p['name'].lower() or 
                                   search_term.lower() in p['description'].lower()]
            if selected_category != "All":
                filtered_products = [p for p in filtered_products if p['category'] == selected_category]
            
            # Display products in grid
            cols_per_row = 3
            for i in range(0, len(filtered_products), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(filtered_products):
                        product = filtered_products[i + j]
                        with col:
                            st.markdown(f"""
                            <div class="product-card">
                                <h3>{product['name']}</h3>
                                <p><strong>Category:</strong> {product['category']}</p>
                                <p>{product['description']}</p>
                                <div class="price-tag">${product['price']:.2f}</div>
                                <p class="{'stock-info' if product['stock_quantity'] > 0 else 'out-of-stock'}">
                                    {'✅ In Stock: ' + str(product['stock_quantity']) if product['stock_quantity'] > 0 else '❌ Out of Stock'}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if product['stock_quantity'] > 0:
                                if st.button(f"🛒 Add to Cart", key=f"add_{product['id']}"):
                                    add_to_cart(product)
                                    st.rerun()
                            else:
                                st.button("❌ Out of Stock", disabled=True, key=f"out_{product['id']}")
        else:
            st.info("🔍 No products found.")
    else:
        st.error("❌ Unable to load products. Please check the API connection.")

elif st.session_state.current_page == "cart":
    # CART PAGE
    st.header("🛒 Shopping Cart")
    
    if st.session_state.cart:
        # Display cart items
        for item in st.session_state.cart:
            st.markdown(f"""
            <div class="cart-item">
                <h4>{item['name']}</h4>
                <p>Price: ${item['price']:.2f} each</p>
                <p>Subtotal: ${item['price'] * item['quantity']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**Quantity:** {item['quantity']}")
            with col2:
                if st.button("➕", key=f"inc_{item['id']}"):
                    if item['quantity'] < item['max_stock']:
                        item['quantity'] += 1
                        st.rerun()
                    else:
                        st.warning("Maximum stock reached!")
            with col3:
                if st.button("➖", key=f"dec_{item['id']}"):
                    if item['quantity'] > 1:
                        item['quantity'] -= 1
                        st.rerun()
                    else:
                        remove_from_cart(item['id'])
                        st.rerun()
            with col4:
                if st.button("🗑️", key=f"remove_{item['id']}"):
                    remove_from_cart(item['id'])
                    st.rerun()
        
        # Cart summary
        total = get_cart_total()
        st.markdown(f"""
        <div class="order-summary">
            <h3>Order Summary</h3>
            <p><strong>Total Items:</strong> {get_cart_count()}</p>
            <p><strong>Total Amount:</strong> ${total:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Checkout
        if st.session_state.token:
            if st.button("💳 Checkout", type="primary"):
                # Prepare order data
                order_items = [
                    {"product_id": item['id'], "quantity": item['quantity']}
                    for item in st.session_state.cart
                ]
                
                # Create order
                response = make_request("POST", "/orders", 
                                      {"items": order_items}, 
                                      get_auth_headers())
                
                if response and response.status_code == 200:
                    st.success("🎉 Order placed successfully!")
                    st.session_state.cart = []
                    st.session_state.current_page = "orders"
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Failed to place order. Please try again.")
        else:
            st.warning("🔐 Please login to checkout")
            if st.button("Login to Checkout"):
                st.session_state.current_page = "auth"
                st.rerun()
    else:
        st.info("🛒 Your cart is empty. Start shopping to add items!")
        if st.button("🛍️ Continue Shopping"):
            st.session_state.current_page = "home"
            st.rerun()

elif st.session_state.current_page == "orders":
    # ORDERS PAGE
    st.header("📋 My Orders")
    
    if st.session_state.token:
        response = make_request("GET", "/orders", headers=get_auth_headers())
        if response and response.status_code == 200:
            orders = response.json()
            
            if orders:
                for order in orders:
                    with st.expander(f"🧾 Order #{order['id']} - ${order['total_amount']:.2f} ({order['status']})"):
                        st.write(f"**Date:** {order['created_at'][:19]}")
                        st.write(f"**Status:** {order['status']}")
                        st.write(f"**Total:** ${order['total_amount']:.2f}")
                        
                        st.write("**Items:**")
                        for item in order['items']:
                            st.write(f"- Product ID {item['product_id']}: {item['quantity']} × ${item['price']:.2f}")
            else:
                st.info("📦 No orders found. Place your first order!")
        else:
            st.error("❌ Unable to load orders.")
    else:
        st.warning("🔐 Please login to view orders")

elif st.session_state.current_page == "auth":
    # AUTHENTICATION PAGE
    st.header("🔐 User Authentication")
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("🔑 Login", type="primary")
            
            if login_btn and username and password:
                response = requests.post(f"{API_BASE_URL}/login", 
                                       data={"username": username, "password": password})
                
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]
                    
                    # Get user info
                    user_response = make_request("GET", "/users/me", headers=get_auth_headers())
                    if user_response and user_response.status_code == 200:
                        st.session_state.user_info = user_response.json()
                        st.success("✅ Login successful!")
                        st.session_state.current_page = "home"
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("❌ Invalid username or password")
    
    with tab2:
        st.subheader("Create New Account")
        with st.form("register_form"):
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            register_btn = st.form_submit_button("📝 Register", type="primary")
            
            if register_btn and email and username and password:
                response = make_request("POST", "/register", {
                    "email": email,
                    "username": username,
                    "password": password
                })
                
                if response and response.status_code == 200:
                    st.success("✅ Registration successful! Please login.")
                else:
                    st.error("❌ Registration failed. Username or email might already exist.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🛒 E-Commerce Store | Powered by FastAPI & Streamlit | Deployed on Render</p>
    <p>API Status: <a href="https://production-deployment-to-render.onrender.com/health" target="_blank">Health Check</a> | 
    <a href="https://production-deployment-to-render.onrender.com/docs" target="_blank">API Docs</a></p>
</div>
""", unsafe_allow_html=True)
