import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import Header from '../components/Header.jsx'
import { useApp } from '../context/AppContext'

// Mock the useApp hook
vi.mock('../context/AppContext', () => ({
  useApp: vi.fn()
}))

describe('Header Component', () => {
  it('renders app title', () => {
    useApp.mockReturnValue({
      user: null,
      isLoggedIn: false
    })

    render(<Header />)
    
    expect(screen.getByText('Shopping App')).toBeInTheDocument()
  })

  it('displays user info when logged in', () => {
    useApp.mockReturnValue({
      user: { email: 'test@example.com' },
      isLoggedIn: true
    })

    render(<Header />)
    
    expect(screen.getByText('Welcome, test@example.com')).toBeInTheDocument()
    expect(screen.getByTestId('user-info')).toBeInTheDocument()
  })

  it('does not display user info when not logged in', () => {
    useApp.mockReturnValue({
      user: null,
      isLoggedIn: false
    })

    render(<Header />)
    
    expect(screen.queryByTestId('user-info')).not.toBeInTheDocument()
  })
})
