<template>
  <div class="login-container">
    <div class="login-form">
      <h1 class="login-title">管理员登录</h1>
      
      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <div class="form-group">
        <label class="form-label">姓名</label>
        <input 
          type="text" 
          v-model="formData.name" 
          class="form-input" 
          placeholder="请输入姓名" 
        />
      </div>
      <div class="form-group">
        <label class="form-label">手机号</label>
        <input 
          type="text" 
          v-model="formData.phone" 
          class="form-input" 
          placeholder="请输入手机号" 
        />
      </div>
      <div class="form-group">
        <label class="form-label">密码</label>
        <input 
          type="password" 
          v-model="formData.password" 
          class="form-input" 
          placeholder="请输入密码" 
        />
      </div>
      <button 
        @click="handleLogin" 
        class="login-button" 
        :disabled="isLoading"
      >
        {{ isLoading ? '登录中...' : '登录' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['login-success'])

const formData = ref({
  name: '',
  phone: '',
  password: ''
})

const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  // 表单验证
  if (!formData.value.name || !formData.value.phone || !formData.value.password) {
    errorMessage.value = '请填写所有必填字段'
    return
  }
  
  // 重置错误信息
  errorMessage.value = ''
  isLoading.value = true
  
  try {
    // 调用后端登录API
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData.value)
    })
    
    const data = await response.json()
    
    if (data.success) {
      // 登录成功，存储管理员信息到本地存储
      localStorage.setItem('admin', JSON.stringify({
        id: data.admin_id,
        name: data.admin_name
      }))
      
      // 触发登录成功事件
      emit('login-success', data)
      
      // 跳转到主应用页面
      // 这里我们将在App.vue中处理路由逻辑
      // 暂时使用alert模拟
      alert('登录成功！')
      // 实际项目中应该使用路由跳转
      // router.push('/dashboard')
    } else {
      // 登录失败
      errorMessage.value = data.message
    }
  } catch (error) {
    console.error('登录请求失败:', error)
    errorMessage.value = '登录失败，请检查网络连接'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  background-image: url('../pic/login.jpeg');
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1;
}

.login-form {
  background: rgba(255, 255, 255, 0.9);
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  z-index: 2;
  width: 100%;
  max-width: 400px;
}

.login-title {
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.8rem;
  font-weight: bold;
}

.error-message {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
  padding: 0.8rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  color: #555;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.1);
}

.login-button {
  width: 100%;
  padding: 0.9rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 1rem;
}

.login-button:hover:not(:disabled) {
  background-color: #2980b9;
}

.login-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .login-form {
    padding: 2rem;
    margin: 1rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
}
</style>