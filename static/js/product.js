// Product Detail Page JavaScript

document.addEventListener('DOMContentLoaded', () => {
    loadProductDetail();
});

async function loadProductDetail() {
    try {
        const response = await fetch(`/api/products/${productId}`);
        
        if (!response.ok) {
            throw new Error('Product not found');
        }
        
        const product = await response.json();
        displayProductDetail(product);
    } catch (error) {
        console.error('Error loading product:', error);
        document.getElementById('productDetail').innerHTML = `
            <div style="text-align: center; padding: 4rem;">
                <h2>Product Not Found</h2>
                <p style="color: var(--text-secondary); margin: 1rem 0;">The product you're looking for doesn't exist.</p>
                <a href="/shop" class="btn btn-primary">Back to Shop</a>
            </div>
        `;
    }
}

function displayProductDetail(product) {
    const container = document.getElementById('productDetail');
    const stars = '⭐'.repeat(Math.floor(product.rating));
    
    const stockStatus = product.stock > 0 
        ? `<span style="color: #10b981;"><i class="fas fa-check-circle"></i> In Stock (${product.stock} available)</span>`
        : '<span style="color: #ef4444;"><i class="fas fa-times-circle"></i> Out of Stock</span>';
    
    container.innerHTML = `
        <div class="product-detail-grid">
            <div class="product-detail-image">
                <img src="${product.image_url}" alt="${product.name}">
            </div>
            <div class="product-detail-info">
                <div class="product-brand">${product.brand}</div>
                <h1 class="product-detail-title">${product.name}</h1>
                <div class="product-rating">
                    ${stars} <span style="color: var(--text-secondary); margin-left: 0.5rem;">${product.rating} / 5.0</span>
                </div>
                <div class="product-detail-price">$${product.price.toFixed(2)}</div>
                <div class="product-stock">${stockStatus}</div>
                
                <div class="product-description">
                    <h3>Description</h3>
                    <p>${product.description}</p>
                </div>
                
                ${product.specifications ? `
                <div class="product-specs">
                    <h3>Specifications</h3>
                    <p>${product.specifications}</p>
                </div>
                ` : ''}
                
                <div class="product-actions">
                    <div class="quantity-selector">
                        <button onclick="decreaseQuantity()">-</button>
                        <input type="number" id="quantity" value="1" min="1" max="${product.stock}" readonly>
                        <button onclick="increaseQuantity(${product.stock})">+</button>
                    </div>
                    <button 
                        class="btn btn-primary add-to-cart-large" 
                        onclick="addToCartFromDetail(${product.id}, '${product.name.replace(/'/g, "\\'")}', ${product.price}, '${product.image_url}')"
                        ${product.stock <= 0 ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}
                    >
                        <i class="fas fa-shopping-cart"></i> Add to Cart
                    </button>
                </div>
                
                <div class="product-features">
                    <div class="feature">
                        <i class="fas fa-shipping-fast"></i>
                        <div>
                            <strong>Free Shipping</strong>
                            <p>On orders over $100</p>
                        </div>
                    </div>
                    <div class="feature">
                        <i class="fas fa-undo"></i>
                        <div>
                            <strong>30-Day Returns</strong>
                            <p>Money-back guarantee</p>
                        </div>
                    </div>
                    <div class="feature">
                        <i class="fas fa-shield-alt"></i>
                        <div>
                            <strong>Secure Payment</strong>
                            <p>100% secure transactions</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function increaseQuantity(maxStock) {
    const input = document.getElementById('quantity');
    const currentValue = parseInt(input.value);
    if (currentValue < maxStock) {
        input.value = currentValue + 1;
    }
}

function decreaseQuantity() {
    const input = document.getElementById('quantity');
    const currentValue = parseInt(input.value);
    if (currentValue > 1) {
        input.value = currentValue - 1;
    }
}

function addToCartFromDetail(id, name, price, image) {
    const quantity = parseInt(document.getElementById('quantity').value);
    
    for (let i = 0; i < quantity; i++) {
        addToCart(id, name, price, image);
    }
    
    // Reset quantity to 1
    document.getElementById('quantity').value = 1;
}