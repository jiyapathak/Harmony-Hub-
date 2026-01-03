// Cart Management using localStorage

// Get cart from localStorage
function getCart() {
  const cart = localStorage.getItem("musicStoreCart");
  return cart ? JSON.parse(cart) : [];
}

// Save cart to localStorage
function saveCart(cart) {
  localStorage.setItem("musicStoreCart", JSON.stringify(cart));
  updateCartCount();
}

// Add item to cart
function addToCart(id, name, price, image) {
  const cart = getCart();
  const existingItem = cart.find((item) => item.id === id);

  if (existingItem) {
    existingItem.quantity += 1;
  } else {
    cart.push({
      id: id,
      name: name,
      price: price,
      image: image,
      quantity: 1,
    });
  }

  saveCart(cart);
  showNotification("Item added to cart!");
}

// Remove item from cart
function removeFromCart(id) {
  let cart = getCart();
  cart = cart.filter((item) => item.id !== id);
  saveCart(cart);

  // Reload cart page if we're on it
  if (window.location.pathname === "/cart") {
    loadCart();
  }
}

// Update item quantity
function updateQuantity(id, quantity) {
  const cart = getCart();
  const item = cart.find((item) => item.id === id);

  if (item) {
    if (quantity <= 0) {
      removeFromCart(id);
    } else {
      item.quantity = quantity;
      saveCart(cart);

      // Reload cart page if we're on it
      if (window.location.pathname === "/cart") {
        loadCart();
      }
    }
  }
}

// Update cart count in navbar
function updateCartCount() {
  const cart = getCart();
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
  const cartCountElements = document.querySelectorAll("#cartCount");
  cartCountElements.forEach((el) => {
    el.textContent = totalItems;
    el.style.display = totalItems > 0 ? "flex" : "none";
  });
}

// Get cart total
function getCartTotal() {
  const cart = getCart();
  return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Show notification
function showNotification(message) {
  // Create notification element
  const notification = document.createElement("div");
  notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
  notification.innerHTML = `
        <i class="fas fa-check-circle"></i> ${message}
    `;

  document.body.appendChild(notification);

  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.animation = "slideOutRight 0.3s ease";
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Checkout function
function checkout() {
  const cart = getCart();

  if (cart.length === 0) {
    alert("Your cart is empty!");
    return;
  }

  // Check if user is logged in
  fetch("/api/auth/status")
    .then((response) => response.json())
    .then((data) => {
      if (data.logged_in) {
        window.location.href = "/checkout";
      } else {
        alert("Please login first to checkout");
        window.location.href = "/login";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Please login to checkout");
      window.location.href = "/login";
    });
}

// Initialize cart count on page load
document.addEventListener("DOMContentLoaded", updateCartCount);

// Add animation styles
const style = document.createElement("style");
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
