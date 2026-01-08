import { describe, it, expect } from 'vitest'
import { api, API_BASE_URL } from '../api/config'

describe('API Config', () => {
  it('has a valid base URL', () => {
    expect(API_BASE_URL).toBeDefined()
    expect(typeof API_BASE_URL).toBe('string')
    expect(API_BASE_URL.length).toBeGreaterThan(0)
  })

  it('exports api object with baseURL', () => {
    expect(api.baseURL).toBeDefined()
    expect(api.baseURL).toBe(API_BASE_URL)
  })

  it('has all required endpoints', () => {
    expect(api.endpoints.products).toBe('/api/products')
    expect(api.endpoints.suppliers).toBe('/api/suppliers')
    expect(api.endpoints.orders).toBe('/api/orders')
    expect(api.endpoints.branches).toBe('/api/branches')
    expect(api.endpoints.headquarters).toBe('/api/headquarters')
    expect(api.endpoints.deliveries).toBe('/api/deliveries')
    expect(api.endpoints.orderDetails).toBe('/api/order-details')
    expect(api.endpoints.orderDetailDeliveries).toBe('/api/order-detail-deliveries')
  })

  it('endpoints are properly formatted', () => {
    Object.values(api.endpoints).forEach(endpoint => {
      expect(endpoint).toMatch(/^\/api\/[a-z-]+$/)
    })
  })
})
