export interface ApiResponse<T> {
  message: string
  code: number
  data: T
}

/** 文章信息的基本结构 */
export interface ArticleInfo {
  id: number
  current_date: number
  title: string
  content: string
  url: string
}

