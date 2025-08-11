import axios, { type AxiosRequestConfig } from 'axios'
import type { ApiResponse } from '@/api/types'

const request = axios.create({
  baseURL: 'http://localhost:8100',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

request.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

request.interceptors.response.use(
  (response) => {
    if (response.status === 200) {
      return Promise.resolve(response.data)
    } else {
      return Promise.reject(response.data)
    }
  },
  (error) => {
    return Promise.reject(error)
  },
)

export const httpGet = <T>(url: string, params: any): Promise<ApiResponse<T>> => {
  return request.get(url, { params })
}

export const httpPost = <T>(url: string, data?: object): Promise<ApiResponse<T>> => {
  return request.post(url, data)
}

export default request
