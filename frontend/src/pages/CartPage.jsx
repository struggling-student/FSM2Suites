import React from 'react';
import { useApp } from '../context/AppContext';

function CartPage() {
  const { 
    cart, 
    removeFromCart, 
    updateCartItem, 
    startCheckout, 
    continueShopping,
    logout 
  } = useApp();

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const handleQuantityChange = (item, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(item.id);
    } else {
      updateCartItem({ id: item.id, quantity: parseInt(newQuantity) });
    }
  };

  const handleProceedToCheckout = () => {
    if (cart.length > 0) {
      startCheckout();
    }
  };

  return (
    <div className="page cart-page">
      <div className="page-header">
        <h2 data-testid="cart-title">Shopping Cart</h2>
        <div className="page-actions">
          <button
            className="continue-shopping-btn"
            data-testid="continue-shopping-btn"
            onClick={continueShopping}
          >
            Continue Shopping
          </button>
          <button
            className="logout-btn"
            data-testid="logout-btn"
            onClick={logout}
          >
            Logout
          </button>
        </div>
      </div>

      {cart.length === 0 ? (
        <div className="empty-cart" data-testid="empty-cart">
          <p>Your cart is empty</p>
          <button
            className="browse-products-btn"
            data-testid="browse-products-btn"
            onClick={continueShopping}
          >
            Browse Products
          </button>
        </div>
      ) : (
        <div className="cart-content">
          <div className="cart-items">
            {cart.map((item) => (
              <div key={item.id} className="cart-item" data-testid={`cart-item-${item.id}`}>
                <div className="item-info">
                  <h4 className="item-name">{item.name}</h4>
                  <p className="item-price">${item.price.toFixed(2)} each</p>
                </div>
                <div className="item-controls">
                  <label htmlFor={`quantity-${item.id}`}>Quantity:</label>
                  <input
                    type="number"
                    id={`quantity-${item.id}`}
                    data-testid={`quantity-${item.id}`}
                    value={item.quantity}
                    min="0"
                    onChange={(e) => handleQuantityChange(item, e.target.value)}
                  />
                  <button
                    className="remove-item-btn"
                    data-testid={`remove-${item.id}`}
                    onClick={() => removeFromCart(item.id)}
                  >
                    Remove
                  </button>
                </div>
                <div className="item-total">
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <div className="total-price" data-testid="total-price">
              <strong>Total: ${getTotalPrice().toFixed(2)}</strong>
            </div>
            <button
              className="checkout-btn"
              data-testid="checkout-btn"
              onClick={handleProceedToCheckout}
              disabled={cart.length === 0}
            >
              Proceed to Checkout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default CartPage;
