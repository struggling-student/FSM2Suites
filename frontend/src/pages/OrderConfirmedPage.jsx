import React from 'react';
import { useApp } from '../context/AppContext';

function OrderConfirmedPage() {
  const { orderSummary, continueShopping, logout } = useApp();

  if (!orderSummary) {
    return (
      <div className="page order-confirmed-page">
        <div className="error-message" data-testid="no-order-error">
          No order information available.
        </div>
      </div>
    );
  }

  return (
    <div className="page order-confirmed-page">
      <div className="success-message" data-testid="success-message">
        <h2>🎉 Order Confirmed!</h2>
        <p>Thank you for your purchase!</p>
      </div>

      <div className="order-details">
        <h3>Order Details</h3>
        <div className="order-info">
          <p><strong>Order ID:</strong> <span data-testid="order-id">{orderSummary.orderId}</span></p>
          <p><strong>Order Date:</strong> <span data-testid="order-date">{orderSummary.orderDate}</span></p>
          <p><strong>Total:</strong> <span data-testid="order-total">${orderSummary.total.toFixed(2)}</span></p>
        </div>

        <div className="ordered-items">
          <h4>Items Ordered:</h4>
          {orderSummary.items.map((item) => (
            <div key={item.id} className="ordered-item" data-testid={`ordered-item-${item.id}`}>
              <span className="item-name">{item.name}</span>
              <span className="item-quantity">x{item.quantity}</span>
              <span className="item-price">${(item.price * item.quantity).toFixed(2)}</span>
            </div>
          ))}
        </div>

        <div className="shipping-details">
          <h4>Shipping Address:</h4>
          <div className="shipping-info" data-testid="shipping-info">
            <p>{orderSummary.shippingInfo.address}</p>
            <p>{orderSummary.shippingInfo.city}, {orderSummary.shippingInfo.zipCode}</p>
            <p>{orderSummary.shippingInfo.country}</p>
          </div>
        </div>
      </div>

      <div className="order-actions">
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
  );
}

export default OrderConfirmedPage;
