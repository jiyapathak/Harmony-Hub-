#!/usr/bin/env python3
"""
Database Export Script
Exports database data to CSV and JSON files for easy viewing
"""

import sqlite3
import csv
import json
import os
from datetime import datetime

def export_to_csv_and_json():
    """Export database data to CSV and JSON files"""
    
    db_path = 'music_store.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Create exports directory
        if not os.path.exists('exports'):
            os.makedirs('exports')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # ===== 1. SALES DATA (Orders with Customer Info) =====
        print("\n📊 Exporting SALES DATA...")
        
        cursor.execute('''
            SELECT 
                o.id as order_id,
                u.username as customer,
                u.email as email,
                o.total_amount as total_amount,
                o.status as status,
                o.payment_method as payment_method,
                o.delivery_address as delivery_address,
                o.created_at as order_date,
                COUNT(oi.id) as items_count
            FROM orders o
            JOIN users u ON o.user_id = u.id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            GROUP BY o.id
            ORDER BY o.created_at DESC
        ''')
        
        sales_data = [dict(row) for row in cursor.fetchall()]
        
        # Export to CSV
        if sales_data:
            csv_file = f'exports/sales_data_{timestamp}.csv'
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=sales_data[0].keys())
                writer.writeheader()
                writer.writerows(sales_data)
            print(f"  ✓ CSV exported: {csv_file}")
        
        # Export to JSON
        json_file = f'exports/sales_data_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(sales_data, f, indent=2)
        print(f"  ✓ JSON exported: {json_file}")
        
        # ===== 2. CUSTOMER PURCHASE DETAILS =====
        print("\n🛒 Exporting CUSTOMER PURCHASE DETAILS...")
        
        cursor.execute('''
            SELECT 
                o.id as order_id,
                u.username as customer,
                p.name as product_name,
                p.category as category,
                p.brand as brand,
                oi.quantity as quantity_bought,
                oi.price as price_per_item,
                (oi.quantity * oi.price) as total_item_price,
                o.payment_method as payment_method,
                o.status as order_status,
                o.created_at as purchase_date
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN users u ON o.user_id = u.id
            JOIN products p ON oi.product_id = p.id
            ORDER BY o.created_at DESC
        ''')
        
        purchases_data = [dict(row) for row in cursor.fetchall()]
        
        # Export to CSV
        if purchases_data:
            csv_file = f'exports/customer_purchases_{timestamp}.csv'
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=purchases_data[0].keys())
                writer.writeheader()
                writer.writerows(purchases_data)
            print(f"  ✓ CSV exported: {csv_file}")
        
        # Export to JSON
        json_file = f'exports/customer_purchases_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(purchases_data, f, indent=2)
        print(f"  ✓ JSON exported: {json_file}")
        
        # ===== 3. INVENTORY & STOCK STATUS =====
        print("\n📦 Exporting INVENTORY & STOCK STATUS...")
        
        cursor.execute('''
            SELECT 
                p.id as product_id,
                p.name as product_name,
                p.category as category,
                p.brand as brand,
                p.price as price,
                p.stock as current_stock,
                COALESCE(st.quantity_sold, 0) as units_sold,
                COALESCE(st.total_revenue, 0) as total_revenue,
                p.rating as rating,
                CASE 
                    WHEN p.stock = 0 THEN 'OUT OF STOCK'
                    WHEN p.stock <= 5 THEN 'LOW STOCK'
                    ELSE 'IN STOCK'
                END as stock_status,
                st.last_updated as last_sales_update
            FROM products p
            LEFT JOIN sales_tracking st ON p.id = st.product_id
            ORDER BY p.category, p.name
        ''')
        
        inventory_data = [dict(row) for row in cursor.fetchall()]
        
        # Export to CSV
        if inventory_data:
            csv_file = f'exports/inventory_stock_{timestamp}.csv'
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=inventory_data[0].keys())
                writer.writeheader()
                writer.writerows(inventory_data)
            print(f"  ✓ CSV exported: {csv_file}")
        
        # Export to JSON
        json_file = f'exports/inventory_stock_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(inventory_data, f, indent=2)
        print(f"  ✓ JSON exported: {json_file}")
        
        # ===== 4. SALES SUMMARY BY PRODUCT =====
        print("\n📈 Exporting SALES SUMMARY BY PRODUCT...")
        
        cursor.execute('''
            SELECT 
                p.id as product_id,
                p.name as product_name,
                p.category as category,
                p.brand as brand,
                p.price as current_price,
                COALESCE(st.quantity_sold, 0) as total_sold,
                COALESCE(st.total_revenue, 0) as total_revenue,
                ROUND(COALESCE(st.total_revenue, 0) / NULLIF(COALESCE(st.quantity_sold, 0), 0), 2) as average_price
            FROM products p
            LEFT JOIN sales_tracking st ON p.id = st.product_id
            ORDER BY COALESCE(st.quantity_sold, 0) DESC
        ''')
        
        sales_summary = [dict(row) for row in cursor.fetchall()]
        
        # Export to CSV
        if sales_summary:
            csv_file = f'exports/sales_summary_{timestamp}.csv'
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=sales_summary[0].keys())
                writer.writeheader()
                writer.writerows(sales_summary)
            print(f"  ✓ CSV exported: {csv_file}")
        
        # Export to JSON
        json_file = f'exports/sales_summary_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(sales_summary, f, indent=2)
        print(f"  ✓ JSON exported: {json_file}")
        
        # ===== 5. SUMMARY STATISTICS =====
        print("\n📊 Generating SUMMARY STATISTICS...")
        
        cursor.execute('SELECT COUNT(*) as total_orders FROM orders')
        total_orders = cursor.fetchone()['total_orders']
        
        cursor.execute('SELECT SUM(total_amount) as total_revenue FROM orders')
        total_revenue = cursor.fetchone()['total_revenue'] or 0
        
        cursor.execute('SELECT COUNT(*) as total_customers FROM users WHERE is_admin = 0')
        total_customers = cursor.fetchone()['total_customers']
        
        cursor.execute('SELECT COUNT(*) as total_products FROM products')
        total_products = cursor.fetchone()['total_products']
        
        cursor.execute('SELECT SUM(quantity_sold) as total_units_sold FROM sales_tracking')
        total_units = cursor.fetchone()['total_units_sold'] or 0
        
        cursor.execute('SELECT SUM(stock) as total_stock FROM products')
        total_stock = cursor.fetchone()['total_stock'] or 0
        
        statistics = {
            "export_date": datetime.now().isoformat(),
            "summary": {
                "total_orders": total_orders,
                "total_revenue": float(total_revenue),
                "total_customers": total_customers,
                "total_products": total_products,
                "total_units_sold": total_units,
                "total_stock_remaining": total_stock,
                "average_order_value": float(total_revenue / total_orders) if total_orders > 0 else 0
            },
            "sales_data": {
                "total_files": len(sales_data),
                "latest_order_date": max([item['order_date'] for item in sales_data]) if sales_data else None
            },
            "inventory_data": {
                "total_products": len(inventory_data),
                "in_stock_products": len([x for x in inventory_data if x['stock_status'] == 'IN STOCK']),
                "low_stock_products": len([x for x in inventory_data if x['stock_status'] == 'LOW STOCK']),
                "out_of_stock_products": len([x for x in inventory_data if x['stock_status'] == 'OUT OF STOCK'])
            }
        }
        
        # Export statistics
        stats_file = f'exports/summary_statistics_{timestamp}.json'
        with open(stats_file, 'w') as f:
            json.dump(statistics, f, indent=2)
        print(f"  ✓ Statistics exported: {stats_file}")
        
        # Print summary to console
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        print(f"\n📦 Products & Inventory:")
        print(f"  • Total Products: {total_products}")
        print(f"  • In Stock: {statistics['inventory_data']['in_stock_products']}")
        print(f"  • Low Stock: {statistics['inventory_data']['low_stock_products']}")
        print(f"  • Out of Stock: {statistics['inventory_data']['out_of_stock_products']}")
        print(f"  • Total Stock Remaining: {total_stock} units")
        
        print(f"\n💰 Sales & Revenue:")
        print(f"  • Total Orders: {total_orders}")
        print(f"  • Total Revenue: ${total_revenue:,.2f}")
        print(f"  • Units Sold: {total_units}")
        print(f"  • Average Order Value: ${statistics['summary']['average_order_value']:,.2f}")
        
        print(f"\n👥 Customers:")
        print(f"  • Total Customers: {total_customers}")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ EXPORT COMPLETE!")
        print("="*60)
        print(f"\n📁 All files saved to: exports/")
        print(f"\nFiles created:")
        print(f"  • sales_data_{timestamp}.csv / .json")
        print(f"  • customer_purchases_{timestamp}.csv / .json")
        print(f"  • inventory_stock_{timestamp}.csv / .json")
        print(f"  • sales_summary_{timestamp}.csv / .json")
        print(f"  • summary_statistics_{timestamp}.json")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during export: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("DATABASE EXPORT UTILITY")
    print("="*60)
    
    success = export_to_csv_and_json()
    
    if success:
        print("\n✨ You can now open the CSV files in Excel or Google Sheets!")
        print("✨ Or view the JSON files in any text editor!")
    else:
        print("\n⚠️  Please check the errors above")
