// Profile page functionality

function getCart() {
  const cart = localStorage.getItem("musicStoreCart");
  return cart ? JSON.parse(cart) : [];
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

function formatDate(dateString) {
  const options = {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };
  return new Date(dateString).toLocaleDateString("en-US", options);
}

function getStatusBadge(status) {
  const statusMap = {
    pending: "status-pending",
    confirmed: "status-confirmed",
    shipped: "status-shipped",
    delivered: "status-delivered",
  };

  const badgeClass = statusMap[status] || "status-pending";
  const statusText = status.charAt(0).toUpperCase() + status.slice(1);

  return `<span class="order-status ${badgeClass}">${statusText}</span>`;
}

async function loadOrders() {
  try {
    const response = await fetch("/api/user/orders");
    const orders = await response.json();

    const container = document.getElementById("ordersContainer");

    if (!Array.isArray(orders) || orders.length === 0) {
      container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p>No orders yet</p>
                    <a href="/shop">Start Shopping</a>
                </div>
            `;
      return;
    }

    // Load items for each order
    const ordersWithItems = await Promise.all(
      orders.map(async (order) => {
        const itemsResponse = await fetch(`/api/user/orders/${order.id}/items`);
        const items = await itemsResponse.json();
        return { ...order, items };
      })
    );

    container.innerHTML = ordersWithItems
      .map(
        (order) => `
            <div class="order-card">
                <div class="order-header">
                    <div>
                        <div class="order-id">Order #${order.id}</div>
                        <div class="order-date">${formatDate(
                          order.created_at
                        )}</div>
                    </div>
                    ${getStatusBadge(order.status)}
                </div>

                <div class="order-items">
                    ${order.items
                      .map(
                        (item) => `
                        <div class="order-item">
                            <div class="item-info">
                                <div class="item-name">${item.name}</div>
                                <div class="item-qty">Quantity: ${
                                  item.quantity
                                }</div>
                            </div>
                            <div class="item-price">${formatCurrency(
                              item.price * item.quantity
                            )}</div>
                        </div>
                    `
                      )
                      .join("")}
                </div>

                <div class="order-footer">
                    <div class="order-total">
                        Total: <span>${formatCurrency(
                          order.total_amount
                        )}</span>
                    </div>
                    <button class="order-details-btn" onclick="showOrderDetails(${
                      order.id
                    })">
                        <i class="fas fa-eye"></i> View Details
                    </button>
                </div>
            </div>
        `
      )
      .join("");
  } catch (error) {
    console.error("Error loading orders:", error);
    const container = document.getElementById("ordersContainer");
    container.innerHTML = `
            <div style="padding: 40px; text-align: center; color: #e74c3c;">
                <i class="fas fa-exclamation-circle" style="font-size: 40px; margin-bottom: 10px;"></i>
                <p>Error loading orders. Please try again later.</p>
            </div>
        `;
  }
}

async function showOrderDetails(orderId) {
  try {
    const response = await fetch(`/api/orders/${orderId}`);
    const data = await response.json();

    const order = data.order;
    const items = data.items;

    const modal = document.getElementById("orderModal");
    const modalBody = document.getElementById("modalBody");

    const paymentMethod = order.payment_method.replace("_", " ").toUpperCase();

    let itemsHTML = items
      .map(
        (item) => `
            <div class="modal-item">
                <div class="modal-item-img">
                    ${
                      item.image_url
                        ? `<img src="${item.image_url}" alt="${item.name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 5px;">`
                        : '<i class="fas fa-music"></i>'
                    }
                </div>
                <div class="modal-item-details">
                    <div class="modal-item-name">${item.name}</div>
                    <div class="modal-item-qty">Quantity: ${item.quantity}</div>
                    <div class="modal-item-price">${formatCurrency(
                      item.price
                    )}</div>
                </div>
            </div>
        `
      )
      .join("");

    modalBody.innerHTML = `
            <div style="margin-bottom: 20px;">
                <h3 style="margin: 0 0 10px 0; color: #333;">Order Information</h3>
                <div style="display: grid; gap: 10px; font-size: 14px;">
                    <div><strong>Order ID:</strong> #${order.id}</div>
                    <div><strong>Date:</strong> ${formatDate(
                      order.created_at
                    )}</div>
                    <div><strong>Status:</strong> ${
                      order.status.charAt(0).toUpperCase() +
                      order.status.slice(1)
                    }</div>
                    <div><strong>Payment Method:</strong> ${paymentMethod}</div>
                </div>
            </div>

            <div style="margin-bottom: 20px;">
                <h3 style="margin: 0 0 15px 0; color: #333;">Items Ordered</h3>
                ${itemsHTML}
            </div>

            <div class="modal-summary">
                <div class="modal-row">
                    <span>Subtotal:</span>
                    <span>${formatCurrency(order.total_amount * 0.9)}</span>
                </div>
                <div class="modal-row">
                    <span>Tax (10%):</span>
                    <span>${formatCurrency(order.total_amount * 0.1)}</span>
                </div>
                <div class="modal-row modal-total">
                    <span>Total Amount:</span>
                    <span>${formatCurrency(order.total_amount)}</span>
                </div>
            </div>

            ${
              order.delivery_address
                ? `
                <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
                    <h3 style="margin: 0 0 10px 0; color: #333;">Delivery Address</h3>
                    <div style="white-space: pre-wrap; font-size: 14px; color: #666;">
                        ${order.delivery_address}
                    </div>
                </div>
            `
                : ""
            }
        `;

    modal.style.display = "block";
  } catch (error) {
    console.error("Error loading order details:", error);
    alert("Error loading order details");
  }
}

function setupMenuNavigation() {
  const menuItems = document.querySelectorAll(".menu-item");

  menuItems.forEach((item) => {
    item.addEventListener("click", function (e) {
      e.preventDefault();

      // Remove active class from all items
      menuItems.forEach((i) => i.classList.remove("active"));
      // Add active class to clicked item
      this.classList.add("active");

      // Hide all sections
      document.getElementById("ordersSection").style.display = "none";
      document.getElementById("accountSection").style.display = "none";
      document.getElementById("addressesSection").style.display = "none";

      // Show selected section
      const section = this.dataset.section;
      document.getElementById(section + "Section").style.display = "block";
    });
  });
}

function setupLogout() {
  document.getElementById("logoutBtn").addEventListener("click", async (e) => {
    e.preventDefault();

    try {
      await fetch("/api/auth/logout", { method: "POST" });
      window.location.href = "/login";
    } catch (error) {
      console.error("Error logging out:", error);
    }
  });
}

async function loadUserInfo() {
  try {
    const response = await fetch("/api/auth/status");
    const data = await response.json();

    if (data.logged_in) {
      document.getElementById("profileUsername").textContent = data.username;
    }
  } catch (error) {
    console.error("Error loading user info:", error);
  }
}

// Modal functionality
function setupModal() {
  const modal = document.getElementById("orderModal");
  const closeBtn = document.getElementById("closeModalBtn");

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
}

// Initialize
document.addEventListener("DOMContentLoaded", function () {
  updateCartCount();
  loadUserInfo();
  loadOrders();
  setupMenuNavigation();
  setupLogout();
  setupModal();
});
