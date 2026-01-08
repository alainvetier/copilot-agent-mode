import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import About from '../components/About'
import { ThemeProvider } from '../context/ThemeContext'

const renderAbout = () => {
  return render(
    <ThemeProvider>
      <BrowserRouter>
        <About />
      </BrowserRouter>
    </ThemeProvider>
  )
}

describe('About', () => {
  it('renders the About page', () => {
    renderAbout()
    expect(screen.getByText(/About OctoCAT Supply/i)).toBeInTheDocument()
  })

  it('displays the mission section', () => {
    renderAbout()
    expect(screen.getByText(/Our Meow-ssion/i)).toBeInTheDocument()
  })

  it('displays the purpose section', () => {
    renderAbout()
    expect(screen.getByText(/Our Purr-pose/i)).toBeInTheDocument()
  })

  it('displays information about products', () => {
    renderAbout()
    expect(screen.getByText(/Key Features of Our Products/i)).toBeInTheDocument()
  })

  it('describes the company mission', () => {
    renderAbout()
    expect(screen.getByText(/revolutionize the way cats and humans interact/i)).toBeInTheDocument()
  })
})
