import { httpGet, httpPost } from "@/service/requests"

export const getBreakingArticleList = (params: any = {}) => {
    return httpGet('/article/list/breaking', params)
}

export const getHotArticleList = (params: any = {}) => {
    return httpGet('/article/list/hot', params)
}

export const getArticleContent = (data: any = {}) => {
    return httpPost('/article/content', data)
}

export const reloadArticle = (data: any = {}) => {
    return httpPost('/article/reload', data)
}

export const getArticleContentByUrl = (data: any = {}) => {
    return httpPost('/article/content/url', data)
}