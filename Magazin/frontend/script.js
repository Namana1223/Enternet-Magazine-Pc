// Sistem de coș de cumpărături cu localStorage
class ShoppingCart {
    constructor() {
        this.cart = this.loadCart();
        this.updateCartDisplay();
    }

    // Încarcă coșul din localStorage
    loadCart() {
        const savedCart = localStorage.getItem('shoppingCart');
        return savedCart ? JSON.parse(savedCart) : [];
    }

    // Salvează coșul în localStorage
    saveCart() {
        localStorage.setItem('shoppingCart', JSON.stringify(this.cart));
        this.updateCartDisplay();
    }

    // Adaugă produs în coș
    addToCart(product) {
        const existingItem = this.cart.find(item => item.name === product.name);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.cart.push({
                ...product,
                quantity: 1
            });
        }
        
        this.saveCart();
        this.showNotification('produs adaugat in cos', 'success');
    }

    // Șterge produs din coș
    removeFromCart(productName) {
        this.cart = this.cart.filter(item => item.name !== productName);
        this.saveCart();
        this.showNotification('Produs șters din coș!', 'info');
    }

    // Actualizează cantitatea
    updateQuantity(productName, newQuantity) {
        const item = this.cart.find(item => item.name === productName);
        if (item) {
            if (newQuantity <= 0) {
                this.removeFromCart(productName);
            } else {
                item.quantity = newQuantity;
                this.saveCart();
            }
        }
    }

    // Calculează totalul coșului
    getTotal() {
        return this.cart.reduce((total, item) => {
            const price = parseFloat(item.price.replace(/[^\d.]/g, ''));
            return total + (price * item.quantity);
        }, 0);
    }

    // Golește coșul
    clearCart() {
        this.cart = [];
        this.saveCart();
        this.showNotification('Coșul a fost golit!', 'info');
    }

    // Actualizează afișarea coșului în navbar
    updateCartDisplay() {
        const cartCount = document.getElementById('cartCount');
        if (cartCount) {
            const totalItems = this.cart.reduce((sum, item) => sum + item.quantity, 0);
            cartCount.textContent = totalItems;
            
            if (totalItems > 0) {
                cartCount.style.display = 'flex';
                // Adaugă efect de bounce când se schimbă numărul
                cartCount.style.animation = 'none';
                setTimeout(() => {
                    cartCount.style.animation = 'pulse 2s infinite';
                }, 10);
            } else {
                cartCount.style.display = 'none';
            }
        }
    }

    // Afișează notificări avansate
    showNotification(message, type = 'info', title = null) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        const icons = {
            success: '🎉',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        const titles = {
            success: 'Succes!',
            error: 'Eroare!',
            warning: 'Atenție!',
            info: 'Informație'
        };
        
        notification.innerHTML = `
            <div class="notification-icon">${icons[type]}</div>
            <div class="notification-content">
                <div class="notification-title">${title || titles[type]}</div>
                <div class="notification-message">${message}</div>
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">×</button>
            <div class="notification-progress"></div>
        `;
        
        // Adaugă la container sau creează unul nou
        let container = document.querySelector('.notification-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'notification-container';
            document.body.appendChild(container);
        }
        
        container.appendChild(notification);
        
        // Efect de bounce la apariție
        setTimeout(() => {
            notification.style.animation = 'bounce 0.6s ease-out';
        }, 100);
        
        // Șterge notificarea după 5 secunde
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideInFromRight 0.4s ease-out reverse';
                setTimeout(() => notification.remove(), 400);
            }
        }, 5000);
    }
    
    // Verifică dacă utilizatorul este autentificat
    isAuthenticated() {
        const user = JSON.parse(localStorage.getItem('user') || 'null');
        return user !== null;
    }
    
    // Deconectare
    logout() {
        localStorage.removeItem('user');
        this.cart = [];
        this.saveCart();
        this.updateCartDisplay();
    }
}

// Inițializează coșul global
const cart = new ShoppingCart();

