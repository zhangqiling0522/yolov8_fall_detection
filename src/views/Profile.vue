<template>
<div class="profile-container">
<header class="profile-header">
<h1>个人中心</h1>
<button @click="goBack" class="back-button">返回首页</button>
</header>

<main class="profile-content">
<section class="personal-info-section">
<h2>个人信息</h2>
<div class="info-card">
<div class="info-item">
<span class="info-label">姓名:</span>
<span class="info-value">{{ adminInfo.name }}</span>
</div>
<div class="info-item">
<span class="info-label">编号:</span>
<span class="info-value">{{ adminInfo.id }}</span>
</div>
<div class="info-item">
<span class="info-label">年龄:</span>
<span class="info-value">{{ adminInfo.age }}</span>
</div>
<div class="info-item">
<span class="info-label">性别:</span>
<span class="info-value">{{ adminInfo.gender }}</span>
</div>
<div class="info-item">
<span class="info-label">职务:</span>
<span class="info-value">{{ adminInfo.position }}</span>
</div>
<div class="info-item">
<span class="info-label">手机号:</span>
<span class="info-value">{{ adminInfo.phone }}</span>
</div>
</div>
</section>

<section class="add-employee-section">
<h2>添加新员工</h2>
<div class="form-card">
<form @submit.prevent="addEmployee">
<div class="form-row">
<div class="form-group">
<label>编号</label>
<input type="text" v-model="newEmployee.id" class="form-input" placeholder="请输入4位编号" />
</div>
<div class="form-group">
<label>姓名</label>
<input type="text" v-model="newEmployee.name" class="form-input" placeholder="请输入姓名" />
</div>
</div>

<div class="form-row">
<div class="form-group">
<label>年龄</label>
<input type="number" v-model="newEmployee.age" class="form-input" placeholder="请输入年龄" />
</div>
<div class="form-group">
<label>性别</label>
<select v-model="newEmployee.gender" class="form-select">
<option value="男">男</option>
<option value="女">女</option>
</select>
</div>
</div>

<div class="form-row">
<div class="form-group">
<label>职务</label>
<select v-model="newEmployee.position" class="form-select">
<option value="护工">护工</option>
<option value="系统管理员">系统管理员</option>
<option value="监控管理员">监控管理员</option>
</select>
</div>
<div class="form-group">
<label>手机号</label>
<input type="text" v-model="newEmployee.phone" class="form-input" placeholder="请输入手机号" />
</div>
</div>

<div class="form-row">
<div class="form-group">
<label>密码</label>
<input type="password" v-model="newEmployee.password" class="form-input" placeholder="请输入密码" />
</div>
</div>

<button type="submit" class="submit-button">添加员工</button>
</form>
</div>
</section>

<section class="employee-list-section">
<h2>员工列表</h2>
<div class="employee-list">
<div v-for="employee in employees" :key="employee.id" class="employee-item">
<div class="employee-info">
<div class="employee-name">{{ employee.name }}</div>
<div class="employee-detail">{{ employee.position }} | {{ employee.phone }}</div>
</div>
</div>
</div>
</section>
</main>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const adminInfo = ref({
id: '0001',
name: '小张',
age: 30,
gender: '男',
position: '系统管理员',
phone: '13800138004'
})

const newEmployee = ref({
id: '',
name: '',
age: '',
gender: '男',
position: '护工',
phone: '',
password: ''
})

const employees = ref([])

// 从后端获取员工列表
const fetchEmployees = async function() {
  try {
    const response = await fetch('http://localhost:8000/admins')
    if (!response.ok) {
      throw new Error('获取员工列表失败')
    }
    const data = await response.json()
    console.log('后端返回的员工数据:', data)
    // 转换职位显示
    employees.value = data.map(admin => {
      console.log('处理员工:', admin.name, '职位:', admin.position)
      let positionText = '监控管理员'
      // 检查position字段是否存在
      if (admin.position) {
        // 直接使用后端返回的职位值
        positionText = admin.position
      }
      console.log('转换后的职位:', positionText)
      return {
        id: admin.id,
        name: admin.name,
        age: admin.age,
        gender: admin.gender,
        position: positionText,
        phone: admin.phone
      }
    })
  } catch (error) {
    console.error('获取员工列表失败:', error)
  }
}

const goBack = function() {
router.push('/')
}

