import React from 'react'
import { AppProvider, useApp, APP_STATES } from './context/AppContext'
import Header from './components/Header'
import ErrorBanner from './components/ErrorBanner'
import LoginPage from './pages/LoginPage'
import ProductCatalogPage from './pages/ProductCatalogPage'
import CartPage from './pages/CartPage'
import CheckoutPage from './pages/CheckoutPage'
import OrderConfirmedPage from './pages/OrderConfirmedPage'
import PaymentFailedPage from './pages/PaymentFailedPage'
import SessionEndedPage from './pages/SessionEndedPage'
import './App.css'

function AppContent() {
  const { currentState } = useApp();

  const renderCurrentPage = () => {
    switch (currentState) {
      case APP_STATES.LOGIN:
        return <LoginPage />;
      case APP_STATES.BROWSING:
        return <ProductCatalogPage />;
      case APP_STATES.CART_EDITING:
        return <CartPage />;
      case APP_STATES.CHECKOUT:
        return <CheckoutPage />;
      case APP_STATES.ORDER_CONFIRMED:
        return <OrderConfirmedPage />;
      case APP_STATES.PAYMENT_FAILED:
        return <PaymentFailedPage />;
      case APP_STATES.SESSION_ENDED:
        return <SessionEndedPage />;
      default:
        return <LoginPage />;
    }
  };

  return (
    <div className="app" data-testid="app">
      <Header />
      <ErrorBanner />
      <main className="main-content">
        {renderCurrentPage()}
      </main>
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App
