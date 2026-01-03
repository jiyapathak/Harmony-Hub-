// Checkout functionality

function getCart() {
  const cart = localStorage.getItem("musicStoreCart");
  return cart ? JSON.parse(cart) : [];
}

function clearCart() {
  localStorage.removeItem("musicStoreCart");
  updateCartCount();
}

function updateCartCount() {
  const cart = getCart();
  const count = cart.reduce((total, item) => total + item.quantity, 0);
  document.getElementById("cartCount").textContent = count;
}

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

function calculateTotals() {
  const cart = getCart();
  const subtotal = cart.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  );
  const shipping = subtotal > 100 ? 0 : 10;
  const tax = (subtotal + shipping) * 0.1;
  const total = subtotal + shipping + tax;

  return {
    subtotal,
    shipping,
    tax,
    total,
  };
}

function loadOrderItems() {
  const cart = getCart();
  const itemsContainer = document.getElementById("orderItems");

  if (cart.length === 0) {
    window.location.href = "/cart";
    return;
  }

  itemsContainer.innerHTML = cart
    .map(
      (item) => `
        <div class="order-item">
            <div class="item-details">
                <div class="item-name">${item.name}</div>
                <div class="item-qty">Quantity: ${item.quantity}</div>
            </div>
            <div class="item-price">${formatCurrency(
              item.price * item.quantity
            )}</div>
        </div>
    `
    )
    .join("");

  updateSummary();
}

function updateSummary() {
  const totals = calculateTotals();

  document.getElementById("subtotal").textContent = formatCurrency(
    totals.subtotal
  );
  document.getElementById("shipping").textContent = formatCurrency(
    totals.shipping
  );
  document.getElementById("tax").textContent = formatCurrency(totals.tax);
  document.getElementById("total").textContent = formatCurrency(totals.total);
}

function setupPaymentMethodToggle() {
  const paymentOptions = document.querySelectorAll(
    'input[name="payment_method"]'
  );
  const cardDetails = document.getElementById("cardDetails");

  paymentOptions.forEach((option) => {
    option.addEventListener("change", function () {
      // Update selected state
      document.querySelectorAll(".payment-option").forEach((el) => {
        el.classList.remove("selected");
      });
      this.parentElement.classList.add("selected");

      // Show/hide card details
      if (this.value === "credit_card") {
        cardDetails.style.display = "block";
      } else {
        cardDetails.style.display = "none";
      }
    });
  });
}

function validateForm() {
  const form = document.getElementById("checkoutForm");
  const paymentMethod = document.querySelector(
    'input[name="payment_method"]:checked'
  ).value;

  // Basic validation
  if (!form.checkValidity()) {
    return false;
  }

  // Card validation if credit card is selected
  if (paymentMethod === "credit_card") {
    const cardNumber = document
      .getElementById("cardNumber")
      .value.replace(/\s/g, "");
    const expiry = document.getElementById("expiry").value;
    const cvv = document.getElementById("cvv").value;

    if (!cardNumber || cardNumber.length !== 16) {
      showError("Please enter a valid card number");
      return false;
    }

    if (!expiry || !expiry.match(/^\d{2}\/\d{2}$/)) {
      showError("Please enter expiry date in MM/YY format");
      return false;
    }

    if (!cvv || cvv.length !== 3) {
      showError("Please enter a valid CVV");
      return false;
    }
  }

  return true;
}

function showError(message) {
  const errorEl = document.getElementById("errorMessage");
  errorEl.textContent = message;
  errorEl.style.display = "block";
  setTimeout(() => {
    errorEl.style.display = "none";
  }, 5000);
}

function showSuccess(message) {
  const successEl = document.getElementById("successMessage");
  successEl.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
  successEl.style.display = "block";
}

async function handleCheckout(e) {
  e.preventDefault();

  if (!validateForm()) {
    return;
  }

  const submitBtn = document.getElementById("submitBtn");
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

  const cart = getCart();
  const paymentMethod = document.querySelector(
    'input[name="payment_method"]:checked'
  ).value;

  const deliveryAddress = `
        ${document.getElementById("fullName").value}
        ${document.getElementById("address").value}
        ${document.getElementById("city").value}
        ${document.getElementById("zipCode").value}
        Phone: ${document.getElementById("phone").value}
    `;

  try {
    const response = await fetch("/api/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        items: cart,
        payment_method: paymentMethod,
        delivery_address: deliveryAddress,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Error placing order");
    }

    // Clear cart
    clearCart();

    // Show success message
    showSuccess("Order placed successfully! Order ID: #" + data.order_id);

    // Redirect to profile after 2 seconds
    setTimeout(() => {
      window.location.href = "/profile";
    }, 2000);
  } catch (error) {
    console.error("Error:", error);
    showError(error.message);
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<i class="fas fa-lock"></i> Place Order';
  }
}

// Initialize
document.addEventListener("DOMContentLoaded", function () {
  updateCartCount();
  loadOrderItems();
  setupPaymentMethodToggle();

  document
    .getElementById("checkoutForm")
    .addEventListener("submit", handleCheckout);

  // Format card number input
  const cardNumberInput = document.getElementById("cardNumber");
  if (cardNumberInput) {
    cardNumberInput.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\s/g, "");
      let formattedValue = "";
      for (let i = 0; i < value.length; i++) {
        if (i > 0 && i % 4 === 0) {
          formattedValue += " ";
        }
        formattedValue += value[i];
      }
      e.target.value = formattedValue;
    });
  }

  // Format expiry input
  const expiryInput = document.getElementById("expiry");
  if (expiryInput) {
    expiryInput.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length >= 2) {
        value = value.substring(0, 2) + "/" + value.substring(2, 4);
      }
      e.target.value = value;
    });
  }

  // CVV only numbers
  const cvvInput = document.getElementById("cvv");
  if (cvvInput) {
    cvvInput.addEventListener("input", function (e) {
      e.target.value = e.target.value.replace(/\D/g, "").substring(0, 3);
    });
  }
});
