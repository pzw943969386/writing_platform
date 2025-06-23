<script setup lang="ts">
import { getArticleList, getArticleContent, reloadArticle } from "@/api/article";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Refresh } from "@element-plus/icons-vue";

const router = useRouter();

interface Article {
  title: string;
  url: string;
}

const articleList = ref<Article[]>([]);
const loading = ref(false);

const getArticleListData = async () => {
  loading.value = true;
  const res = await getArticleList();
  articleList.value = res.data;
  loading.value = false;
};

const goArticleContent = (id: number, url: string, title: string) => {
  console.log("点击跳转，URL:", url);
  router.push({
    name: "articleContent",
    query: { id, url, title },
  });
};

const getArticleRewriteData = async () => {
  loading.value = true;
  const res = await reloadArticle();
  articleList.value = res.data;
  loading.value = false;
};

const getRandomColor = () => {
  return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
};

onMounted(() => {
  getArticleListData();
});
</script>

<template>
  <div class="container">
    <div class="main">
      <el-button @click="getArticleRewriteData" :icon="Refresh" type="success"></el-button>
      <div class="data" v-for="item in articleList" :key="item.url" target="_blank" v-loading="loading">
        <div
          class="title"
          :style="{ color: getRandomColor() }"
          @click="goArticleContent(item.id, item.url, item.title)"
        >
          {{ item.title }}
        </div>
      </div>
    </div>
    <router-view />
  </div>
</template>

<style scoped lang="less">
.container {
  display: flex;
  width: 100%;
  height: 100%;
  .main {
    width: 100%;
    height: 100%;
    margin: 10px;
  }
}
.data {
  width: 100%;
  text-align: center;
  margin: 10px 0;
  cursor: pointer;
  .id {
    width: 30px;
  }
  .title {
    font-size: 18px;
  }
}
</style>
