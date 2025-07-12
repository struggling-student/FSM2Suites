import { describe, it, expect } from 'vitest'
import { APP_STATES } from '../context/AppContext'

describe('AppContext Constants', () => {
  it('should have all required FSM states', () => {
    expect(APP_STATES.LOGIN).toBe('Login')
    expect(APP_STATES.LOGIN_FAILED).toBe('LoginFailed')
    expect(APP_STATES.BROWSING).toBe('Browsing')
    expect(APP_STATES.CART_EDITING).toBe('CartEditing')
    expect(APP_STATES.CHECKOUT).toBe('Checkout')
    expect(APP_STATES.ORDER_CONFIRMED).toBe('OrderConfirmed')
    expect(APP_STATES.SESSION_ENDED).toBe('SessionEnded')
    expect(APP_STATES.PAYMENT_FAILED).toBe('PaymentFailed')
  })

  it('should have 8 total states', () => {
    const stateValues = Object.values(APP_STATES)
    expect(stateValues).toHaveLength(8)
  })
})