const addEmployee = async function() {
if (!newEmployee.value.id || !newEmployee.value.name || !newEmployee.value.age || !newEmployee.value.phone || !newEmployee.value.password) {
alert('请填写完整的员工信息')
return
}

// 调用后端API添加员工
try {
// 转换职务为英文
let positionEnglish = newEmployee.value.position
if (positionEnglish === '护工') {
positionEnglish = 'NURSE'
} else if (positionEnglish === '系统管理员') {
positionEnglish = 'SYSTEM_ADMIN'
} else if (positionEnglish === '监控管理员') {
positionEnglish = 'MONITOR_ADMIN'
}

const response = await fetch('http://localhost:8000/admins', {
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify({
id: newEmployee.value.id,
name: newEmployee.value.name,
age: newEmployee.value.age,
gender: newEmployee.value.gender,
position: positionEnglish,
phone: newEmployee.value.phone,
password: newEmployee.value.password
})
})

if (!response.ok) {
const errorData = await response.json()
throw new Error(errorData.detail || '添加失败')
}

const result = await response.json()

// 更新前端员工列表
await fetchEmployees()

// 重置表单
newEmployee.value = {
id: '',
name: '',
age: '',
gender: '男',
position: '护工',
phone: '',
password: ''
}

alert('员工添加成功！')
} catch (error) {
alert('添加失败：' + error.message)
console.error('添加员工失败:', error)
}
}

onMounted(async function() {
console.log('加载个人中心数据')
// 从后端获取员工列表
await fetchEmployees()
})
</script>

<style scoped>
.profile-container {
min-height: 100vh;
background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), url('../pic/webbackground.jpg');
background-size: cover;
background-position: center;
display: flex;
flex-direction: column;
}

.profile-header {
  background-color: rgba(50, 205, 50, 0.8);
  color: #ffffff;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(10px);
}

.profile-header h1 {
margin: 0;
text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.back-button {
padding: 0.5rem 1rem;
background-color: rgba(52, 152, 219, 0.7);
color: white;
border: none;
border-radius: 4px;
cursor: pointer;
transition: background-color 0.3s;
}

.back-button:hover {
background-color: rgba(52, 152, 219, 0.9);
}

.profile-content {
flex: 1;
padding: 2rem;
max-width: 1200px;
margin: 0 auto;
width: 100%;
}

.personal-info-section,
.add-employee-section,
.employee-list-section {
background: rgba(255, 255, 255, 0.9);
border-radius: 8px;
padding: 1.5rem;
margin-bottom: 2rem;
box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h2 {
color: #2c3e50;
margin-bottom: 1.5rem;
font-weight: bold;
}

.info-card {
background: rgba(249, 249, 249, 0.8);
border-radius: 8px;
padding: 1.5rem;
}

.info-item {
display: flex;
justify-content: space-between;
margin-bottom: 1rem;
padding: 0.5rem 0;
border-bottom: 1px solid rgba(224, 224, 224, 0.8);
}

.info-item:last-child {
border-bottom: none;
}

.info-label {
font-weight: 600;
color: #34495e;
}

.info-value {
color: #7f8c8d;
}

.form-card {
background: rgba(249, 249, 249, 0.8);
border-radius: 8px;
padding: 1.5rem;
}

.form-row {
display: flex;
gap: 1.5rem;
margin-bottom: 1.5rem;
flex-wrap: wrap;
}

.form-group {
flex: 1;
min-width: 200px;
}

.form-group label {
display: block;
color: #34495e;
margin-bottom: 0.5rem;
font-weight: 500;
}

.form-input,
.form-select {
width: 100%;
padding: 0.8rem;
border: 1px solid #ddd;
border-radius: 6px;
font-size: 1rem;
transition: border-color 0.3s;
background: rgba(255, 255, 255, 0.8);
}

.form-input:focus,
.form-select:focus {
outline: none;
border-color: #3498db;
box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.1);
}

.submit-button {
padding: 0.8rem 1.5rem;
background-color: rgba(46, 204, 113, 0.7);
color: white;
border: none;
border-radius: 4px;
cursor: pointer;
transition: background-color 0.3s;
font-size: 1rem;
font-weight: 500;
}

.submit-button:hover {
background-color: rgba(39, 174, 96, 0.9);
}

.employee-list {
background: rgba(249, 249, 249, 0.8);
border-radius: 8px;
padding: 1rem;
}

.employee-item {
background: rgba(255, 255, 255, 0.8);
border-radius: 6px;
padding: 1rem;
margin-bottom: 1rem;
border-left: 4px solid #3498db;
display: flex;
justify-content: space-between;
align-items: center;
}

.employee-item:last-child {
margin-bottom: 0;
}

.employee-name {
font-weight: 600;
color: #2c3e50;
margin-bottom: 0.25rem;
}

.employee-detail {
font-size: 0.9rem;
color: #7f8c8d;
}

@media (max-width: 768px) {
.profile-content {
padding: 1rem;
}

.form-row {
flex-direction: column;
}

.form-group {
min-width: 100%;
}
}
</style>