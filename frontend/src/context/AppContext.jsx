import React, { createContext, useContext, useReducer } from 'react';
import ApiService from '../services/api';

// FSM States
export const APP_STATES = {
  LOGIN: 'Login',
  LOGIN_FAILED: 'LoginFailed',
  BROWSING: 'Browsing',
  CART_EDITING: 'CartEditing',
  CHECKOUT: 'Checkout',
  ORDER_CONFIRMED: 'OrderConfirmed',
  SESSION_ENDED: 'SessionEnded',
  PAYMENT_FAILED: 'PaymentFailed'
};

// Initial state
const initialState = {
  currentState: APP_STATES.LOGIN,
  user: null,
  products: [],
  cart: [],
  isLoggedIn: false,
  lastError: null,
  orderSummary: null
};

// Actions
const ACTIONS = {
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILED: 'LOGIN_FAILED',
  RETRY_LOGIN: 'RETRY_LOGIN',
  EXIT_APPLICATION: 'EXIT_APPLICATION',
  LOGOUT: 'LOGOUT',
  SET_PRODUCTS: 'SET_PRODUCTS',
  ADD_TO_CART: 'ADD_TO_CART',
  REMOVE_FROM_CART: 'REMOVE_FROM_CART',
  UPDATE_CART_ITEM: 'UPDATE_CART_ITEM',
  START_CHECKOUT: 'START_CHECKOUT',
  PAYMENT_SUCCESS: 'PAYMENT_SUCCESS',
  PAYMENT_FAILED: 'PAYMENT_FAILED',
  CANCEL_CHECKOUT: 'CANCEL_CHECKOUT',
  CONTINUE_SHOPPING: 'CONTINUE_SHOPPING',
  VIEW_CART: 'VIEW_CART',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR'
};

// Reducer
function appReducer(state, action) {
  switch (action.type) {
    case ACTIONS.LOGIN_SUCCESS:
      return {
        ...state,
        currentState: APP_STATES.BROWSING,
        user: action.payload,
        isLoggedIn: true,
        lastError: null
      };
    
    case ACTIONS.LOGIN_FAILED:
      return {
        ...state,
        currentState: APP_STATES.LOGIN_FAILED,
        lastError: action.payload || 'Invalid email or password'
      };
    
    case ACTIONS.RETRY_LOGIN:
      return {
        ...state,
        currentState: APP_STATES.LOGIN,
        lastError: null
      };
    
    case ACTIONS.EXIT_APPLICATION:
      return {
        ...state,
        currentState: APP_STATES.SESSION_ENDED,
        lastError: null
      };
    
    case ACTIONS.LOGOUT:
      return {
        ...initialState,
        currentState: APP_STATES.SESSION_ENDED
      };
    
    case ACTIONS.SET_PRODUCTS:
      return {
        ...state,
        products: action.payload
      };
    
    case ACTIONS.ADD_TO_CART:
      const existingItem = state.cart.find(item => item.id === action.payload.id);
      if (existingItem) {
        return {
          ...state,
          currentState: APP_STATES.CART_EDITING,
          cart: state.cart.map(item =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + action.payload.quantity }
              : item
          )
        };
      } else {
        return {
          ...state,
          currentState: APP_STATES.CART_EDITING,
          cart: [...state.cart, action.payload]
        };
      }
    
    case ACTIONS.REMOVE_FROM_CART:
      return {
        ...state,
        cart: state.cart.filter(item => item.id !== action.payload),
        currentState: state.cart.length <= 1 ? APP_STATES.BROWSING : APP_STATES.CART_EDITING
      };
    
    case ACTIONS.UPDATE_CART_ITEM:
      return {
        ...state,
        currentState: APP_STATES.CART_EDITING,
        cart: state.cart.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ).filter(item => item.quantity > 0)
      };
    
    case ACTIONS.START_CHECKOUT:
      return {
        ...state,
        currentState: APP_STATES.CHECKOUT
      };
    
    case ACTIONS.PAYMENT_SUCCESS:
      return {
        ...state,
        currentState: APP_STATES.ORDER_CONFIRMED,
        orderSummary: action.payload,
        cart: []
      };
    
    case ACTIONS.PAYMENT_FAILED:
      return {
        ...state,
        currentState: APP_STATES.PAYMENT_FAILED,
        lastError: 'Payment failed. Please try again.'
      };
    
    case ACTIONS.CANCEL_CHECKOUT:
      return {
        ...state,
        currentState: state.cart.length > 0 ? APP_STATES.CART_EDITING : APP_STATES.BROWSING
      };
    
    case ACTIONS.CONTINUE_SHOPPING:
      return {
        ...state,
        currentState: APP_STATES.BROWSING,
        orderSummary: null,
        lastError: null
      };
    
    case ACTIONS.VIEW_CART:
      return {
        ...state,
        currentState: state.cart.length > 0 ? APP_STATES.CART_EDITING : APP_STATES.BROWSING
      };
    
    case ACTIONS.SET_ERROR:
      return {
        ...state,
        lastError: action.payload
      };
    
    case ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        lastError: null
      };
    
    default:
      return state;
  }
}

