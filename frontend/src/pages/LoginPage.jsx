import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import ApiService from '../services/api';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { loginSuccess, loginFailed } = useApp();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const result = await ApiService.login(email, password);
      if (result.success) {
        loginSuccess({ email, token: result.token });
      } else {
        loginFailed(result.message || 'Login failed');
      }
    } catch (error) {
      loginFailed('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page login-page">
      <div className="login-container">
        <h2 data-testid="login-title">Login to Shopping App</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              data-testid="email-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              data-testid="password-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="login-btn"
            data-testid="login-btn"
            disabled={isLoading}
          >
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <div className="demo-credentials" data-testid="demo-credentials">
          <p><strong>Demo credentials:</strong></p>
          <p>Email: test@example.com</p>
          <p>Password: password123</p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
