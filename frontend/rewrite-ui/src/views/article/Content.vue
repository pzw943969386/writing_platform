<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getArticleContent } from "@/api/article";
import { useRoute, useRouter } from "vue-router";
import { ArrowLeft, CopyDocument } from "@element-plus/icons-vue";

const route = useRoute();
const router = useRouter();

const title = ref(route.query.title as string);
const loading = ref(true);
const articleContent = ref("");

const getArticleContentData = async (id: number, url: string) => {
  loading.value = true;
  const res = await getArticleContent({ article_id: id, article_url: url });
  articleContent.value = res.data.content;
  loading.value = false;
};

onMounted(() => {
  getArticleContentData(route.query.id as string, route.query.url as string);
});

const goBack = () => {
  router.back();
};

const copyContent = () => {
  navigator.clipboard.writeText(articleContent.value);
};
</script>

<template>
  <div class="container">
    <div class="main">
      <div class="header">
        <el-button @click="goBack" :icon="ArrowLeft" type="primary"></el-button>
        <el-button @click="copyContent" :icon="CopyDocument" type="success"></el-button>
      </div>
      <div class="content">
        <div class="title">{{ title }}</div>
        <div class="url">{{ url }}</div>
        <div class="content" v-loading="loading">{{ articleContent }}</div>
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
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title {
  height: 50px;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
  line-height: 50px;
}
.content {
  width: 100%;
  height: 100%;
  font-size: 16px;
  line-height: 32px;
}
</style>
