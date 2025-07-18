<script setup lang="ts">

</script>

<template>
  <div class="container">
    <span class="rainbow-text">这是首页</span>
  </div>
</template>

<style scoped lang="less">
.container {
  width: 100%;
  height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
}

.rainbow-text {
  font-size: 128px;
  font-weight: bold;
  background: linear-gradient(90deg, #ff6b6b, #f7d06c, #4ecdc4, #5e60ce, #ff6b6b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-fill-color: transparent;
  text-shadow: 1px 1px 2px #fff6, 0 2px 8px #0002;
}
</style>