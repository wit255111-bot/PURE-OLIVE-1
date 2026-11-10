"""
PURE & OLIVE - Web Application Server
Flask + SQLite Clean Beauty E-Commerce
"""
import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = 'pure-and-olive-clean-beauty-secret-key-2026'

# Ensure DB initialized
init_db()

@app.context_processor
def inject_global_data():
    """Make shop info available to all templates"""
    return {
        'shop_name': 'PURE & OLIVE',
        'shop_tagline': 'Minimal & Clean Beauty',
        'shop_phone': '02-888-PURE (7873)',
        'shop_line': '@pureandolive',
        'free_shipping_threshold': 990.0,
        'standard_shipping_fee': 50.0
    }

# ----------------- ROUTES ----------------- #

@app.route('/')
def index():
    """Home page with banners, bestseller products, quiz teaser, and philosophy"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Bestsellers
    cursor.execute("SELECT * FROM products WHERE is_bestseller = 1 LIMIT 8")
    bestsellers = [dict(row) for row in cursor.fetchall()]

    # Featured Products
    cursor.execute("SELECT * FROM products WHERE is_featured = 1 LIMIT 8")
    featured = [dict(row) for row in cursor.fetchall()]

    # Latest Reviews with product info
    cursor.execute('''
        SELECT r.*, p.name AS product_name, p.image_url AS product_image
        FROM reviews r
        JOIN products p ON r.product_id = p.id
        ORDER BY r.created_at DESC LIMIT 4
    ''')
    reviews = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return render_template('index.html', bestsellers=bestsellers, featured=featured, reviews=reviews)


@app.route('/products')
def products():
    """Catalog with filtering by category, skin concern, search, and sorting"""
    conn = get_db_connection()
    cursor = conn.cursor()

    category = request.args.get('category', '').strip()
    concern = request.args.get('concern', '').strip()
    skin_type = request.args.get('skin_type', '').strip()
    search = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'popular')

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if concern:
        query += " AND skin_concerns LIKE ?"
        params.append(f'%{concern}%')

    if skin_type:
        query += " AND (skin_types LIKE ? OR skin_types LIKE '%all%')"
        params.append(f'%{skin_type}%')

    if search:
        query += " AND (name LIKE ? OR name_en LIKE ? OR key_ingredients LIKE ? OR description LIKE ?)"
        term = f'%{search}%'
        params.extend([term, term, term, term])

    # Sorting
    if sort == 'price_low':
        query += " ORDER BY price ASC"
    elif sort == 'price_high':
        query += " ORDER BY price DESC"
    elif sort == 'rating':
        query += " ORDER BY rating DESC"
    elif sort == 'newest':
        query += " ORDER BY id DESC"
    else:  # popular / bestseller
        query += " ORDER BY is_bestseller DESC, rating DESC"

    cursor.execute(query, params)
    product_list = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return render_template(
        'products.html',
        products=product_list,
        current_category=category,
        current_concern=concern,
        current_skin_type=skin_type,
        current_sort=sort,
        search_query=search,
        total_count=len(product_list)
    )


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Detailed view for a single product with reviews and related items"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if not product:
        conn.close()
        flash('ไม่พบสินค้าที่ต้องการ', 'danger')
        return redirect(url_for('products'))

    product = dict(product)

    # Product Reviews
    cursor.execute("SELECT * FROM reviews WHERE product_id = ? ORDER BY created_at DESC", (product_id,))
    reviews = [dict(r) for r in cursor.fetchall()]

    # Related Products in the same category
    cursor.execute(
        "SELECT * FROM products WHERE category = ? AND id != ? LIMIT 4",
        (product['category'], product_id)
    )
    related = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('product_detail.html', product=product, reviews=reviews, related=related)


@app.route('/api/review', methods=['POST'])
def add_review():
    """Submit a customer review for a product"""
    data = request.form
    product_id = data.get('product_id')
    reviewer_name = data.get('reviewer_name', 'ลูกค้าผู้รักผิว')
    skin_type = data.get('skin_type', 'ผิวธรรมดา')
    rating = int(data.get('rating', 5))
    comment = data.get('comment', '').strip()

    if not comment or not product_id:
        flash('กรุณากรอกข้อความรีวิวให้ครบถ้วน', 'warning')
        return redirect(url_for('product_detail', product_id=product_id))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO reviews (product_id, reviewer_name, skin_type, rating, comment, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product_id, reviewer_name, skin_type, rating, comment, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    # Update product review count and average rating
    cursor.execute("SELECT AVG(rating), COUNT(id) FROM reviews WHERE product_id = ?", (product_id,))
    avg_r, cnt_r = cursor.fetchone()
    cursor.execute("UPDATE products SET rating = ?, reviews_count = ? WHERE id = ?",
                   (round(avg_r, 1), cnt_r, product_id))

    conn.commit()
    conn.close()

    flash('ขอบคุณสำหรับรีวิวของคุณค่ะ!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))


@app.route('/routine-quiz')
def routine_quiz():
    """Interactive Skin Quiz & Routine Builder page"""
    return render_template('routine_quiz.html')


@app.route('/api/quiz-recommend', methods=['POST'])
def quiz_recommend():
    """
    Intelligent Routine Matching Engine:
    Takes user skin type, primary concern, and preference style
    Returns morning routine, night routine, total package price, and discount
    """
    data = request.get_json() or {}
    skin_type = data.get('skin_type', 'combination')  # oily, dry, combination, sensitive
    concern = data.get('concern', 'barrier')          # acne, hydration, brightening, aging, barrier
    ritual_style = data.get('style', 'complete')      # minimal (3-step) or complete (with tool/gadget)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all products
    cursor.execute("SELECT * FROM products")
    all_products = [dict(row) for row in cursor.fetchall()]
    conn.close()

    # Rule-based matching
    # 1. Cleanser
    cleanser = next((p for p in all_products if p['subcategory'] == 'cleanser'), None)
    
    # 2. Toner
    toner = next((p for p in all_products if p['subcategory'] == 'toner'), None)

    # 3. Targeted Serum
    if concern == 'acne':
        serum = next((p for p in all_products if 'Niacinamide' in p['name_en']), None)
    elif concern == 'aging':
        serum = next((p for p in all_products if 'Bakuchiol' in p['name_en']), None)
    else:
        serum = next((p for p in all_products if 'Squalane' in p['name_en']), None)

    # 4. Moisturizer
    if skin_type in ['oily', 'combination'] and concern == 'acne':
        moisturizer = next((p for p in all_products if 'Cica' in p['name_en']), None)
    else:
        moisturizer = next((p for p in all_products if 'Recovery Cream' in p['name_en']), None)

    # 5. Sunscreen
    sunscreen = next((p for p in all_products if p['subcategory'] == 'sunscreen'), None)

    # 6. Night Treatment / Tool
    if ritual_style == 'complete':
        if concern == 'aging':
            special_item = next((p for p in all_products if 'Face Booster' in p['name_en']), None)
        else:
            special_item = next((p for p in all_products if 'Jade Gua Sha' in p['name_en']), None)
    else:
        special_item = next((p for p in all_products if 'Lip' in p['subcategory']), None)

    # Construct Morning Routine
    morning_items = [item for item in [cleanser, toner, serum, moisturizer, sunscreen] if item]
    
    # Construct Night Routine
    night_items = [item for item in [cleanser, toner, serum, moisturizer, special_item] if item]

    # Combined Unique Bundle Items
    unique_items_map = {}
    for item in (morning_items + night_items):
        unique_items_map[item['id']] = item
    bundle_items = list(unique_items_map.values())

    subtotal = sum(p['price'] for p in bundle_items)
    discount = round(subtotal * 0.15, 2)  # 15% discount for full routine bundle
    bundle_price = subtotal - discount

    # Explanations tailored to skin type & concern
    concern_names = {
        'acne': 'ปัญหาสิวและการควบคุมความมัน',
        'hydration': 'ผิวแห้งขาดน้ำและลอกเป็นขุย',
        'brightening': 'ผิวหมองคล้ำและรอยดำสะสม',
        'aging': 'ริ้วรอยและความหย่อนคล้อย',
        'barrier': 'ผิวบอบบางและเกราะป้องกันผิวอ่อนแอ'
    }
    
    skin_type_names = {
        'oily': 'ผิวมัน (Oily Skin)',
        'dry': 'ผิวแห้ง (Dry Skin)',
        'combination': 'ผิวผสม (Combination Skin)',
        'sensitive': 'ผิวบอบบางแพ้ง่าย (Sensitive Skin)'
    }

    advice = f"สำหรับคุณที่มี {skin_type_names.get(skin_type, skin_type)} และกังวลเรื่อง {concern_names.get(concern, concern)} ทาง PURE & OLIVE แนะนำให้เน้นการปลอบประโลมผิว เสริมเกราะป้องกันชั้นผิวด้วยสารสกัดธรรมชาติ และหลีกเลี่ยงสารอุดตัน โดยรูทีนนี้ได้รับการคัดสรรให้มีความสมดุลทั้งกลางวันและกลางคืน"

    return jsonify({
        'status': 'success',
        'advice': advice,
        'skin_type_label': skin_type_names.get(skin_type, skin_type),
        'concern_label': concern_names.get(concern, concern),
        'morning_routine': morning_items,
        'night_routine': night_items,
        'bundle_items': bundle_items,
        'subtotal': subtotal,
        'discount': discount,
        'bundle_price': bundle_price
    })


@app.route('/cart')
def cart():
    """Cart overview and checkout form"""
    return render_template('cart.html')


@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Process order placement, record in SQLite, and return order confirmation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'ไม่พบข้อมูลคำสั่งซื้อ'}), 400

        name = data.get('customer_name', '').strip()
        phone = data.get('customer_phone', '').strip()
        email = data.get('customer_email', '').strip()
        address = data.get('customer_address', '').strip()
        payment_method = data.get('payment_method', 'promptpay')
        items = data.get('items', [])
        coupon = data.get('coupon_code', '').strip().upper()

        if not name or not phone or not address or not items:
            return jsonify({'status': 'error', 'message': 'กรุณากรอกข้อมูลและที่อยู่จัดส่งให้ครบถ้วน'}), 400

        subtotal = sum(float(item['price']) * int(item['quantity']) for item in items)
        
        # Coupon Logic
        discount = 0.0
        if coupon == 'PURE10':
            discount = round(subtotal * 0.10, 2)
        elif coupon == 'OLIVE50':
            discount = 50.0 if subtotal >= 300 else 0.0
        elif coupon == 'ROUTINE15':
            discount = round(subtotal * 0.15, 2)

        # Shipping Fee Logic
        shipping_fee = 0.0 if (subtotal - discount) >= 990.0 else 50.0
        total_price = max(0.0, (subtotal - discount) + shipping_fee)

        # Order Number: PO-YYYYMMDD-XXXX
        order_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update Stock
        for item in items:
            cursor.execute("UPDATE products SET stock = MAX(0, stock - ?) WHERE id = ?",
                           (int(item['quantity']), int(item['id'])))

        # Insert Order
        cursor.execute('''
            INSERT INTO orders (
                order_number, customer_name, customer_phone, customer_email,
                customer_address, payment_method, items_json, subtotal,
                discount, coupon_code, shipping_fee, total_price, status,
                tracking_number, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_number, name, phone, email, address, payment_method,
            json.dumps(items, ensure_ascii=False), subtotal, discount,
            coupon, shipping_fee, total_price, 'paid',
            f"TH-PO{random.randint(1000000, 9999999)}",
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))

        conn.commit()
        conn.close()

        return jsonify({
            'status': 'success',
            'order_number': order_number,
            'total_price': total_price,
            'redirect_url': url_for('order_success', order_number=order_number)
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/order-success/<order_number>')
def order_success(order_number):
    """Order confirmation and simulated PromptPay QR / details"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
    order = cursor.fetchone()
    conn.close()

    if not order:
        flash('ไม่พบข้อมูลคำสั่งซื้อ', 'warning')
        return redirect(url_for('index'))

    order = dict(order)
    try:
        order['order_items'] = json.loads(order['items_json'])
    except:
        order['order_items'] = []

    return render_template('order_success.html', order=order)


