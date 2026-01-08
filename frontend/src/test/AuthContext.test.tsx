import { describe, it, expect } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { AuthProvider, useAuth } from '../context/AuthContext'

describe('AuthContext', () => {
  it('provides initial auth state', () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: AuthProvider,
    })

    expect(result.current.isLoggedIn).toBe(false)
    expect(result.current.isAdmin).toBe(false)
  })

  it('logs in user successfully', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: AuthProvider,
    })

    await act(async () => {
      await result.current.login('user@example.com', 'password')
    })

    expect(result.current.isLoggedIn).toBe(true)
    expect(result.current.isAdmin).toBe(false)
  })

  it('logs in admin user successfully', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: AuthProvider,
    })

    await act(async () => {
      await result.current.login('admin@github.com', 'password')
    })

    expect(result.current.isLoggedIn).toBe(true)
    expect(result.current.isAdmin).toBe(true)
  })

  it('logs out user successfully', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: AuthProvider,
    })

    await act(async () => {
      await result.current.login('user@example.com', 'password')
    })

    expect(result.current.isLoggedIn).toBe(true)

    act(() => {
      result.current.logout()
    })

    expect(result.current.isLoggedIn).toBe(false)
    expect(result.current.isAdmin).toBe(false)
  })

  it('throws error when useAuth is used outside AuthProvider', () => {
    expect(() => {
      renderHook(() => useAuth())
    }).toThrow('useAuth must be used within an AuthProvider')
  })
})
