import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Login from '../components/Login'
import { AuthProvider } from '../context/AuthContext'
import { ThemeProvider } from '../context/ThemeContext'

const renderLogin = () => {
  return render(
    <AuthProvider>
      <ThemeProvider>
        <BrowserRouter>
          <Login />
        </BrowserRouter>
      </ThemeProvider>
    </AuthProvider>
  )
}

describe('Login', () => {
  it('renders the login heading', () => {
    renderLogin()
    const headings = screen.getAllByText(/Login/)
    expect(headings.length).toBeGreaterThan(0)
  })

  it('has email and password labels', () => {
    renderLogin()
    expect(screen.getByText(/Email Address/i)).toBeInTheDocument()
    expect(screen.getByText(/Password/i)).toBeInTheDocument()
  })

  it('has email input field', () => {
    renderLogin()
    const emailInput = screen.getByLabelText(/Email Address/i)
    expect(emailInput).toBeInTheDocument()
  })

  it('has password input field', () => {
    renderLogin()
    const passwordInput = screen.getByLabelText(/Password/i)
    expect(passwordInput).toBeInTheDocument()
  })

  it('has a login button', () => {
    renderLogin()
    const buttons = screen.getAllByText(/Login/)
    const button = buttons.find(el => el.tagName === 'BUTTON')
    expect(button).toBeInTheDocument()
  })
})
