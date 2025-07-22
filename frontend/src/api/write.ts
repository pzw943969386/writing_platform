interface ArticleWriteRequest {
  article_type: string
  article_content: string
}

/**
 * 调用文章写作接口并处理流式响应 (使用 Fetch API，最稳定可靠)。
 * @param payload 发送到API的数据。
 * @param onChunk 接收到每个数据块时调用的回调函数。
 * @param onFinish 流结束时调用的回调函数。
 * @param onError 发生错误时调用的回调函数。
 */
export const streamWriteArticle = async (
  payload: ArticleWriteRequest,
  onChunk: (chunk: string) => void,
  onFinish: () => void,
  onError: (error: any) => void,
) => {
  try {
    const response = await fetch('http://localhost:8888/write/article_write', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'text/event-stream',
      },
      body: JSON.stringify(payload),
    })

    if (!response.ok || !response.body) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    while (true) {
      const { done, value } = await reader.read()
      if (done) {
        break // 流结束
      }
      const chunk = decoder.decode(value, { stream: true })
      onChunk(chunk) // 调用回调，传递数据块
    }
  } catch (error) {
    onError(error)
  } finally {
    onFinish()
  }
}