@app.route('/tips')
def tips():
    """Clean Beauty Philosophy, Ingredients Guide, and Skincare Tips"""
    return render_template('tips.html')


# ----------------- ADMIN DASHBOARD ----------------- #

@app.route('/admin')
def admin():
    """Admin Dashboard for stock management and orders overview"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Stats
    cursor.execute("SELECT COUNT(id), COALESCE(SUM(total_price), 0) FROM orders")
    total_orders, total_sales = cursor.fetchone()

    cursor.execute("SELECT COUNT(id) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(id) FROM products WHERE stock <= 15")
    low_stock_count = cursor.fetchone()[0]

    # Orders List
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT 20")
    orders = []
    for row in cursor.fetchall():
        ord_dict = dict(row)
        try:
            ord_dict['items'] = json.loads(ord_dict['items_json'])
        except:
            ord_dict['items'] = []
        orders.append(ord_dict)

    # Products List
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return render_template(
        'admin.html',
        total_sales=total_sales,
        total_orders=total_orders,
        total_products=total_products,
        low_stock_count=low_stock_count,
        orders=orders,
        products=products
    )


@app.route('/admin/product/add', methods=['POST'])
def admin_add_product():
    """Add a new product via admin panel"""
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO products (
            name, name_en, brand, category, subcategory, price, original_price,
            image_url, stock, skin_types, skin_concerns, routine_step, routine_time,
            key_ingredients, volume, description, how_to_use, is_bestseller, is_featured
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'), data.get('name_en'), 'PURE & OLIVE',
        data.get('category'), data.get('subcategory', 'general'),
        float(data.get('price', 0)), float(data.get('original_price', 0) or 0),
        data.get('image_url') or 'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=800&q=80',
        int(data.get('stock', 20)), data.get('skin_types', 'all'),
        data.get('skin_concerns', 'all'), data.get('routine_step', 'serum'),
        data.get('routine_time', 'both'), data.get('key_ingredients', ''),
        data.get('volume', '50 ml'), data.get('description', ''),
        data.get('how_to_use', ''), 1 if 'is_bestseller' in data else 0,
        1 if 'is_featured' in data else 0
    ))

    conn.commit()
    conn.close()
    flash('เพิ่มสินค้าใหม่เรียบร้อยแล้วค่ะ', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
def admin_delete_product(product_id):
    """Delete product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    cursor.execute("DELETE FROM reviews WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()
    flash('ลบสินค้าเรียบร้อยแล้วค่ะ', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/order/status/<int:order_id>', methods=['POST'])
def admin_update_order_status(order_id):
    """Update order delivery status"""
    status = request.form.get('status', 'paid')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()
    flash('อัปเดตสถานะคำสั่งซื้อเรียบร้อยแล้ว', 'success')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    print("[SERVER] PURE & OLIVE Server starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
