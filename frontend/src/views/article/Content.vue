<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getArticleContent } from '@/api/article'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, CopyDocument } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const title = ref('')
const url = ref('')
const articleContent = ref('')
const loading = ref(true)

const getArticleContentData = async (id: number, articleUrl: string) => {
  loading.value = true
  try {
    const res = await getArticleContent({ article_id: id, article_url: articleUrl })
    if (res.code === 200 && res.data) {
      articleContent.value = res.data.content
      title.value = res.data.title
      url.value = res.data.url
    } else {
      ElMessage.error(res.message || '获取文章失败')
    }
  } catch (error) {
    ElMessage.error('获取文章失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const { id: queryId, url: queryUrl, title: queryTitle } = route.query
  const id = Number(queryId)

  if (!isNaN(id) && typeof queryUrl === 'string' && queryUrl) {
    title.value = (queryTitle as string) || 'Loading article...'
    getArticleContentData(id, queryUrl)
  } else {
    ElMessage.error('Invalid article parameters. Redirecting to home.')
    loading.value = false
    router.replace({ name: 'articleHome' })
  }
})

const goBack = () => {
  router.back()
}

const copyContent = () => {
  if (!articleContent.value) {
    ElMessage.error('文章内容为空')
    return
  }
  try {
    navigator.clipboard.writeText(articleContent.value)
    ElMessage.success('复制成功')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}
</script>

<template>
  <div class="container">
    <div class="main">
      <div class="header">
        <el-button @click="goBack" :icon="ArrowLeft" type="primary" circle></el-button>
        <el-button @click="copyContent" :icon="CopyDocument" type="success" circle></el-button>
      </div>
      <div class="article-container" v-loading="loading">
        <div class="title">{{ title }}</div>
        <a class="url" :href="url" target="_blank" rel="noopener noreferrer">{{ url }}</a>
        <div class="article-body">{{ articleContent }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}
.main {
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  margin-bottom: 20px;
}
.article-container {
  overflow-y: auto; // Allow content to scroll
  flex-grow: 1;
}
.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
}
.url {
  display: block;
  text-align: center;
  margin-bottom: 20px;
  font-size: 14px;
  color: #888;
  word-break: break-all;
  &:hover {
    color: #409eff;
  }
}
.article-body {
  font-size: 16px;
  line-height: 1.8;
  white-space: pre-wrap; // Preserve whitespace and wrap lines
}
</style>
