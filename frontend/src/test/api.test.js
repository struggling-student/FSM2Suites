import { describe, it, expect, vi, beforeEach } from 'vitest'
import apiService from '../services/api.js'

// Mock fetch globally
global.fetch = vi.fn()

describe('ApiService', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  describe('login', () => {
    it('should call login endpoint with correct data', async () => {
      const mockResponse = { success: true, sessionId: 'test123' }
      fetch.mockResolvedValueOnce({
        json: async () => mockResponse,
      })

      const result = await apiService.login('test@example.com', 'password')

      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: 'test@example.com', password: 'password' }),
      })
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getProducts', () => {
    it('should fetch products from API', async () => {
      const mockProducts = [
        { id: 1, name: 'Test Product', price: 100 }
      ]
      fetch.mockResolvedValueOnce({
        json: async () => mockProducts,
      })

      const result = await apiService.getProducts()

      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/products')
      expect(result).toEqual(mockProducts)
    })
  })

  describe('addToCart', () => {
    it('should add item to cart with correct data', async () => {
      const mockResponse = { success: true }
      fetch.mockResolvedValueOnce({
        json: async () => mockResponse,
      })

      const result = await apiService.addToCart(1, 2)

      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/cart/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: 1, quantity: 2 }),
      })
      expect(result).toEqual(mockResponse)
    })
  })

  describe('removeFromCart', () => {
    it('should remove item from cart', async () => {
      const mockResponse = { success: true }
      fetch.mockResolvedValueOnce({
        json: async () => mockResponse,
      })

      const result = await apiService.removeFromCart(1)

      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/cart/remove', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: 1 }),
      })
      expect(result).toEqual(mockResponse)
    })
  })
})
