import React from 'react';
import { useApp, APP_STATES } from '../context/AppContext';

function SessionEndedPage() {
  const { loginSuccess } = useApp();

  const handleBackToLogin = () => {
    // Reset to login state
    window.location.reload();
  };

  return (
    <div className="page session-ended-page">
      <div className="session-ended-content">
        <h2 data-testid="session-ended-title">Session Ended</h2>
        <p data-testid="session-ended-message">
          You have been successfully logged out.
        </p>
        <p>Thank you for using our shopping app!</p>
        
        <button
          className="back-to-login-btn"
          data-testid="back-to-login-btn"
          onClick={handleBackToLogin}
        >
          Back to Login
        </button>
      </div>
    </div>
  );
}

export default SessionEndedPage;
