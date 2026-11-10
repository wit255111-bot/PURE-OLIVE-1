"""
PURE & OLIVE - Database Configuration & Schema
Clean, Minimalist E-Commerce Platform
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pure_olive.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Products Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_en TEXT NOT NULL,
            brand TEXT DEFAULT 'PURE & OLIVE',
            category TEXT NOT NULL,         -- 'skincare', 'cosmetics', 'tools'
            subcategory TEXT NOT NULL,      -- 'cleanser', 'toner', 'serum', 'cream', 'sunscreen', 'lip', 'cushion', 'blush', 'powder', 'tool'
            price REAL NOT NULL,
            original_price REAL,
            image_url TEXT NOT NULL,
            rating REAL DEFAULT 5.0,
            reviews_count INTEGER DEFAULT 0,
            stock INTEGER DEFAULT 20,
            skin_types TEXT,                -- 'all,oily,dry,combination,sensitive'
            skin_concerns TEXT,             -- 'acne,hydration,brightening,aging,barrier,soothing'
            routine_step TEXT,              -- 'cleanser', 'toner', 'serum', 'moisturizer', 'sunscreen', 'makeup', 'tool'
            routine_time TEXT,              -- 'both', 'morning', 'night'
            key_ingredients TEXT,
            volume TEXT,
            description TEXT,
            how_to_use TEXT,
            is_bestseller INTEGER DEFAULT 0,
            is_featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_email TEXT,
            customer_address TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            items_json TEXT NOT NULL,
            subtotal REAL NOT NULL,
            discount REAL DEFAULT 0,
            coupon_code TEXT,
            shipping_fee REAL DEFAULT 0,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'paid',    -- 'pending', 'paid', 'shipping', 'completed'
            tracking_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Reviews Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            reviewer_name TEXT NOT NULL,
            skin_type TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully at:", DB_PATH)
