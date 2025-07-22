<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { streamWriteArticle } from '@/api/write'
import { CopyDocument } from '@element-plus/icons-vue'

// --- Component State ---
const userInput = ref('')
const generatedContent = ref('')
const isLoading = ref(false)

// 新增：文章类型的状态和选项
const selectedArticleType = ref('comment')
const articleTypeOptions = ref([
  { value: 'comment', label: '评论文' },
  { value: 'reduce_ai', label: '降低ai率' },
])

const handleWriteArticle = async () => {
  if (!userInput.value.trim()) {
    ElMessage.warning('请输入一些内容来开始写作。')
    return
  }

  isLoading.value = true
  generatedContent.value = ''

  const payload = {
    article_type: selectedArticleType.value, // 使用下拉框选中的值
    article_content: userInput.value,
  }

  await streamWriteArticle(
    payload,
    (chunk) => {
      generatedContent.value += chunk
    },
    () => {
      isLoading.value = false
    },
    (error) => {
      console.error('流式请求错误:', error)
      ElMessage.error('文章生成过程中发生错误。')
      isLoading.value = false
    }
  )
}

const copyGeneratedContent = async () => {
  if (!generatedContent.value) {
    ElMessage.warning('没有可复制的内容。')
    return
  }
  try {
    await navigator.clipboard.writeText(generatedContent.value)
    ElMessage.success('内容已成功复制到剪贴板！')
  } catch (err) {
    console.error('复制失败:', err)
    ElMessage.error('复制失败，请手动复制。')
  }
}
</script>

<template>
  <div class="write-container">
    <div class="input-section">
      <el-input
        v-model="userInput"
        type="textarea"
        :rows="10"
        placeholder="在这里输入您的主题、大纲或初始段落..."
        class="input-textarea"
        resize="vertical"
      />
      <div class="actions-bar">
        <el-select v-model="selectedArticleType" placeholder="选择文章类型" class="type-select">
          <el-option
            v-for="item in articleTypeOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-button
          type="primary"
          @click="handleWriteArticle"
          :loading="isLoading"
          class="generate-button"
        >
          {{ isLoading ? '生成中...' : '生成文章' }}
        </el-button>
      </div>
    </div>

    <div v-if="generatedContent || isLoading" class="output-section">
      <div class="output-header">
        <h3>生成内容:</h3>
        <el-button
          type="success"
          :icon="CopyDocument"
          @click="copyGeneratedContent"
          circle
          title="复制内容"
        />
      </div>
      <div class="output-content">
        <pre>{{ generatedContent }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.write-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.actions-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 15px;
}

.type-select {
  width: 150px;
}

.generate-button {
  width: 180px;
}

.output-section {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 15px;
  min-height: 200px;
  background-color: #f9fafb;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;

  h3 {
    margin: 0;
    color: #303133;
    font-size: 18px;
  }
}

.output-content {
  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
    line-height: 1.6;
    color: #606266;
  }
}
</style>