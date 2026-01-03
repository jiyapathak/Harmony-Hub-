#!/usr/bin/env python3
"""
Database Viewer Script
Display database data in readable table format in terminal
"""

import sqlite3
import os
from tabulate import tabulate

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*100)
    print(title.center(100))
    print("="*100 + "\n")

def view_orders():
    """Display all orders"""
    db_path = 'music_store.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # ===== ORDERS VIEW =====
    print_section("📋 ALL ORDERS - WHO BOUGHT WHAT")
    
    cursor.execute('''
        SELECT 
            o.id as "Order ID",
            u.username as "Customer",
            GROUP_CONCAT(p.name, ', ') as "Products Bought",
            GROUP_CONCAT(oi.quantity, ', ') as "Quantities",
            SUM(oi.quantity * oi.price) as "Total Amount",
            o.payment_method as "Payment Method",
            o.status as "Status",
            o.created_at as "Order Date"
        FROM orders o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN products p ON oi.product_id = p.id
        GROUP BY o.id
        ORDER BY o.created_at DESC
    ''')
    
    orders = cursor.fetchall()
    if orders:
        rows = [dict(order) for order in orders]
        print(tabulate(rows, headers="keys", tablefmt="grid"))
    else:
        print("No orders found")
    
    # ===== INDIVIDUAL ITEMS SOLD =====
    print_section("🛍️  INDIVIDUAL ITEMS SOLD - DETAILED BREAKDOWN")
    
    cursor.execute('''
        SELECT 
            o.id as "Order ID",
            u.username as "Customer",
            p.name as "Product",
            p.category as "Category",
            oi.quantity as "Qty",
            oi.price as "Price",
            (oi.quantity * oi.price) as "Total",
            o.payment_method as "Payment",
            o.created_at as "Date"
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN users u ON o.user_id = u.id
        JOIN products p ON oi.product_id = p.id
        ORDER BY o.created_at DESC
    ''')
    
    items = cursor.fetchall()
    if items:
        rows = [dict(item) for item in items]
        print(tabulate(rows, headers="keys", tablefmt="grid"))
    else:
        print("No items sold yet")
    
    # ===== INVENTORY STATUS =====
    print_section("📦 INVENTORY STATUS - WHAT'S IN STOCK")
    
    cursor.execute('''
        SELECT 
            p.id as "ID",
            p.name as "Product Name",
            p.category as "Category",
            p.brand as "Brand",
            p.price as "Price",
            p.stock as "Current Stock",
            COALESCE(st.quantity_sold, 0) as "Units Sold",
            COALESCE(st.total_revenue, 0) as "Total Revenue",
            CASE 
                WHEN p.stock = 0 THEN '🔴 OUT'
                WHEN p.stock <= 5 THEN '🟡 LOW'
                ELSE '🟢 OK'
            END as "Status"
        FROM products p
        LEFT JOIN sales_tracking st ON p.id = st.product_id
        ORDER BY p.category, p.name
    ''')
    
    inventory = cursor.fetchall()
    if inventory:
        rows = [dict(item) for item in inventory]
        print(tabulate(rows, headers="keys", tablefmt="grid"))
    else:
        print("No products found")
    
    # ===== SALES SUMMARY =====
    print_section("📊 TOP SELLING PRODUCTS")
    
    cursor.execute('''
        SELECT 
            p.id as "ID",
            p.name as "Product",
            p.category as "Category",
            COALESCE(st.quantity_sold, 0) as "Units Sold",
            COALESCE(st.total_revenue, 0) as "Total Revenue",
            p.stock as "Stock Left",
            p.price as "Price"
        FROM products p
        LEFT JOIN sales_tracking st ON p.id = st.product_id
        WHERE COALESCE(st.quantity_sold, 0) > 0
        ORDER BY st.quantity_sold DESC
    ''')
    
    top_sellers = cursor.fetchall()
    if top_sellers:
        rows = [dict(item) for item in top_sellers]
        print(tabulate(rows, headers="keys", tablefmt="grid"))
    else:
        print("No sales recorded yet")
    
    # ===== SUMMARY STATISTICS =====
    print_section("📈 SUMMARY STATISTICS")
    
    cursor.execute('SELECT COUNT(*) as total_orders FROM orders')
    total_orders = cursor.fetchone()['total_orders']
    
    cursor.execute('SELECT SUM(total_amount) as total_revenue FROM orders')
    total_revenue = cursor.fetchone()['total_revenue'] or 0
    
    cursor.execute('SELECT COUNT(*) as total_customers FROM users WHERE is_admin = 0')
    total_customers = cursor.fetchone()['total_customers']
    
    cursor.execute('SELECT COUNT(*) as total_products FROM products')
    total_products = cursor.fetchone()['total_products']
    
    cursor.execute('SELECT SUM(quantity_sold) as total_units FROM sales_tracking')
    total_units = cursor.fetchone()['total_units'] or 0
    
    cursor.execute('SELECT SUM(stock) as total_stock FROM products')
    total_stock = cursor.fetchone()['total_stock'] or 0
    
    stats = [
        ["📦 Total Products", total_products],
        ["👥 Total Customers", total_customers],
        ["🛒 Total Orders", total_orders],
        ["💰 Total Revenue", f"${total_revenue:,.2f}"],
        ["📊 Units Sold", total_units],
        ["🏪 Stock Remaining", total_stock],
        ["💵 Avg Order Value", f"${total_revenue/total_orders if total_orders > 0 else 0:,.2f}"]
    ]
    
    print(tabulate(stats, headers=["Metric", "Value"], tablefmt="grid"))
    
    conn.close()

if __name__ == "__main__":
    print("\n" + "="*100)
    print("DATABASE VIEWER - REAL-TIME DATA VIEW".center(100))
    print("="*100)
    
    try:
        view_orders()
        print("\n✅ View complete!\n")
    except ImportError:
        print("\n⚠️  'tabulate' module not found.")
        print("Install it with: pip install tabulate\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
