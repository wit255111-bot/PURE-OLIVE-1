/**
 * PURE & OLIVE - Shopping Cart & User Experience Engine
 * Handles Cart Drawer, LocalStorage persistence, quantity updates, and Toast alerts
 */

const CART_KEY = 'pure_olive_cart';

// Get Cart from LocalStorage
function getCart() {
  try {
    const data = localStorage.getItem(CART_KEY);
    return data ? JSON.parse(data) : [];
  } catch (e) {
    console.error('Cart parse error:', e);
    return [];
  }
}

// Save Cart to LocalStorage
function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartUI();
}

// Add Item to Cart
function addToCart(item, showDrawer = true) {
  let cart = getCart();
  const existingIndex = cart.findIndex(p => p.id === item.id);

  if (existingIndex > -1) {
    cart[existingIndex].quantity += (item.quantity || 1);
  } else {
    cart.push({
      id: item.id,
      name: item.name,
      name_en: item.name_en || '',
      price: parseFloat(item.price),
      image_url: item.image_url,
      volume: item.volume || '',
      quantity: item.quantity || 1
    });
  }

  saveCart(cart);
  showToast(`เพิ่ม "${item.name}" ลงในตะกร้าแล้วค่ะ 🌿`);

  if (showDrawer) {
    openCartDrawer();
  }
}

// Add multiple items (e.g. from Routine Quiz bundle)
function addBundleToCart(items) {
  let cart = getCart();
  items.forEach(item => {
    const existingIndex = cart.findIndex(p => p.id === item.id);
    if (existingIndex > -1) {
      cart[existingIndex].quantity += 1;
    } else {
      cart.push({
        id: item.id,
        name: item.name,
        name_en: item.name_en || '',
        price: parseFloat(item.price),
        image_url: item.image_url,
        volume: item.volume || '',
        quantity: 1
      });
    }
  });

  saveCart(cart);
  showToast(`เพิ่มเซตสกินแคร์ ${items.length} รายการลงในตะกร้าแล้วค่ะ ✨`);
  openCartDrawer();
}

// Update Quantity
function updateQuantity(productId, delta) {
  let cart = getCart();
  const item = cart.find(p => p.id === productId);
  if (!item) return;

  item.quantity += delta;
  if (item.quantity <= 0) {
    cart = cart.filter(p => p.id !== productId);
    showToast('นำสินค้าออกจากตะกร้าแล้วค่ะ');
  }

  saveCart(cart);
  renderCartDrawer();
  if (typeof renderCartPage === 'function') {
    renderCartPage();
  }
}

// Remove Item
function removeFromCart(productId) {
  let cart = getCart();
  cart = cart.filter(p => p.id !== productId);
  saveCart(cart);
  showToast('ลบสินค้าออกจากตะกร้าเรียบร้อยแล้ว');
  renderCartDrawer();
  if (typeof renderCartPage === 'function') {
    renderCartPage();
  }
}

// Clear Cart
function clearCart() {
  localStorage.removeItem(CART_KEY);
  updateCartUI();
  if (typeof renderCartPage === 'function') {
    renderCartPage();
  }
}

// Update UI Badges & Drawer
function updateCartUI() {
  const cart = getCart();
  const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  // Update badge elements
  document.querySelectorAll('.cart-badge').forEach(el => {
    el.textContent = totalCount;
    el.style.display = totalCount > 0 ? 'flex' : 'none';
  });

  renderCartDrawer();
}

// Render Drawer Content
function renderCartDrawer() {
  const container = document.getElementById('cart-drawer-items');
  const totalEl = document.getElementById('cart-drawer-total');
  const countEl = document.getElementById('cart-drawer-count');
  if (!container) return;

  const cart = getCart();
  const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
  const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  if (countEl) countEl.textContent = `(${totalCount})`;
  if (totalEl) totalEl.textContent = `฿${subtotal.toLocaleString('th-TH', { minimumFractionDigits: 2 })}`;

  if (cart.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px 10px; color: var(--text-muted);">
        <div style="font-size: 2.5rem; margin-bottom: 12px;">🌿</div>
        <p style="font-size: 1rem; margin-bottom: 6px; color: var(--olive-dark); font-weight: 600;">ตะกร้าสินค้าว่างเปล่า</p>
        <p style="font-size: 0.85rem;">ค้นหาผลิตภัณฑ์เพื่อสุขภาพผิวที่ดีของคุณได้เลยค่ะ</p>
        <a href="/products" class="btn btn-primary" style="margin-top: 18px; padding: 8px 20px; font-size: 0.88rem;">เริ่มช้อปสินค้า</a>
      </div>
    `;
    return;
  }

  container.innerHTML = cart.map(item => `
    <div class="cart-item">
      <img src="${item.image_url}" alt="${item.name}" class="cart-item-img">
      <div class="cart-item-details">
        <h4 class="cart-item-title">${item.name}</h4>
        <div class="cart-item-price">฿${(item.price * item.quantity).toLocaleString('th-TH', { minimumFractionDigits: 2 })}</div>
        <div class="cart-item-qty">
          <button type="button" class="qty-btn" onclick="updateQuantity(${item.id}, -1)">-</button>
          <span style="font-size: 0.9rem; font-weight: 600; min-width: 20px; text-align: center;">${item.quantity}</span>
          <button type="button" class="qty-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
          <button type="button" onclick="removeFromCart(${item.id})" style="background:none; border:none; color: var(--text-muted); font-size: 0.78rem; margin-left: auto; cursor:pointer; text-decoration: underline;">ลบ</button>
        </div>
      </div>
    </div>
  `).join('');
}

// Drawer Visibility
function openCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-drawer-overlay');
  if (drawer && overlay) {
    drawer.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-drawer-overlay');
  if (drawer && overlay) {
    drawer.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// Toast Notifications
function showToast(message) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>🌿</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// Document Ready Setup
document.addEventListener('DOMContentLoaded', () => {
  updateCartUI();

  // Attach Cart Trigger Button
  const cartTrigger = document.getElementById('cart-trigger');
  if (cartTrigger) {
    cartTrigger.addEventListener('click', openCartDrawer);
  }

  const closeDrawerBtn = document.getElementById('close-cart-drawer');
  if (closeDrawerBtn) {
    closeDrawerBtn.addEventListener('click', closeCartDrawer);
  }

  const drawerOverlay = document.getElementById('cart-drawer-overlay');
  if (drawerOverlay) {
    drawerOverlay.addEventListener('click', closeCartDrawer);
  }
});
