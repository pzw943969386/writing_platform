<script setup lang="ts">
import { ref } from 'vue'
import { getArticleContentByUrl } from '@/api/article'

const input = ref('')

const articleContent = ref('')

const getArticleContent = async () => {
  const res = await getArticleContentByUrl({ url: input.value })
  articleContent.value = res.data
}
</script>

<template>
  <div class="container">
    <div class="header">
      <el-input v-model="input" style="width: 80%" placeholder="请输入文章url" />
      <el-button @click="getArticleContent" type="primary">查询</el-button>
    </div>
    <div class="content">
      <div>{{ articleContent }}</div>
    </div>
  </div>
</template>

<style scoped lang="less">
.container {
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  .header {
    display: flex;
    justify-content: center;
    margin: 10px;
  }
}
</style>
