<script setup lang="ts">
import { getBreakingArticleList, getHotArticleList, reloadArticle } from '@/api/article'
import type { ArticleInfo } from '@/api/types'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Refresh } from '@element-plus/icons-vue'

const router = useRouter()

const articleList = ref<ArticleInfo[]>([])
const loading = ref(false)

const getArticleListData = async () => {
  loading.value = true
  try {
    const res = await getBreakingArticleList()
    if (res.code === 200) {
      articleList.value = res.data
    }
  } finally {
    loading.value = false
  }
}

const getHotArticleListData = async () => {
  loading.value = true
  try {
    const res = await getHotArticleList()
    if (res.code === 200) {
      articleList.value = res.data
    }
  } finally {
    loading.value = false
  }
}

const goArticleContent = (article: ArticleInfo) => {
  router.push({
    name: 'articleContent',
    query: { id: article.id, url: article.url, title: article.title },
  })
}

const getArticleRewriteData = async () => {
  loading.value = true
  try {
    const res = await reloadArticle()
    if (res.code === 200) {
      articleList.value = res.data
    }
  } finally {
    loading.value = false
  }
}

const getRandomColor = () => {
  return `#${Math.floor(Math.random() * 16777215)
    .toString(16)
    .padStart(6, '0')}`
}

onMounted(() => {
  getArticleListData()
})
</script>

<template>
  <div class="container">
    <div class="main">
      <el-button @click="getArticleRewriteData" :icon="Refresh" type="success" circle></el-button>
      <!-- <el-button @click="getHotArticleList" type="primary">热门</el-button> -->
      <div class="data-list" v-loading="loading">
        <div
          v-for="item in articleList"
          :key="item.id"
          class="data-item"
          @click="goArticleContent(item)"
        >
          <div class="title" :style="{ color: getRandomColor() }">
            {{ item.title }}
          </div>
        </div>
      </div>
    </div>
    <router-view />
  </div>
</template>

<style scoped lang="less">
.container {
  width: 100%;
  height: 100%;
  .main {
    width: 100%;
    height: 100%;
    margin: 10px;
    .data-list {
      margin-top: 10px;
    }
    .data-item {
      width: 100%;
      text-align: center;
      margin: 10px 0;
      cursor: pointer;
      .title {
        font-size: 18px;
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
}
</style>
