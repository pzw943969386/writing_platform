<script setup lang="ts">
import { ref } from "vue";
import { splitText } from "@/api/other";

const text = ref("");

const splitTextData = async () => {
  const res = await splitText({ text: text.value });
  text.value = res.text;
};
</script>

<template>
  <div class="container">
    <div class="header">
      <el-button @click="splitTextData" type="primary">点击进行分段</el-button>
    </div>
    <div class="content">
      <el-input v-model="text" type="textarea" :rows="30" />
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
    margin-bottom: 10px;
  }
}
</style>