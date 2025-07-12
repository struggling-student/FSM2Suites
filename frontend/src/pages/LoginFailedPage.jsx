import React from 'react';
import { useApp } from '../context/AppContext';

function LoginFailedPage() {
  const { lastError, retryLogin, exitApplication } = useApp();

  return (
    <div className="page login-failed-page">
      <div className="login-failed-container">
        <h2 data-testid="login-failed-title">❌ Login Failed</h2>
        <div className="error-message" data-testid="login-failed-message">
          {lastError || 'Invalid email or password'}
        </div>
        
        <div className="login-failed-actions">
          <button
            className="retry-login-btn"
            data-testid="retry-login-btn"
            onClick={retryLogin}
          >
            Try Login Again
          </button>
          <button
            className="exit-app-btn"
            data-testid="exit-app-btn"
            onClick={exitApplication}
          >
            Exit Application
          </button>
        </div>

        <div className="demo-credentials" data-testid="demo-credentials">
          <p><strong>Reminder - Demo credentials:</strong></p>
          <p>Email: test@example.com</p>
          <p>Password: password123</p>
        </div>
      </div>
    </div>
  );
}

export default LoginFailedPage;
