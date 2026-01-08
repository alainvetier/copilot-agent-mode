import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Footer from '../components/Footer'
import { ThemeProvider } from '../context/ThemeContext'

const renderFooter = () => {
  return render(
    <ThemeProvider>
      <BrowserRouter>
        <Footer />
      </BrowserRouter>
    </ThemeProvider>
  )
}

describe('Footer', () => {
  it('renders the footer', () => {
    renderFooter()
    const footer = document.querySelector('footer')
    expect(footer).toBeInTheDocument()
  })

  it('displays copyright information', () => {
    renderFooter()
    expect(screen.getByText(/Copyright ©/i)).toBeInTheDocument()
    expect(screen.getByText(/All Rights Reserved/i)).toBeInTheDocument()
  })

  it('displays company name', () => {
    renderFooter()
    const elements = screen.getAllByText(/OctoCAT Supply/i)
    expect(elements.length).toBeGreaterThan(0)
  })
})
