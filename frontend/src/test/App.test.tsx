import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />)
    expect(document.querySelector('main')).toBeInTheDocument()
  })

  it('renders navigation component', () => {
    render(<App />)
    expect(document.querySelector('nav')).toBeInTheDocument()
  })

  it('renders footer component', () => {
    render(<App />)
    expect(document.querySelector('footer')).toBeInTheDocument()
  })
})
