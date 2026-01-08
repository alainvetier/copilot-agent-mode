import { describe, it, expect, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { ThemeProvider, useTheme } from '../context/ThemeContext'

describe('ThemeContext', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
    // Clear document classes
    document.documentElement.classList.remove('dark', 'light')
  })

  it('provides initial theme state from localStorage', () => {
    localStorage.setItem('theme', 'dark')
    
    const { result } = renderHook(() => useTheme(), {
      wrapper: ThemeProvider,
    })

    expect(result.current.darkMode).toBe(true)
  })

  it('defaults to light mode when no theme in localStorage', () => {
    const { result } = renderHook(() => useTheme(), {
      wrapper: ThemeProvider,
    })

    expect(result.current.darkMode).toBe(false)
  })

  it('toggles theme from light to dark', () => {
    const { result } = renderHook(() => useTheme(), {
      wrapper: ThemeProvider,
    })

    expect(result.current.darkMode).toBe(false)

    act(() => {
      result.current.toggleTheme()
    })

    expect(result.current.darkMode).toBe(true)
    expect(localStorage.getItem('theme')).toBe('dark')
  })

  it('toggles theme from dark to light', () => {
    localStorage.setItem('theme', 'dark')
    
    const { result } = renderHook(() => useTheme(), {
      wrapper: ThemeProvider,
    })

    expect(result.current.darkMode).toBe(true)

    act(() => {
      result.current.toggleTheme()
    })

    expect(result.current.darkMode).toBe(false)
    expect(localStorage.getItem('theme')).toBe('light')
  })

  it('adds dark class to document when dark mode is enabled', () => {
    const { result } = renderHook(() => useTheme(), {
      wrapper: ThemeProvider,
    })

    act(() => {
      result.current.toggleTheme()
    })

    expect(document.documentElement.classList.contains('dark')).toBe(true)
    expect(document.documentElement.classList.contains('light')).toBe(false)
  })

  it('adds light class to document when light mode is enabled', () => {
    localStorage.setItem('theme', 'dark')
    
    const { result } = renderHook(() => useTheme(), {
      wrapper: ThemeProvider,
    })

    act(() => {
      result.current.toggleTheme()
    })

    expect(document.documentElement.classList.contains('light')).toBe(true)
    expect(document.documentElement.classList.contains('dark')).toBe(false)
  })

  it('throws error when useTheme is used outside ThemeProvider', () => {
    expect(() => {
      renderHook(() => useTheme())
    }).toThrow('useTheme must be used within a ThemeProvider')
  })
})
