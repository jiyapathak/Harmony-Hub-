from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Database initialization
def init_db():
    conn = sqlite3.connect('music_store.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Products table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        specifications TEXT,
        image_url TEXT,
        rating REAL DEFAULT 5.0,
        stock INTEGER DEFAULT 10,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        total_amount REAL,
        status TEXT DEFAULT 'pending',
        payment_method TEXT,
        delivery_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Order items table
    c.execute('''CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )''')
    
    # Sales tracking table
    c.execute('''CREATE TABLE IF NOT EXISTS sales_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity_sold INTEGER DEFAULT 0,
        total_revenue REAL DEFAULT 0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id),
        UNIQUE(product_id)
    )''')
    
    # Add missing columns to orders table if they don't exist
    try:
        c.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in c.fetchall()]
        
        if 'payment_method' not in columns:
            c.execute('ALTER TABLE orders ADD COLUMN payment_method TEXT DEFAULT "cash_on_delivery"')
        
        if 'delivery_address' not in columns:
            c.execute('ALTER TABLE orders ADD COLUMN delivery_address TEXT DEFAULT ""')
    except Exception as e:
        print(f"Column migration note: {e}")
    
    # Create admin user
    admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)',
                  ('admin', 'admin@musicstore.com', admin_password, 1))
    except sqlite3.IntegrityError:
        pass
    
    # Sample products
    sample_products = [
        ('Fender Stratocaster Electric Guitar', 'Guitars', 'Fender', 1299.99, 
         'Iconic electric guitar with versatile tone', 'Alder body, Maple neck, 3 single-coil pickups', 
         'https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?w=500', 4.8, 15),
        ('Yamaha P-125 Digital Piano', 'Pianos & Keyboards', 'Yamaha', 649.99,
         'Portable digital piano with authentic piano touch', '88 weighted keys, 24 voices, USB connectivity',
         'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=500', 4.7, 8),
        ('Pearl Export Drum Kit', 'Drums', 'Pearl', 899.99,
         'Complete 5-piece drum set for beginners and pros', '5 drums, hardware included, birch shells',
         'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=500', 4.6, 5),
        ('Stentor Violin Student II', 'Violins', 'Stentor', 299.99,
         'Quality student violin with bow and case', 'Solid carved top, ebony fittings, includes case',
         'https://images.unsplash.com/photo-1612225330812-0e9e10f03a83?w=500', 4.5, 12),
        ('Yamaha YFL-222 Flute', 'Flutes', 'Yamaha', 549.99,
         'Professional student flute with excellent tone', 'Nickel silver, offset G, E mechanism',
         'https://images.unsplash.com/photo-1598030886674-c92be74e237b?w=500', 4.9, 7),
        ('Pioneer DJ DDJ-400', 'DJ Equipment', 'Pioneer', 249.99,
         '2-channel DJ controller for beginners', 'Rekordbox compatible, built-in sound card',
         'https://images.unsplash.com/photo-1598653222000-6b7b7a552625?w=500', 4.7, 10),
        ('Shure SM58 Microphone', 'Accessories', 'Shure', 99.99,
         'Legendary vocal microphone', 'Dynamic, cardioid, rugged construction',
         'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=500', 5.0, 25),
        ('Boss Katana-50 Amplifier', 'Accessories', 'Boss', 229.99,
         '50-watt guitar amplifier with effects', '5 amp characters, built-in effects, USB',
         'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=500', 4.8, 6),
        ('Gibson Les Paul Standard', 'Guitars', 'Gibson', 2499.99,
         'Legendary electric guitar with premium tone', 'Mahogany body, AAA maple top, humbuckers',
         'https://images.unsplash.com/photo-1516924962500-2b4b3b99ea02?w=500', 4.9, 3),
        ('Roland TD-17KVX V-Drums', 'Drums', 'Roland', 1699.99,
         'Electronic drum kit with mesh heads', 'Premium sound module, bluetooth audio',
         'https://images.unsplash.com/photo-1571327073757-71d13c24de30?w=500', 4.8, 4),
        ('Korg SV-2 Stage Piano', 'Pianos & Keyboards', 'Korg', 1999.99,
         '88-key stage piano with vintage sounds', 'Weighted hammer action, tube-driven preamp',
         'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500', 4.7, 5),
        ('D\'Addario Guitar Strings Pack', 'Accessories', 'D\'Addario', 19.99,
         '3-pack of premium guitar strings', 'Nickel wound, 10-46 gauge, long life',
         'https://images.unsplash.com/photo-1556449895-a33c9dba33dd?w=500', 4.6, 50)
    ]
    
    for product in sample_products:
        try:
            c.execute('''INSERT INTO products 
                (name, category, brand, price, description, specifications, image_url, rating, stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', product)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Helper function to get db connection
def get_db():
    conn = sqlite3.connect('music_store.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    return render_template('product.html', product_id=product_id)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('checkout.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

# API Routes
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db()
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search', '')
    
    query = 'SELECT * FROM products WHERE 1=1'
    params = []
    
    if category and category != 'all':
        query += ' AND category = ?'
        params.append(category)
    
    if min_price:
        query += ' AND price >= ?'
        params.append(min_price)
    
    if max_price:
        query += ' AND price <= ?'
        params.append(max_price)
    
    if search:
        query += ' AND (name LIKE ? OR brand LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    products = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(p) for p in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    
    if product:
        return jsonify(dict(product))
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'All fields required'}), 400
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = get_db()
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Registration successful'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 400

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({'error': 'All fields required'}), 400
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                       (username, hashed_password)).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = user['is_admin']
        return jsonify({
            'message': 'Login successful',
            'user': {'username': user['username'], 'is_admin': user['is_admin']}
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'})

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'username': session['username'],
            'is_admin': session.get('is_admin', False)
        })
    return jsonify({'logged_in': False})

# Order Management Routes
@app.route('/api/orders', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    user_id = session['user_id']
    
    items = data.get('items', [])
    payment_method = data.get('payment_method', 'cash_on_delivery')
    delivery_address = data.get('delivery_address', '')
    
    if not items:
        return jsonify({'error': 'No items in order'}), 400
    
    try:
        conn = get_db()
        
        # Calculate total
        total_amount = sum(item['price'] * item['quantity'] for item in items)
        
        # Create order
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO orders (user_id, total_amount, payment_method, delivery_address, status)
                         VALUES (?, ?, ?, ?, ?)''',
                       (user_id, total_amount, payment_method, delivery_address, 'pending'))
        order_id = cursor.lastrowid
        
        # Add order items and update inventory
        for item in items:
            product_id = item['id']
            quantity = item['quantity']
            price = item['price']
            
            # Add to order items
            cursor.execute('''INSERT INTO order_items (order_id, product_id, quantity, price)
                             VALUES (?, ?, ?, ?)''',
                           (order_id, product_id, quantity, price))
            
            # Update product stock
            cursor.execute('UPDATE products SET stock = stock - ? WHERE id = ?',
                          (quantity, product_id))
            
            # Update sales tracking
            cursor.execute('''INSERT INTO sales_tracking (product_id, quantity_sold, total_revenue)
                             VALUES (?, ?, ?)
                             ON CONFLICT(product_id) DO UPDATE SET
                             quantity_sold = quantity_sold + ?,
                             total_revenue = total_revenue + ?,
                             last_updated = CURRENT_TIMESTAMP''',
                          (product_id, quantity, price * quantity, quantity, price * quantity))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order_id,
            'status': 'pending'
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db()
    order = conn.execute('SELECT * FROM orders WHERE id = ? AND user_id = ?',
                        (order_id, session['user_id'])).fetchone()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    items = conn.execute('''SELECT oi.*, p.name, p.image_url FROM order_items oi
                            JOIN products p ON oi.product_id = p.id
                            WHERE oi.order_id = ?''', (order_id,)).fetchall()
    conn.close()
    
    return jsonify({
        'order': dict(order),
        'items': [dict(item) for item in items]
    })

