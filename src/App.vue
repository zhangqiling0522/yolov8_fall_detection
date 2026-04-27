<template>
  <router-view v-if="isLoggedIn" />
  <Login v-else @login-success="handleLoginSuccess" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Login from './components/Login.vue'

// 登录状态管理
const isLoggedIn = ref(false)

// 检查登录状态
onMounted(() => {
  checkLoginStatus()
})

// 检查登录状态
const checkLoginStatus = () => {
  const admin = localStorage.getItem('admin')
  if (admin) {
    isLoggedIn.value = true
  }
}

// 处理登录成功
const handleLoginSuccess = (adminData) => {
  isLoggedIn.value = true
}
</script>

<style>
/* 全局样式 */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: url('./pic/webbackground.jpg') no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
}
</style>