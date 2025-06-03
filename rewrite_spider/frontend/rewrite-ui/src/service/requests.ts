import axios from 'axios'

const request = axios.create({
  baseURL: 'http://localhost:8888',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

request.interceptors.request.use((config) => {
  return config
}, (error) => {
  return Promise.reject(error)
})

request.interceptors.response.use((response) => {
  if (response.status === 200) {
    return Promise.resolve(response.data)
  } else {
    return Promise.reject(response.data)
  }
}, (error) => {
  return Promise.reject(error)
})

export const httpGet = (url: string, params: any) => {
    return new Promise((resolve, reject) => {
        request.get(url, { params }).then((res) => {
            resolve(res)
        }).catch((err) => {
            reject(err)
        })
    })
}

export const httpPost = (url: string, data: any) => {
    return new Promise((resolve, reject) => {
        request.post(url, data).then((res) => {
            resolve(res)
        }).catch((err) => {
            reject(err)
        })
    })
}

export default request