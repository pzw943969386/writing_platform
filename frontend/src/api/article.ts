import { httpGet, httpPost } from '@/service/requests'
import type { ArticleInfo } from './types'

export const getBreakingArticleList = (params: any = {}) => {
  return httpGet<ArticleInfo[]>('/article/list/breaking', params)
}

export const getHotArticleList = (params: any = {}) => {
  return httpGet<ArticleInfo[]>('/article/list/hot', params)
}

export const getArticleContent = (data: any = {}) => {
  return httpPost<ArticleInfo>('/article/content', data)
}

export const reloadArticle = (data: any = {}) => {
  return httpPost<ArticleInfo[]>('/article/reload', data)
}

export const getArticleContentByUrl = (data: any = {}) => {
  return httpPost<string>('/article/content/url', data)
}