// Context
const AppContext = createContext();

// Provider component
export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  const actions = {
    loginSuccess: (user) => dispatch({ type: ACTIONS.LOGIN_SUCCESS, payload: user }),
    loginFailed: (error) => dispatch({ type: ACTIONS.LOGIN_FAILED, payload: error }),
    retryLogin: () => dispatch({ type: ACTIONS.RETRY_LOGIN }),
    exitApplication: () => dispatch({ type: ACTIONS.EXIT_APPLICATION }),
    logout: () => dispatch({ type: ACTIONS.LOGOUT }),
    setProducts: (products) => dispatch({ type: ACTIONS.SET_PRODUCTS, payload: products }),
    addToCart: async (product) => {
      try {
        // Call backend API first
        await ApiService.addToCart(product.id, product.quantity || 1);
        // Then update local state
        dispatch({ type: ACTIONS.ADD_TO_CART, payload: product });
      } catch (error) {
        console.error('Failed to add to cart:', error);
        dispatch({ type: ACTIONS.SET_ERROR, payload: 'Failed to add item to cart' });
      }
    },
    removeFromCart: async (productId) => {
      try {
        // Call backend API first
        await ApiService.removeFromCart(productId);
        // Then update local state
        dispatch({ type: ACTIONS.REMOVE_FROM_CART, payload: productId });
      } catch (error) {
        console.error('Failed to remove from cart:', error);
        dispatch({ type: ACTIONS.SET_ERROR, payload: 'Failed to remove item from cart' });
      }
    },
    updateCartItem: async (item) => {
      try {
        // Call backend API first
        await ApiService.updateCart(item.id, item.quantity);
        // Then update local state
        dispatch({ type: ACTIONS.UPDATE_CART_ITEM, payload: item });
      } catch (error) {
        console.error('Failed to update cart:', error);
        dispatch({ type: ACTIONS.SET_ERROR, payload: 'Failed to update cart' });
      }
    },
    startCheckout: async () => {
      try {
        await ApiService.startCheckout();
        dispatch({ type: ACTIONS.START_CHECKOUT });
      } catch (error) {
        console.error('Failed to start checkout:', error);
        dispatch({ type: ACTIONS.SET_ERROR, payload: 'Failed to start checkout' });
      }
    },
    paymentSuccess: (orderSummary) => dispatch({ type: ACTIONS.PAYMENT_SUCCESS, payload: orderSummary }),
    paymentFailed: () => dispatch({ type: ACTIONS.PAYMENT_FAILED }),
    cancelCheckout: () => dispatch({ type: ACTIONS.CANCEL_CHECKOUT }),
    continueShopping: () => dispatch({ type: ACTIONS.CONTINUE_SHOPPING }),
    viewCart: () => dispatch({ type: ACTIONS.VIEW_CART }),
    setError: (error) => dispatch({ type: ACTIONS.SET_ERROR, payload: error }),
    clearError: () => dispatch({ type: ACTIONS.CLEAR_ERROR })
  };

  return (
    <AppContext.Provider value={{ ...state, ...actions }}>
      {children}
    </AppContext.Provider>
  );
}

// Hook to use the context
export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
