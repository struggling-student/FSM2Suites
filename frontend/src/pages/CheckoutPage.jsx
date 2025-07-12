import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import ApiService from '../services/api';

function CheckoutPage() {
  const { 
    cart, 
    paymentSuccess, 
    paymentFailed, 
    cancelCheckout,
    logout,
    setError 
  } = useApp();
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [shippingInfo, setShippingInfo] = useState({
    address: '',
    city: '',
    zipCode: '',
    country: ''
  });

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const handleInputChange = (field, value) => {
    setShippingInfo(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePayment = async (forceSuccess = true) => {
    setIsProcessing(true);
    
    try {
      const result = await ApiService.processPayment(forceSuccess);
      
      if (result.success) {
        const orderSummary = {
          orderId: result.orderId || 'ORD' + Date.now(),
          items: [...cart],
          total: getTotalPrice(),
          shippingInfo: { ...shippingInfo },
          orderDate: new Date().toLocaleString()
        };
        paymentSuccess(orderSummary);
      } else {
        paymentFailed();
      }
    } catch (error) {
      setError('Payment processing failed. Please try again.');
      paymentFailed();
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCancel = () => {
    cancelCheckout();
  };

  return (
    <div className="page checkout-page">
      <div className="page-header">
        <h2 data-testid="checkout-title">Checkout</h2>
      </div>

      <div className="checkout-content">
        <div className="order-summary">
          <h3>Order Summary</h3>
          <div className="order-items">
            {cart.map((item) => (
              <div key={item.id} className="order-item" data-testid={`order-item-${item.id}`}>
                <span className="item-name">{item.name}</span>
                <span className="item-quantity">x{item.quantity}</span>
                <span className="item-price">${(item.price * item.quantity).toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="order-total" data-testid="order-total">
            <strong>Total: ${getTotalPrice().toFixed(2)}</strong>
          </div>
        </div>

        <div className="shipping-form">
          <h3>Shipping Information</h3>
          <div className="form-group">
            <label htmlFor="address">Address:</label>
            <input
              type="text"
              id="address"
              data-testid="address-input"
              value={shippingInfo.address}
              onChange={(e) => handleInputChange('address', e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="city">City:</label>
            <input
              type="text"
              id="city"
              data-testid="city-input"
              value={shippingInfo.city}
              onChange={(e) => handleInputChange('city', e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="zipCode">ZIP Code:</label>
            <input
              type="text"
              id="zipCode"
              data-testid="zipcode-input"
              value={shippingInfo.zipCode}
              onChange={(e) => handleInputChange('zipCode', e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="country">Country:</label>
            <input
              type="text"
              id="country"
              data-testid="country-input"
              value={shippingInfo.country}
              onChange={(e) => handleInputChange('country', e.target.value)}
              required
            />
          </div>
        </div>

        <div className="payment-section">
          <h3>Payment</h3>
          <div className="payment-buttons">
            <button
              className="pay-success-btn"
              data-testid="pay-success-btn"
              onClick={() => handlePayment(true)}
              disabled={isProcessing}
            >
              {isProcessing ? 'Processing...' : 'Pay Now (Success)'}
            </button>
            <button
              className="pay-fail-btn"
              data-testid="pay-fail-btn"
              onClick={() => handlePayment(false)}
              disabled={isProcessing}
            >
              {isProcessing ? 'Processing...' : 'Pay Now (Fail)'}
            </button>
            <button
              className="cancel-checkout-btn"
              data-testid="cancel-checkout-btn"
              onClick={handleCancel}
              disabled={isProcessing}
            >
              Cancel
            </button>
            <button
              className="logout-btn"
              data-testid="logout-btn"
              onClick={logout}
              disabled={isProcessing}
            >
              Logout
            </button>
          </div>
          <p className="payment-note">
            Use "Pay Now (Success)" for successful payment or "Pay Now (Fail)" to simulate payment failure.
          </p>
        </div>
      </div>
    </div>
  );
}

export default CheckoutPage;
