<script setup lang="ts">
import { getArticleList, getArticleContent } from "@/api/article";
import { ref, onMounted } from "vue";

interface Article {
  title: string;
  url: string;
}

const articleList = ref<Article[]>([]);

const getArticleListData = async () => {
  const res = await getArticleList();
  articleList.value = res.data;
};

const getArticleContentData = async (url: string) => {
  try {
    const res = await getArticleContent({ title_url: url });
    console.log(res);
    const index = articleList.value.findIndex((item) => item.url === url);
    if (index !== -1) {
      articleList.value[index].content = res.data;
    }
  } catch (error) {
    console.error("Failed to get article content:", error);
  }
};

onMounted(() => {
  getArticleListData();
});
</script>

<template>
  <div class="container">
    <div class="left">
      <ul>
        <li>
          <p
            v-for="item in articleList"
            :key="item.url"
            target="_blank"
            @click="getArticleContentData(item.url)"
          >
            {{ item.title }} {{ item.content }}
          </p>
        </li>
      </ul>
    </div>

    <div class="right"></div>
  </div>
</template>

<style scoped lang="less">
.container {
  display: flex;
  width: 100%;
  height: 100%;
  .left {
    width: 100%;
    height: 100%;
  }
  .left p {
    cursor: pointer;
    word-break: break-all;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .right {
    flex: 1;
    height: 100%;
    background-color: rgb(199, 42, 42);
  }
}
.left {
  ul {
    li {
      list-style: none;
    }
  }
}
</style>
