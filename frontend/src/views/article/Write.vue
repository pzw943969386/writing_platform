<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { streamWriteArticle } from '@/api/write'
import { CopyDocument } from '@element-plus/icons-vue'
import { splitText } from '@/api/tools'

// --- Component State ---
const userInput = ref('')
const generatedContent = ref('')
const isLoading = ref(false)

const handleWriteArticle = async () => {
  if (!userInput.value.trim()) {
    ElMessage.warning('请输入一些内容来开始写作。')
    return
  }

  isLoading.value = true
  generatedContent.value = ''

  const payload = {
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

const handleSplitArticle = async () => {
  try {
    const res = await splitText({ text: generatedContent.value })
    if (res.code === 200 && res.data) {
      generatedContent.value = res.data
    } else {
      ElMessage.error(res.message || '分段失败')
    }
  } catch (error) {
    ElMessage.error('分段失败')
  }
}

const clearContent = () => {
  generatedContent.value = ''
}
</script>

<template>
  <div class="write-container">
    <!-- 左侧输入区域 -->
    <div class="input-section">
      <div class="section-header">
        <h3>输入文章</h3>
        <el-button
          type="primary"
          @click="handleWriteArticle"
          :loading="isLoading"
          class="generate-button"
        >
          {{ isLoading ? '分析重写中...' : '分析重写' }}
        </el-button>
      </div>
      <el-input
        v-model="userInput"
        type="textarea"
        :rows="25"
        placeholder="在这里粘贴您想要分析和重写的文章内容..."
        class="input-textarea"
        resize="vertical"
      />
    </div>

    <!-- 右侧输出区域 -->
    <div class="output-section">
      <div class="section-header">
        <h3>重写结果</h3>
        <div class="output-actions">
          <el-button
            type="danger"
            @click="clearContent"
            size="small"
            plain
            v-if="generatedContent"
          >
            清空
          </el-button>
          <el-button
            type="success"
            :icon="CopyDocument"
            @click="copyGeneratedContent"
            size="small"
            v-if="generatedContent"
          >
            复制
          </el-button>
          <el-button
            type="primary"
            @click="handleSplitArticle"
            size="small"
            v-if="generatedContent"
          >
            分段
          </el-button>
        </div>
      </div>
      
      <div class="output-content" :class="{ 'loading': isLoading }">
        <div v-if="isLoading && !generatedContent" class="loading-placeholder">
          <el-icon class="loading-icon"><Loading /></el-icon>
          <p>正在分析和重写文章，请稍候...</p>
        </div>
        <div v-else-if="!generatedContent && !isLoading" class="empty-placeholder">
          <p>重写后的文章内容将在这里显示</p>
        </div>
        <pre v-else class="content-text">{{ generatedContent }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.write-container {
  padding: 20px;
  display: flex;
  gap: 20px;
  height: calc(100vh - 120px); // 减去顶部导航和padding的高度
}

.input-section,
.output-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-width: 0; // 防止flex项目溢出
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 2px solid #e4e7ed;

  h3 {
    margin: 0;
    color: #303133;
    font-size: 18px;
    font-weight: 600;
  }
}

.generate-button {
  min-width: 120px;
}

.output-actions {
  display: flex;
  gap: 10px;
}

.input-textarea {
  flex: 1;
  
  :deep(.el-textarea__inner) {
    height: 100% !important;
    resize: none;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.6;
  }
}

.output-content {
  flex: 1;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  background-color: #fafafa;
  overflow: hidden;
  display: flex;
  flex-direction: column;

  &.loading {
    border-color: #409eff;
    background-color: #f0f9ff;
  }

  .loading-placeholder,
  .empty-placeholder {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #909399;
    
    .loading-icon {
      font-size: 24px;
      margin-bottom: 10px;
      animation: rotate 2s linear infinite;
    }
    
    p {
      margin: 0;
      font-size: 14px;
    }
  }

  .empty-placeholder {
    background-color: #f9f9f9;
    
    p {
      color: #c0c4cc;
    }
  }

  .content-text {
    flex: 1;
    padding: 15px;
    margin: 0;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.6;
    color: #303133;
    background-color: #ffffff;
    overflow-y: auto;
    border: none;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .write-container {
    flex-direction: column;
    height: auto;
  }
  
  .input-section,
  .output-section {
    flex: none;
  }
  
  .input-textarea :deep(.el-textarea__inner) {
    height: 300px !important;
  }
  
  .output-content {
    min-height: 400px;
  }
}

@media (max-width: 768px) {
  .write-container {
    padding: 10px;
    gap: 15px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
    
    .output-actions {
      justify-content: center;
    }
  }
  
  .generate-button {
    width: 100%;
  }
}
</style>