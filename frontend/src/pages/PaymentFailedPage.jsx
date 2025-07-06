import React from 'react';
import { useApp } from '../context/AppContext';

function PaymentFailedPage() {
  const { startCheckout, cancelCheckout, clearError } = useApp();

  const handleRetryPayment = () => {
    clearError();
    startCheckout();
  };

  const handleCancel = () => {
    clearError();
    cancelCheckout();
  };

  return (
    <div className="page payment-failed-page">
      <div className="failure-message" data-testid="failure-message">
        <h2>❌ Payment Failed</h2>
        <p>We're sorry, but your payment could not be processed.</p>
        <p>Please check your payment information and try again.</p>
      </div>

      <div className="failure-actions">
        <button
          className="retry-payment-btn"
          data-testid="retry-payment-btn"
          onClick={handleRetryPayment}
        >
          Retry Payment
        </button>
        <button
          className="cancel-order-btn"
          data-testid="cancel-order-btn"
          onClick={handleCancel}
        >
          Cancel Order
        </button>
      </div>

      <div className="failure-help">
        <h3>Need Help?</h3>
        <p>If you continue to experience issues, please contact our support team.</p>
      </div>
    </div>
  );
}

export default PaymentFailedPage;
