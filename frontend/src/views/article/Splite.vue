<script setup lang="ts">
import { ref } from 'vue'
import { splitText } from '@/api/tools'
import { ElMessage } from 'element-plus'

const text = ref('')

const splitTextData = async () => {
  try {
    const res = await splitText({ text: text.value })
    if (res.code === 200 && res.data) {
      text.value = res.data
    } else {
      ElMessage.error(res.message || '分段失败')
    }
  } catch (error) {
    ElMessage.error('分段失败')
  }
}

const copyText = () => {
  if (!text.value) {
    ElMessage.error('文本为空')
    return
  }
  try {
    navigator.clipboard.writeText(text.value)
    ElMessage.success('复制成功')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}
</script>

<template>
  <div class="container">
    <div class="header"></div>
    <div class="content">
      <el-input v-model="text" type="textarea" :autosize="{ minRows: 15, maxRows: 15 }" />
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