# Quick Start Guide - Order System

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Application

```bash
python app.py
```

Access at: `http://localhost:5000`

---

## How It Works

### For Customers:

#### Step 1: Browse & Shop

- Go to `/shop`
- Select products
- Click "Add to Cart"
- Cart count updates in navbar

#### Step 2: Review Cart

- Click shopping cart icon
- Review items
- Adjust quantities
- See order summary

#### Step 3: Checkout

- Click "Proceed to Checkout" button
- If not logged in, redirected to login page
- Log in or register

#### Step 4: Enter Details

- **Full Name**: Your name
- **Phone**: Contact number
- **Email**: Email address
- **Address**: Complete address
- **City**: City name
- **ZIP Code**: Postal code

#### Step 5: Select Payment

- **Cash on Delivery** (default) - Pay when you receive
- **Credit/Debit Card** - Enter card details
- **Digital Wallet** - Google Pay, Apple Pay

#### Step 6: Place Order

- Click "Place Order" button
- Order created successfully
- Automatically redirected to profile

#### Step 7: View Profile

- Click user icon in navbar
- See all your orders
- Click "View Details" for full order info
- Track order status

---

### For Admin:

#### Access Sales Data

```
GET http://localhost:5000/api/admin/sales-data
```

Response includes:

- Product names
- Category
- Quantity sold
- Total revenue
- Last updated

#### Access Inventory

```
GET http://localhost:5000/api/admin/inventory
```

Response includes:

- All products
- Current stock
- Units sold
- Revenue generated
- Product prices

---

## Testing Scenarios

### Scenario 1: Complete Purchase

1. Open `/shop`
2. Add guitar to cart (Fender Stratocaster)
3. Add drum kit to cart
4. Go to cart
5. Click "Proceed to Checkout"
6. Create account or login
7. Fill delivery details
8. Select "Cash on Delivery"
9. Click "Place Order"
10. Verify order appears in profile

### Scenario 2: Try Different Payment

1. Add products to cart
2. Go to checkout
3. Select "Credit/Debit Card"
4. Enter test card: `4111 1111 1111 1111`
5. Expiry: `12/25`
6. CVV: `123`
7. Place order

### Scenario 3: View Order History

1. Log in to profile
2. Click "My Orders"
3. See all past orders with status
4. Click "View Details" on any order
5. See items, prices, delivery address

### Scenario 4: Check Inventory Changes

1. Check current stock of product
2. Place an order with that product
3. Check stock again
4. Stock should be reduced by order quantity

---

## Database Tables

After first run, these tables are created:

1. **orders** - All customer orders
2. **order_items** - Items in each order
3. **sales_tracking** - Sales analytics
4. **products** - Product catalog
5. **users** - Customer accounts

---

## Sample Test Data

### Default Admin

- Username: `admin`
- Password: `admin123`

### Sample Products (Auto-loaded)

1. Fender Stratocaster - $1,299.99
2. Yamaha P-125 Piano - $649.99
3. Pearl Export Drum Kit - $899.99
4. Stentor Violin - $299.99
5. Yamaha Flute - $549.99
6. Pioneer DJ Controller - $249.99
7. Shure SM58 Mic - $99.99
8. Boss Katana Amp - $229.99
9. Gibson Les Paul - $2,499.99
10. Roland Electronic Drums - $1,699.99
11. Korg Stage Piano - $1,999.99
12. D'Addario Strings - $19.99

---

## API Endpoints Reference

### Order Management

```
POST   /api/orders                        Create order
GET    /api/orders/<id>                  Get order details
GET    /api/user/orders                  Get user's orders
GET    /api/user/orders/<id>/items       Get order items
```

### Authentication

```
POST   /api/auth/register                Register user
POST   /api/auth/login                   Login user
POST   /api/auth/logout                  Logout user
GET    /api/auth/status                  Check login status
```

### Products

```
GET    /api/products                     Get all products
GET    /api/products/<id>                Get product details
```

### Admin

```
GET    /api/admin/sales-data             Sales analytics
GET    /api/admin/inventory              Inventory status
POST   /api/admin/products               Add product
PUT    /api/admin/products/<id>          Update product
DELETE /api/admin/products/<id>          Delete product
```

---

## Order Status Codes

| Status      | Meaning         | When Set           |
| ----------- | --------------- | ------------------ |
| `pending`   | Order placed    | After checkout     |
| `confirmed` | Order confirmed | Admin confirmation |
| `shipped`   | Order shipped   | Item dispatch      |
| `delivered` | Order delivered | Delivery complete  |

---

## Troubleshooting

### Issue: "Database locked" error

**Solution**: Close other instances of the app, restart

### Issue: Cart not updating

**Solution**: Clear localStorage, refresh browser

```javascript
localStorage.clear();
```

### Issue: Orders not saving

**Solution**: Check database permissions, ensure sqlite3 installed

### Issue: Login required message

**Solution**: Log in first before checkout

### Issue: Stock not decreasing

**Solution**: Reload admin page or check sales_tracking table

---

## Common Errors & Solutions

| Error                 | Cause                  | Fix                 |
| --------------------- | ---------------------- | ------------------- |
| "Not logged in"       | User not authenticated | Login first         |
| "Order not found"     | Wrong order ID         | Check user's orders |
| "Invalid credentials" | Wrong password         | Reset password      |
| "Database error"      | DB corruption          | Backup and rebuild  |

---

## Performance Tips

1. **Clear old test data**

   - Delete `music_store.db` to reset
   - App will recreate with sample data

2. **Check order count**

   ```sql
   SELECT COUNT(*) FROM orders;
   ```

3. **View sales by product**
   ```sql
   SELECT p.name, st.quantity_sold, st.total_revenue
   FROM products p
   LEFT JOIN sales_tracking st ON p.id = st.product_id
   ORDER BY st.quantity_sold DESC;
   ```

---

## Next Steps

1. ✅ Test basic ordering flow
2. ✅ Verify database updates
3. ✅ Check admin analytics
4. ✅ Test different payment methods
5. ✅ Deploy to production
6. 🔄 Add email notifications
7. 🔄 Integrate payment gateway
8. 🔄 Add order tracking

---

## Support

For issues or questions:

1. Check logs in terminal
2. Review database with SQLite browser
3. Test API endpoints with Postman
4. Check browser console for JS errors
5. Verify all files are in correct locations

---

**Ready to process orders! 🎵🛒✅**
