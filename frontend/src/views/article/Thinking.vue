<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { CopyDocument, Delete } from '@element-plus/icons-vue'

// 存储键名
const STORAGE_KEY = 'text_notes_content'

// 组件状态
const textContent = ref('')
const lastSaveTime = ref<Date | null>(null)

// 从localStorage加载内容
const loadContent = () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    try {
      const data = JSON.parse(saved)
      textContent.value = data.content || ''
      lastSaveTime.value = data.saveTime ? new Date(data.saveTime) : null
    } catch (error) {
      console.error('加载保存的内容失败:', error)
    }
  }
}

// 保存内容到localStorage
const saveContent = () => {
  const data = {
    content: textContent.value,
    saveTime: new Date().toISOString()
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  lastSaveTime.value = new Date()
}

// 清空内容
const clearContent = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有内容吗？此操作无法撤销。',
      '确认清空',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    textContent.value = ''
    localStorage.removeItem(STORAGE_KEY)
    lastSaveTime.value = null
    ElMessage.success('内容已清空')
  } catch {
    // 用户取消了操作
  }
}

// 复制内容
const copyContent = async () => {
  if (!textContent.value.trim()) {
    ElMessage.warning('没有可复制的内容')
    return
  }
  
  try {
    await navigator.clipboard.writeText(textContent.value)
    ElMessage.success('内容已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败，请手动复制')
  }
}

// 格式化时间显示
const formatTime = (time: Date | null) => {
  if (!time) return '暂无保存记录'
  return time.toLocaleString('zh-CN')
}

// 监听内容变化，自动保存
watch(textContent, () => {
  saveContent()
}, { deep: true })

// 组件挂载时加载内容
onMounted(() => {
  loadContent()
})

// 页面卸载前保存（额外保险）
window.addEventListener('beforeunload', saveContent)
</script>

<template>
  <div class="notes-container">
    <div class="notes-header">
      <div class="header-left">
        <h2>文本记录本</h2>
        <p class="save-info">{{ `最后保存: ${formatTime(lastSaveTime)}` }}</p>
      </div>
      <div class="header-actions">
        <el-button
          type="success"
          :icon="CopyDocument"
          @click="copyContent"
          size="small"
          v-if="textContent.trim()"
        >
          复制全部
        </el-button>
        <el-button
          type="danger"
          :icon="Delete"
          @click="clearContent"
          size="small"
          v-if="textContent.trim()"
        >
          清空内容
        </el-button>
      </div>
    </div>

    <div class="notes-content">
      <el-input
        v-model="textContent"
        type="textarea"
        placeholder="在这里记录你的想法、笔记或任何重要内容...&#10;&#10;✨ 特点：&#10;• 自动保存，刷新页面不丢失&#10;• 切换页面内容保持不变&#10;• 只有点击'清空内容'才会删除&#10;• 支持一键复制全部内容"
        class="notes-textarea"
        resize="none"
        :autosize="{ minRows: 20 }"
      />
    </div>

    <div class="notes-footer">
      <div class="footer-info">
        <span class="word-count">字数: {{ textContent.length }}</span>
        <span class="auto-save-tip">💾 内容自动保存中...</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.notes-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
}

.notes-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e4e7ed;

  .header-left {
    h2 {
      margin: 0 0 8px 0;
      color: #303133;
      font-size: 24px;
      font-weight: 600;
    }

    .save-info {
      margin: 0;
      color: #909399;
      font-size: 14px;
    }
  }

  .header-actions {
    display: flex;
    gap: 10px;
    align-items: center;
  }
}

.notes-content {
  flex: 1;
  margin-bottom: 20px;

  .notes-textarea {
    :deep(.el-textarea__inner) {
      border: 2px solid #e4e7ed;
      border-radius: 8px;
      font-size: 16px;
      line-height: 1.6;
      color: #303133;
      background-color: #ffffff;
      padding: 20px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
      transition: all 0.3s ease;
      resize: none;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;

      &:focus {
        border-color: #409eff;
        box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.15);
      }

      &::placeholder {
        color: #c0c4cc;
        font-size: 15px;
        line-height: 1.8;
      }
    }
  }
}

.notes-footer {
  .footer-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    color: #909399;
    font-size: 14px;
    border-top: 1px solid #f0f0f0;

    .word-count {
      font-weight: 500;
    }

    .auto-save-tip {
      color: #67c23a;
      font-size: 13px;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .notes-container {
    padding: 15px;
  }

  .notes-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;

    .header-actions {
      justify-content: flex-end;
    }
  }

  .notes-content {
    .notes-textarea {
      :deep(.el-textarea__inner) {
        font-size: 14px;
        padding: 15px;
      }
    }
  }

  .notes-footer {
    .footer-info {
      flex-direction: column;
      gap: 8px;
      align-items: center;
    }
  }
}

@media (max-width: 480px) {
  .notes-container {
    padding: 10px;
  }

  .notes-header {
    .header-left {
      h2 {
        font-size: 20px;
      }
    }

    .header-actions {
      flex-direction: column;
      gap: 8px;

      .el-button {
        width: 100%;
      }
    }
  }
}
</style>