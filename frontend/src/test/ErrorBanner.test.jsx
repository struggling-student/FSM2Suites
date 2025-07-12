import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import ErrorBanner from '../components/ErrorBanner.jsx'
import { useApp } from '../context/AppContext'

// Mock the useApp hook
vi.mock('../context/AppContext', () => ({
  useApp: vi.fn()
}))

describe('ErrorBanner Component', () => {
  it('renders nothing when there is no error', () => {
    useApp.mockReturnValue({
      lastError: null,
      clearError: vi.fn()
    })

    const { container } = render(<ErrorBanner />)
    
    expect(container.firstChild).toBeNull()
  })

  it('displays error message when there is an error', () => {
    const mockClearError = vi.fn()
    useApp.mockReturnValue({
      lastError: 'Something went wrong',
      clearError: mockClearError
    })

    render(<ErrorBanner />)
    
    expect(screen.getByTestId('error-banner')).toBeInTheDocument()
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
    expect(screen.getByTestId('error-close-btn')).toBeInTheDocument()
  })

  it('calls clearError when close button is clicked', () => {
    const mockClearError = vi.fn()
    useApp.mockReturnValue({
      lastError: 'Something went wrong',
      clearError: mockClearError
    })

    render(<ErrorBanner />)
    
    fireEvent.click(screen.getByTestId('error-close-btn'))
    
    expect(mockClearError).toHaveBeenCalledTimes(1)
  })
})
