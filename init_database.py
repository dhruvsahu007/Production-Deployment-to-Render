"""
Database initialization script for NeonDB
This script will create all the necessary tables for the e-commerce API
"""
import os
from sqlalchemy import create_engine, text
from main import Base, User, Product, Order, OrderItem

# NeonDB connection string
DATABASE_URL = "postgresql://neondb_owner:npg_vDR8zMLVfj4r@ep-wispy-dust-a1wv2of0-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def create_database_tables():
    """Create all database tables"""
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
        
        # Create all tables
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = result.fetchall()
            
            print(f"\n📊 Created tables:")
            for table in tables:
                print(f"  - {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_sample_data():
    """Create some sample data for testing"""
    try:
        from sqlalchemy.orm import sessionmaker
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        db = SessionLocal()
        
        # Check if we already have data
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("📋 Sample data already exists, skipping creation.")
            db.close()
            return
        
        # Create sample products
        sample_products = [
            Product(
                name="Laptop Pro",
                description="High-performance laptop for professionals",
                price=1299.99,
                stock_quantity=10,
                category="Electronics"
            ),
            Product(
                name="Wireless Headphones",
                description="Premium noise-canceling wireless headphones",
                price=199.99,
                stock_quantity=25,
                category="Electronics"
            ),
            Product(
                name="Coffee Maker",
                description="Automatic drip coffee maker with timer",
                price=89.99,
                stock_quantity=15,
                category="Home & Kitchen"
            ),
            Product(
                name="Running Shoes",
                description="Comfortable athletic shoes for running",
                price=129.99,
                stock_quantity=30,
                category="Sports"
            ),
            Product(
                name="Smartphone",
                description="Latest generation smartphone with advanced features",
                price=899.99,
                stock_quantity=20,
                category="Electronics"
            )
        ]
        
        # Add products to database
        for product in sample_products:
            db.add(product)
        
        db.commit()
        print("✅ Sample products created successfully!")
        
        # Display created products
        products = db.query(Product).all()
        print(f"\n📦 Created {len(products)} sample products:")
        for product in products:
            print(f"  - {product.name}: ${product.price} (Stock: {product.stock_quantity})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Initializing NeonDB database for E-commerce API...")
    print("=" * 60)
    
    # Create tables
    if create_database_tables():
        print("\n🎯 Creating sample data...")
        create_sample_data()
        
        print("\n" + "=" * 60)
        print("✅ Database initialization complete!")
        print("📊 Your NeonDB is ready for the E-commerce API")
        print("🚀 You can now deploy to Render with confidence!")
    else:
        print("\n❌ Database initialization failed!")
        print("🔍 Please check your connection string and try again.")