@app.route('/api/user/orders', methods=['GET'])
def get_user_orders():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db()
    orders = conn.execute('''SELECT * FROM orders WHERE user_id = ? 
                             ORDER BY created_at DESC''',
                         (session['user_id'],)).fetchall()
    conn.close()
    
    return jsonify([dict(order) for order in orders])

@app.route('/api/user/orders/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db()
    
    # Verify order belongs to user
    order = conn.execute('SELECT * FROM orders WHERE id = ? AND user_id = ?',
                        (order_id, session['user_id'])).fetchone()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    items = conn.execute('''SELECT oi.*, p.name, p.image_url, p.brand FROM order_items oi
                            JOIN products p ON oi.product_id = p.id
                            WHERE oi.order_id = ?''', (order_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(item) for item in items])

@app.route('/api/admin/sales-data', methods=['GET'])
def get_sales_data():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db()
    sales = conn.execute('''SELECT st.*, p.name, p.category FROM sales_tracking st
                            JOIN products p ON st.product_id = p.id
                            ORDER BY st.quantity_sold DESC''').fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in sales])

@app.route('/api/admin/inventory', methods=['GET'])
def get_inventory():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db()
    products = conn.execute('''SELECT p.id, p.name, p.category, p.stock, p.price,
                              COALESCE(st.quantity_sold, 0) as sold,
                              COALESCE(st.total_revenue, 0) as revenue
                              FROM products p
                              LEFT JOIN sales_tracking st ON p.id = st.product_id
                              ORDER BY p.name''').fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in products])

# Admin API Routes
@app.route('/api/admin/products', methods=['POST'])
def add_product():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    required = ['name', 'category', 'brand', 'price', 'description', 'image_url']
    
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    conn.execute('''INSERT INTO products 
        (name, category, brand, price, description, specifications, image_url, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['name'], data['category'], data['brand'], data['price'],
         data['description'], data.get('specifications', ''),
         data['image_url'], data.get('stock', 10)))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/api/admin/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    conn = get_db()
    conn.execute('''UPDATE products SET 
        name=?, category=?, brand=?, price=?, description=?, 
        specifications=?, image_url=?, stock=?
        WHERE id=?''',
        (data['name'], data['category'], data['brand'], data['price'],
         data['description'], data.get('specifications', ''),
         data['image_url'], data.get('stock', 10), product_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Product updated successfully'})

@app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db()
    conn.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)