// Funcții pentru adăugarea produselor în coș
function addToCartFromCatalog(productName, productImage, productPrice) {
    cart.addToCart({
        name: productName,
        image: productImage,
        price: productPrice
    });
}

function addToCartFromCategory(productName, productImage, productPrice) {
    cart.addToCart({
        name: productName,
        image: productImage,
        price: productPrice
    });
}

// Funcție pentru afișarea coșului
function displayCart() {
    const cartContainer = document.getElementById('cartItems');
    if (!cartContainer) return;
    
    if (cart.cart.length === 0) {
        cartContainer.innerHTML = `
            <div class="empty-cart">
                <h2>Coșul tău este gol</h2>
                <p>Nu ai adăugat încă niciun produs în coșul de cumpărături.</p>
                <a href="cartonase.html">Vezi produsele disponibile</a>
            </div>
        `;
    } else {
        cartContainer.innerHTML = cart.cart.map(item => `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}" onerror="this.style.display='none'">
                <div class="cart-item-info">
                    <h3>${item.name}</h3>
                    <p>Preț: ${item.price}</p>
                    <div class="quantity-controls">
                        <button onclick="updateItemQuantity('${item.name}', ${item.quantity - 1})">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="updateItemQuantity('${item.name}', ${item.quantity + 1})">+</button>
                    </div>
                </div>
                <button onclick="removeFromCart('${item.name}')">Șterge</button>
            </div>
        `).join('');
        
        // Adaugă totalul
        cartContainer.innerHTML += `
            <div class="cart-total">
                <h3>Total: ${cart.getTotal().toFixed(2)} MDL</h3>
                <button onclick="proceedToCheckout()" class="checkout-btn">Continuă către plată</button>
            </div>
        `;
    }
}

// Funcții helper pentru coș
function removeFromCart(productName) {
    cart.removeFromCart(productName);
    displayCart();
}

function updateItemQuantity(productName, newQuantity) {
    cart.updateQuantity(productName, newQuantity);
    displayCart();
}

function proceedToCheckout() {
    if (cart.cart.length > 0) {
        window.location.href = 'checkout.html';
    }
}

// Inițializează coșul când se încarcă pagina
document.addEventListener('DOMContentLoaded', function() {
    // Efect de scroll pentru navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    });
    
    // Lazy loading pentru imagini
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('skeleton');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Smooth scroll pentru link-uri interne
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    // Adaugă indicator de coș în navbar dacă există
    const navbar = document.querySelector('.navbar ul');
    if (navbar) {
        const cartLink = navbar.querySelector('a[href="cart.html"]');
        if (cartLink) {
            // Creează un container pentru link și indicator
            const cartContainer = document.createElement('div');
            cartContainer.style.cssText = `
                position: relative;
                display: inline-block;
            `;
            
            // Mută link-ul în container
            cartContainer.appendChild(cartLink.cloneNode(true));
            
            // Creează indicatorul elegant
            const cartBadge = document.createElement('span');
            cartBadge.id = 'cartCount';
            cartBadge.style.cssText = `
                position: absolute;
                top: -8px;
                right: -8px;
                background: linear-gradient(135deg, #e74c3c, #c0392b);
                color: white;
                border-radius: 12px;
                min-width: 18px;
                height: 18px;
                display: none;
                align-items: center;
                justify-content: center;
                font-size: 10px;
                font-weight: 700;
                box-shadow: 0 2px 8px rgba(231, 76, 60, 0.4);
                border: 2px solid white;
                animation: pulse 2s infinite;
                z-index: 10;
                padding: 0 4px;
                box-sizing: border-box;
            `;
            
            cartContainer.appendChild(cartBadge);
            
            // Înlocuiește link-ul original cu containerul
            cartLink.parentNode.replaceChild(cartContainer, cartLink);
        }
    }
    
    // Actualizează afișarea coșului
    cart.updateCartDisplay();
    
    // Afișează coșul dacă suntem pe pagina de coș
    if (window.location.pathname.includes('cart.html')) {
        displayCart();
    }
    
    
    // Funcționalitate pentru Back to Top
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Adaugă efecte de hover pentru produse
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-12px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});
