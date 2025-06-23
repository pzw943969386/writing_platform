import { httpGet, httpPost } from "@/service/requests"

export const getArticleList = (params: any = {}) => {
    return httpGet('/article/list', params)
}

export const getArticleContent = (data: any = {}) => {
    return httpPost('/article/content', data)
}

export const reloadArticle = (data: any = {}) => {
    return httpPost('/article/reload', data)
}