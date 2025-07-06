import React from 'react';
import { useApp } from '../context/AppContext';

function Header() {
  const { user, isLoggedIn } = useApp();

  return (
    <header className="header">
      <div className="header-content">
        <h1 className="app-title">Shopping App</h1>
        {isLoggedIn && user && (
          <div className="user-info" data-testid="user-info">
            Welcome, {user.email}
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
