# HarmonyHub - E-Commerce Music Store

A full-featured e-commerce platform for buying and selling musical instruments with order management, inventory tracking, and payment processing.

## Features Implemented

### 1. **Shopping Cart Management**

- Add/remove products from cart
- Update quantities
- Persistent cart storage using localStorage
- Real-time cart count display

### 2. **Order Management System**

#### Checkout Flow:

- **Order Placement**: Users can create orders from their cart
- **Payment Methods**:
  - Cash on Delivery (COD) - Default option
  - Credit/Debit Card
  - Digital Wallet (Google Pay, Apple Pay)
- **Delivery Address Collection**:

  - Full name
  - Phone number
  - Email
  - Complete address
  - City & ZIP code

- **Order Confirmation**:
  - Order ID generation
  - Status tracking
  - Order placed confirmation page

### 3. **User Profile & Order History**

- View all past orders
- Order status tracking:
  - Pending
  - Confirmed
  - Shipped
  - Delivered
- **Order Details Modal**:
  - View items ordered
  - Product images
  - Quantities and prices
  - Payment method used
  - Delivery address
  - Order timeline

### 4. **Backend Order Storage**

Database tables for complete order management:

- **orders table**: Main order records with user_id, total_amount, payment_method, delivery_address, status
- **order_items table**: Individual items in each order with product_id, quantity, price

### 5. **Inventory Management**

- **Product Stock Tracking**:
  - Automatic stock reduction on purchase
  - Stock availability display
- **Sales Analytics**:
  - **sales_tracking table**: Monitors:
    - Quantity sold per product
    - Total revenue per product
    - Last updated timestamp

### 6. **Admin Dashboard (Backend)**

- View complete sales data
- Inventory overview with:
  - Current stock levels
  - Total units sold
  - Revenue generated per product
  - Product categories and pricing

## API Endpoints

### Order Management

```
POST   /api/orders                        - Create new order
GET    /api/orders/<order_id>            - Get order details
GET    /api/user/orders                  - Get user's all orders
GET    /api/user/orders/<order_id>/items - Get items in order
```

### Admin (Requires Authentication)

```
GET    /api/admin/sales-data    - Get sales analytics
GET    /api/admin/inventory     - Get inventory status
```

## Database Schema

### Orders Table

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    total_amount REAL,
    status TEXT DEFAULT 'pending',
    payment_method TEXT,
    delivery_address TEXT,
    created_at TIMESTAMP
)
```

### Order Items Table

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL
)
```

### Sales Tracking Table

```sql
CREATE TABLE sales_tracking (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity_sold INTEGER DEFAULT 0,
    total_revenue REAL DEFAULT 0,
    last_updated TIMESTAMP
)
```

## File Structure

### New Files Created:

- `templates/checkout.html` - Checkout page with delivery & payment info
- `templates/profile.html` - User profile with order history
- `static/js/checkout.js` - Checkout functionality
- `static/js/profile.js` - Profile and order history management

### Modified Files:

- `app.py` - Added order management routes and database tables
- `static/js/cart.js` - Added checkout redirect function
- `requirements.txt` - Added flask-cors dependency

## Usage Flow

### Customer Journey:

1. **Browse Products** → Select items → Add to cart
2. **View Cart** → Review items → Click "Proceed to Checkout"
3. **Login** (if not already logged in)
4. **Checkout Page**:
   - Enter delivery address
   - Select payment method
   - Review order summary
   - Place order
5. **Order Confirmation** → Redirected to Profile
6. **Profile Page**:
   - View all orders
   - Track order status
   - View detailed order information
   - Download/print order

### Admin Dashboard:

1. Access `/admin` panel
2. View sales data API at `/api/admin/sales-data`
3. View inventory at `/api/admin/inventory`
4. Monitor:
   - Total sales per product
   - Revenue generated
   - Stock levels
   - Best-selling products

## Order Status Workflow

```
Pending → Confirmed → Shipped → Delivered
```

## Key Features:

✅ **Real-time Cart Management**
✅ **Multiple Payment Options**
✅ **Automated Inventory Tracking**
✅ **Complete Order History**
✅ **Sales Analytics**
✅ **Responsive Design**
✅ **Secure Checkout**
✅ **Order Confirmation**

## Installation & Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python app.py
```

3. Access the application:

- Frontend: http://localhost:5000
- Admin Panel: http://localhost:5000/admin (requires admin login)

## Authentication

Default Admin Credentials:

- Username: `admin`
- Password: `admin123`

## Technologies Used

- **Backend**: Flask with SQLite
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Database**: SQLite3
- **Storage**: localStorage (cart), Server (orders)
- **Payment Methods**: Integrated (COD, Card, Digital Wallet)

## Future Enhancements

- Email notifications for order status
- Payment gateway integration (Stripe, PayPal)
- Advanced inventory management
- Customer reviews and ratings
- Wishlist functionality
- Order tracking with map
- Return/Refund management
- Subscription models
