import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Welcome from '../components/Welcome'
import { ThemeProvider } from '../context/ThemeContext'
import { QueryClient, QueryClientProvider } from 'react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
})

const renderWelcome = () => {
  return render(
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <BrowserRouter>
          <Welcome />
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

describe('Welcome', () => {
  it('renders the Welcome page with hero section', () => {
    renderWelcome()
    const heading = screen.getByText(/Smart Cat Tech/i)
    expect(heading).toBeInTheDocument()
  })

  it('displays AI powered badge', () => {
    renderWelcome()
    expect(screen.getByText(/Powered by Advanced AI/i)).toBeInTheDocument()
  })

  it('has call to action buttons', () => {
    renderWelcome()
    expect(screen.getByText(/Explore Products/i)).toBeInTheDocument()
  })

  it('shows company information', () => {
    renderWelcome()
    expect(screen.getByText(/OctoCAT Supply/i)).toBeInTheDocument()
  })
})
