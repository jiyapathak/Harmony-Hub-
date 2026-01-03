// Main JavaScript for Home Page

// Load featured products on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadFeaturedProducts();
    updateCartCount();
    checkAuthStatus();
});

// Load featured products
async function loadFeaturedProducts() {
    try {
        const response = await fetch('/api/products');
        const products = await response.json();
        
        // Get first 6 products for featured section
        const featured = products.slice(0, 6);
        displayProducts(featured);
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Display products in grid
function displayProducts(products) {
    const grid = document.getElementById('featuredProducts');
    grid.innerHTML = '';
    
    products.forEach(product => {
        const card = createProductCard(product);
        grid.appendChild(card);
    });
}

// Create product card element
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.onclick = () => window.location.href = `/product/${product.id}`;
    
    const stars = '⭐'.repeat(Math.floor(product.rating));
    
    card.innerHTML = `
        <img src="${product.image_url}" alt="${product.name}" class="product-image">
        <div class="product-info">
            <div class="product-brand">${product.brand}</div>
            <h3 class="product-name">${product.name}</h3>
            <div class="product-rating">
                ${stars} <span style="color: var(--text-secondary)">(${product.rating})</span>
            </div>
            <div class="product-price">$${product.price.toFixed(2)}</div>
            <button class="add-to-cart-btn" onclick="event.stopPropagation(); addToCart(${product.id}, '${product.name}', ${product.price}, '${product.image_url}')">
                <i class="fas fa-shopping-cart"></i> Add to Cart
            </button>
        </div>
    `;
    
    return card;
}

// Check authentication status
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/status');
        const data = await response.json();
        
        const userIcon = document.getElementById('userIcon');
        if (data.logged_in) {
            userIcon.innerHTML = `<i class="fas fa-user-circle"></i>`;
            userIcon.title = `Logged in as ${data.username}`;
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
    }
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});