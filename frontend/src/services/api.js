const API_BASE_URL = 'http://localhost:8000';

class ApiService {
  async login(email, password) {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    return response.json();
  }

  async logout() {
    const response = await fetch(`${API_BASE_URL}/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  }

  async getProducts() {
    const response = await fetch(`${API_BASE_URL}/products`);
    return response.json();
  }

  async addToCart(productId, quantity) {
    const response = await fetch(`${API_BASE_URL}/cart/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: productId, quantity }),
    });
    return response.json();
  }

  async removeFromCart(productId) {
    const response = await fetch(`${API_BASE_URL}/cart/remove`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: productId }),
    });
    return response.json();
  }

  async updateCart(productId, quantity) {
    const response = await fetch(`${API_BASE_URL}/cart/update`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: productId, quantity }),
    });
    return response.json();
  }

  async getCart() {
    const response = await fetch(`${API_BASE_URL}/cart`);
    return response.json();
  }

  async startCheckout() {
    const response = await fetch(`${API_BASE_URL}/checkout/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  }

  async processPayment(forceSuccess = true) {
    const response = await fetch(`${API_BASE_URL}/checkout/pay`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ forceSuccess }),
    });
    return response.json();
  }

  async cancelCheckout() {
    const response = await fetch(`${API_BASE_URL}/checkout/cancel`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  }
}

export default new ApiService();
