<script setup lang="ts">
import { ref } from "vue";
import { splitText } from "@/api/splite";

const text = ref("");

const splitTextData = async () => {
  const res = await splitText({ text: text.value });
  text.value = res.text;
};

const copyText = () => {
  navigator.clipboard.writeText(text.value);
};
</script>

<template>
  <div class="container">
    <div class="header">
      <!-- <el-button @click="splitTextData" type="primary">点击进行分段</el-button> -->
    </div>
    <div class="content">
      <el-input v-model="text" type="textarea" :autosize="{ minRows: 15, maxRows: 15}" />
    </div>
    <div class="footer">
      <el-button @click="splitTextData" type="primary">点击进行分段</el-button>
      <el-button @click="copyText" type="primary">复制</el-button>
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
  .footer {
    display: flex;
    justify-content: center;
    margin-top: 10px;
  }
}
</style>@/api/splite