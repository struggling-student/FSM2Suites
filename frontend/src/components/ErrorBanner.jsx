import React from 'react';
import { useApp } from '../context/AppContext';

function ErrorBanner() {
  const { lastError, clearError } = useApp();

  if (!lastError) {
    return null;
  }

  return (
    <div className="error-banner" data-testid="error-banner">
      <span className="error-message">{lastError}</span>
      <button 
        className="error-close-btn" 
        data-testid="error-close-btn"
        onClick={clearError}
      >
        ×
      </button>
    </div>
  );
}

export default ErrorBanner;
