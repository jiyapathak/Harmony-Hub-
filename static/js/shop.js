// Shop Page JavaScript

document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    
    // Get category from URL if present
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');
    if (category) {
        document.getElementById('categoryFilter').value = category;
        applyFilters();
    }
    
    // Add enter key listener for search
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            applyFilters();
        }
    });
});

// Load all products
async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Apply filters
async function applyFilters() {
    const category = document.getElementById('categoryFilter').value;
    const minPrice = document.getElementById('minPrice').value;
    const maxPrice = document.getElementById('maxPrice').value;
    const search = document.getElementById('searchInput').value;
    
    // Build query string
    const params = new URLSearchParams();
    if (category && category !== 'all') params.append('category', category);
    if (minPrice) params.append('min_price', minPrice);
    if (maxPrice) params.append('max_price', maxPrice);
    if (search) params.append('search', search);
    
    try {
        const response = await fetch(`/api/products?${params.toString()}`);
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error filtering products:', error);
    }
}

// Display products
function displayProducts(products) {
    const grid = document.getElementById('productsGrid');
    const noProducts = document.getElementById('noProducts');
    
    grid.innerHTML = '';
    
    if (products.length === 0) {
        grid.style.display = 'none';
        noProducts.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    noProducts.style.display = 'none';
    
    products.forEach(product => {
        const card = createProductCard(product);
        grid.appendChild(card);
    });
}

// Create product card
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.onclick = () => window.location.href = `/product/${product.id}`;
    
    const stars = '⭐'.repeat(Math.floor(product.rating));
    const stockStatus = product.stock > 0 
        ? `<span style="color: #10b981;">In Stock (${product.stock})</span>`
        : '<span style="color: #ef4444;">Out of Stock</span>';
    
    card.innerHTML = `
        <img src="${product.image_url}" alt="${product.name}" class="product-image">
        <div class="product-info">
            <div class="product-brand">${product.brand}</div>
            <h3 class="product-name">${product.name}</h3>
            <div class="product-rating">
                ${stars} <span style="color: var(--text-secondary)">(${product.rating})</span>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0.5rem 0;">${product.description}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                <div class="product-price">$${product.price.toFixed(2)}</div>
                <div style="font-size: 0.85rem;">${stockStatus}</div>
            </div>
            <button 
                class="add-to-cart-btn" 
                onclick="event.stopPropagation(); addToCart(${product.id}, '${product.name.replace(/'/g, "\\'")}', ${product.price}, '${product.image_url}')"
                ${product.stock <= 0 ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}
            >
                <i class="fas fa-shopping-cart"></i> ${product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
            </button>
        </div>
    `;
    
    return card;
}