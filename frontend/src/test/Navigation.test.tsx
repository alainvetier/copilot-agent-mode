import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Navigation from '../components/Navigation'
import { AuthProvider } from '../context/AuthContext'
import { ThemeProvider } from '../context/ThemeContext'

const renderNavigation = () => {
  return render(
    <AuthProvider>
      <ThemeProvider>
        <BrowserRouter>
          <Navigation />
        </BrowserRouter>
      </ThemeProvider>
    </AuthProvider>
  )
}

describe('Navigation', () => {
  it('renders the logo and brand name', () => {
    renderNavigation()
    expect(screen.getByText('OctoCAT Supply')).toBeInTheDocument()
    expect(screen.getByText('Smart Cat Tech, Powered by AI')).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    renderNavigation()
    expect(screen.getByText('Home')).toBeInTheDocument()
    expect(screen.getByText('Products')).toBeInTheDocument()
    expect(screen.getByText('About us')).toBeInTheDocument()
  })

  it('shows login button when not logged in', () => {
    renderNavigation()
    expect(screen.getByText('Login')).toBeInTheDocument()
  })

  it('has a theme toggle button', () => {
    renderNavigation()
    const themeButton = screen.getByLabelText('Toggle dark/light mode')
    expect(themeButton).toBeInTheDocument()
  })

  it('toggles theme when theme button is clicked', () => {
    renderNavigation()
    const themeButton = screen.getByLabelText('Toggle dark/light mode')
    
    // Initial state should have light theme class
    expect(document.documentElement.classList.contains('light')).toBe(true)
    
    // Click to toggle to dark
    fireEvent.click(themeButton)
    expect(document.documentElement.classList.contains('dark')).toBe(true)
    
    // Click to toggle back to light
    fireEvent.click(themeButton)
    expect(document.documentElement.classList.contains('light')).toBe(true)
  })
})
