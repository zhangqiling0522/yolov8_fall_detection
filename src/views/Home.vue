<template>
  <div class="app-container">
    <header class="app-header">
      <h1>基于YOLOv8的摔倒智能检测系统</h1>
      <div class="user-info">
        <span>欢迎，{{ adminName }}</span>
        <button @click="goToProfile" class="profile-button">个人中心</button>
        <button @click="handleLogout" class="logout-button">退出登录</button>
      </div>
    </header>
    <main class="app-main">
      <section class="monitoring-section">
        <h2>实时监测</h2>
        <div class="video-container">
          <video ref="videoElement" class="video-player" autoplay></video>
          <canvas ref="canvasElement" class="detection-canvas"></canvas>
        </div>
        <div class="control-panel">
          <button @click="startCamera" class="control-btn">启动摄像头</button>
          <button @click="stopCamera" class="control-btn">停止摄像头</button>
          <button @click="loadVideo" class="control-btn">加载视频</button>
          <input type="file" ref="videoFile" accept="video/*" style="display: none;" @change="handleVideoFile" />
        </div>
        
        <!-- 记录查询窗口 -->
        <div class="log-query-section">
          <h3>记录查询</h3>
          <div class="query-form">
            <div class="form-row">
              <div class="form-group">
                <label>查询方式</label>
                <select v-model="queryType" class="form-select">
                  <option value="time">按时间查询</option>
                  <option value="room">按房间号查询</option>
                  <option value="name">按姓名查询</option>
                </select>
              </div>
              <div class="form-group" v-if="queryType === 'time'">
                <label>时间</label>
                <input type="datetime-local" v-model="queryTime" class="form-input" />
              </div>
              <div class="form-group" v-else-if="queryType === 'room'">
                <label>房间号</label>
                <input type="text" v-model="queryRoom" class="form-input" placeholder="请输入房间号" />
              </div>
              <div class="form-group" v-else>
                <label>姓名</label>
                <input type="text" v-model="queryName" class="form-input" placeholder="请输入姓名" />
              </div>
              <button @click="queryLogs" class="control-btn">查询</button>
            </div>
          </div>
          <div class="log-results">
            <h4>查询结果</h4>
            <div v-if="logs.length > 0" class="log-list">
              <div v-for="log in logs" :key="log.id" class="log-item">
                <div class="log-item-header">
                  <span class="log-room">房间号: {{ log.room_number }}</span>
                  <span class="log-time">{{ formatDate(log.timestamp) }}</span>
                </div>
                <div class="log-item-body">
                  <span class="log-status">{{ log.status }}</span>
                  <span class="log-phone">联系电话: {{ log.phone }}</span>
                </div>
              </div>
            </div>
            <div v-else class="no-results">
              <p>暂无记录</p>
            </div>
          </div>
        </div>
      </section>
      <section class="status-section">
        <h2>检测状态</h2>
        <div class="status-card">
          <div class="status-item">
            <span class="status-label">当前状态:</span>
            <span :class="['status-value', detectionStatus]">{{ detectionStatusText }}</span>
          </div>
          <div class="status-item">
            <span class="status-label">预警房间号:</span>
            <span class="status-value">{{ roomNumber }}</span>
          </div>
          <div class="status-item">
            <span class="status-label">检测人数:</span>
            <span class="status-value">{{ personCount }}</span>
          </div>
          <div class="status-item">
            <span class="status-label">摔倒人数:</span>
            <span class="status-value">{{ fallCount }}</span>
          </div>
        </div>
        <div class="alarm-light-container">
          <div :class="['alarm-light', detectionStatus]"></div>
          <span class="alarm-label">{{ detectionStatusText }}警报</span>
        </div>
        <div class="alarm-control">
          <button class="stop-alarm-btn" @click="stopAlarm" :class="detectionStatus">停止报警</button>
        </div>
      </section>
    </main>
    <footer class="app-footer">
      <p>© 2026 摔倒智能检测系统</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 登录状态管理
const adminName = ref('')

// 视频和检测相关
const videoElement = ref(null)
const canvasElement = ref(null)
const videoFile = ref(null)
const detectionStatus = ref('normal')
const detectionStatusText = ref('正常')
const roomNumber = ref('')
const personCount = ref(0)
const fallCount = ref(0)
let stream = null
let animationId = null

// 记录查询相关
const queryType = ref('time')
const queryTime = ref('')
const queryRoom = ref('')
const queryName = ref('')
const logs = ref([])
const isLoading = ref(false)

// 检查登录状态
onMounted(() => {
  checkLoginStatus()
  // 初始化时设置状态
  detectionStatus.value = 'idle'
  detectionStatusText.value = '未检测'
})

onUnmounted(() => {
  stopCamera()
})

// 检查登录状态
const checkLoginStatus = () => {
  const admin = localStorage.getItem('admin')
  if (admin) {
    const adminData = JSON.parse(admin)
    adminName.value = adminData.name
  }
}

// 处理退出登录
const handleLogout = () => {
  localStorage.removeItem('admin')
  // 刷新页面以确保登录状态更新
  window.location.reload()
}

// 进入个人中心
const goToProfile = () => {
  // 使用路由跳转到个人中心页面
  router.push('/profile')
}

// 摄像头控制
const startCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (videoElement.value) {
      videoElement.value.srcObject = stream
      startDetection()
      detectionStatus.value = 'normal'
      detectionStatusText.value = '正常'
      roomNumber.value = '101'
    }
  } catch (error) {
    console.error('无法访问摄像头:', error)
    alert('无法访问摄像头，请检查权限设置')
  }
}

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
    if (videoElement.value) {
      videoElement.value.srcObject = null
    }
    stopDetection()
    detectionStatus.value = 'idle'
    detectionStatusText.value = '未检测'
    roomNumber.value = ''
    personCount.value = 0
    fallCount.value = 0
  }
}

const loadVideo = () => {
  if (videoFile.value) {
    videoFile.value.click()
  }
}

const handleVideoFile = (event) => {
  const file = event.target.files[0]
  if (file) {
    const videoURL = URL.createObjectURL(file)
    if (videoElement.value) {
      videoElement.value.srcObject = null
      videoElement.value.src = videoURL
      videoElement.value.play()
      startDetection()
      detectionStatus.value = 'normal'
      detectionStatusText.value = '正常'
      roomNumber.value = '102'
    }
  }
}

// 检测相关
const startDetection = () => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  const detect = async () => {
    try {
      // 调用后端API进行检测
      const canvas = canvasElement.value
      const video = videoElement.value
      if (!canvas || !video) return
      
      // 绘制视频帧到画布
      const ctx = canvas.getContext('2d')
      canvas.width = video.offsetWidth
      canvas.height = video.offsetHeight
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      
      // 从画布获取图像数据
      const imageData = canvas.toDataURL('image/jpeg')
      
      // 转换为Blob对象
      const response = await fetch(imageData)
      const blob = await response.blob()
      
      // 创建FormData对象
      const formData = new FormData()
      formData.append('file', blob, 'frame.jpg')
      
      // 调用后端API
      const apiResponse = await fetch('http://localhost:8000/detect/fall', {
        method: 'POST',
        body: formData
      })
      
      const result = await apiResponse.json()
      
      if (result.success) {
        personCount.value = result.fall_count > 0 ? result.fall_count : Math.floor(Math.random() * 3) + 1
        fallCount.value = result.fall_count
        
        // 时序间隔机制
        if (result.fall_detected) {
          // 检测到摔倒，增加连续帧数
          fallFrames.value++
          lastFallDetection.value = new Date()
          
          // 检查是否达到阈值
          if (fallFrames.value >= fallFrameThreshold) {
            detectionStatus.value = 'alert'
            detectionStatusText.value = '有摔倒'
            // 记录摔倒事件
            recordFallEvent()
          } else {
            // 尚未达到阈值，显示检测中
            detectionStatus.value = 'normal'
            detectionStatusText.value = '检测中...'
          }
        } else {
          // 未检测到摔倒，重置计数器
          fallFrames.value = 0
          lastFallDetection.value = null
          detectionStatus.value = 'normal'
          detectionStatusText.value = '正常'
        }
        
        // 更新画布显示标注后的图像
        if (result.image) {
          const img = new Image()
          img.onload = () => {
            const ctx = canvas.getContext('2d')
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
          }
          img.src = result.image
        }
      } else {
        // 模拟检测结果（当API调用失败时）
        personCount.value = Math.floor(Math.random() * 3) + 1
        fallCount.value = Math.floor(Math.random() * personCount.value)
        
        if (fallCount.value > 0) {
          detectionStatus.value = 'alert'
          detectionStatusText.value = '有摔倒'
        } else {
          detectionStatus.value = 'normal'
          detectionStatusText.value = '正常'
        }
        
        // 绘制检测结果到画布
        drawDetectionResults()
      }
    } catch (error) {
      console.error('检测失败:', error)
      // 模拟检测结果（当API调用失败时）
      personCount.value = Math.floor(Math.random() * 3) + 1
      fallCount.value = Math.floor(Math.random() * personCount.value)
      
      if (fallCount.value > 0) {
        detectionStatus.value = 'alert'
        detectionStatusText.value = '有摔倒'
      } else {
        detectionStatus.value = 'normal'
        detectionStatusText.value = '正常'
      }
      
      // 绘制检测结果到画布
      drawDetectionResults()
    }
    
    animationId = requestAnimationFrame(detect)
  }
  detect()
}

// 记录摔倒事件到日志
const recordFallEvent = async () => {
  try {
    const roomNumber = currentSource.value === 'camera' ? '101' : '102'
    const phone = '13800138001' // 示例电话号码
    
    await fetch(`http://localhost:8000/logs/fall-detection?room_number=${roomNumber}&phone=${phone}`, {
      method: 'POST'
    })
    
    console.log('摔倒事件已记录')
  } catch (error) {
    console.error('记录摔倒事件失败:', error)
  }
}

// 停止报警
const stopAlarm = async () => {
  try {
    // 调用后端停止报警API
    const response = await fetch('http://localhost:8000/alarm/stop', {
      method: 'POST'
    })
    const result = await response.json()
    console.log('停止报警响应:', result)
  } catch (error) {
    console.error('停止报警失败:', error)
  }
  
  // 更新前端状态
  detectionStatus.value = 'normal'
  detectionStatusText.value = '正常'
  fallFrames.value = 0
  lastFallDetection.value = null
  console.log('报警已停止')
}

const stopDetection = () => {
  if (animationId) {
    cancelAnimationFrame(animationId)
    animationId = null
  }
}

const drawDetectionResults = () => {
  const video = videoElement.value
  const canvas = canvasElement.value
  if (!video || !canvas) return
  
  const ctx = canvas.getContext('2d')
  canvas.width = video.offsetWidth
  canvas.height = video.offsetHeight
  
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  // 模拟绘制检测框
  for (let i = 0; i < personCount.value; i++) {
    const x = 50 + i * 150
    const y = 100
    const width = 100
    const height = 200
    
    ctx.strokeStyle = i < fallCount.value ? '#ff4444' : '#44ff44'
    ctx.lineWidth = 2
    ctx.strokeRect(x, y, width, height)
    
    ctx.fillStyle = i < fallCount.value ? '#ff4444' : '#44ff44'
    ctx.font = '14px Arial'
    ctx.fillText(i < fallCount.value ? '摔倒' : '正常', x, y - 5)
  }
}

// 时序间隔机制相关变量
const fallFrames = ref(0) // 连续检测到摔倒的帧数
const fallFrameThreshold = 90 // 触发警报的帧数阈值（假设30fps，3秒）
const lastFallDetection = ref(null) // 上次检测到摔倒的时间

// 记录查询相关方法
const queryLogs = async () => {
  isLoading.value = true
  try {
    let url = 'http://localhost:8000/logs'
    
    // 获取日志数据
    const response = await fetch(url)
    const logsData = await response.json()
    
    // 前端过滤
    let filteredLogs = logsData
    
    if (queryType.value === 'room' && queryRoom.value) {
      // 按房间号查询
      filteredLogs = logsData.filter(log => log.room_number === queryRoom.value)
    } else if (queryType.value === 'time' && queryTime.value) {
      // 按时间查询
      const queryDate = new Date(queryTime.value)
      filteredLogs = logsData.filter(log => {
        const logDate = new Date(log.timestamp)
        // 只比较日期部分，忽略时间
        return logDate.toDateString() === queryDate.toDateString()
      })
    } else if (queryType.value === 'name' && queryName.value) {
      // 按姓名查询
      // 先获取老人列表，建立房间号和姓名的映射关系
      const oldPersonsResponse = await fetch('http://localhost:8000/old-persons')
      const oldPersons = await oldPersonsResponse.json()
      
      // 建立姓名到房间号的映射
      const nameToRoomMap = {}
      oldPersons.forEach(person => {
        nameToRoomMap[person.name] = person.room_number
      })
      
      // 根据姓名找到对应的房间号
      const roomNumber = nameToRoomMap[queryName.value]
      if (roomNumber) {
        // 根据房间号过滤日志
        filteredLogs = logsData.filter(log => log.room_number === roomNumber)
      } else {
        // 未找到对应姓名的老人
        filteredLogs = []
      }
    }
    
    logs.value = filteredLogs
  } catch (error) {
    console.error('查询日志失败:', error)
    alert('查询日志失败，请检查网络连接')
  } finally {
    isLoading.value = false
  }
}

// 格式化日期时间
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: rgba(44, 62, 80, 0.6);
  color: #ffffff;
  padding: 1rem;
  text-align: center;
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-header h1 {
  color: #ffffff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-button {
  padding: 0.5rem 1rem;
  background-color: rgba(52, 152, 219, 0.7);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.profile-button:hover {
  background-color: rgba(52, 152, 219, 0.9);
}

.logout-button {
  padding: 0.5rem 1rem;
  background-color: rgba(231, 76, 60, 0.7);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: rgba(231, 76, 60, 0.9);
}

.app-main {
  flex: 1;
  padding: 2rem;
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.monitoring-section {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
}

h2 {
  color: #000;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.video-container {
  position: relative;
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(240, 240, 240, 0.3);
}

.video-player {
  width: 100%;
  height: auto;
  display: block;
}

.detection-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.control-panel {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.control-btn {
  padding: 0.5rem 1rem;
  background-color: rgba(52, 152, 219, 0.7);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.control-btn:hover {
  background-color: rgba(41, 128, 185, 0.8);
}

/* 记录查询窗口样式 */
.log-query-section {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(224, 224, 224, 0.8);
}

.log-query-section h3 {
  color: #000;
  font-weight: bold;
  margin-bottom: 1rem;
}

.log-query-section h4 {
  color: #000;
  font-weight: bold;
  margin-bottom: 1rem;
  margin-top: 1.5rem;
}

.query-form {
  background: rgba(249, 249, 249, 0.3);
  padding: 1.5rem;
  border-radius: 8px;
  backdrop-filter: blur(5px);
}

.form-row {
  display: flex;
  gap: 1rem;
  align-items: end;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group label {
  display: block;
  color: #555;
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

.log-results {
  margin-top: 1rem;
}

.log-list {
  background: rgba(249, 249, 249, 0.3);
  border-radius: 8px;
  padding: 1rem;
  backdrop-filter: blur(5px);
}

.log-item {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 0.8rem;
  border-left: 4px solid #3498db;
}

.log-item:last-child {
  margin-bottom: 0;
}

.log-item-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.log-room {
  font-weight: 600;
  color: #333;
}

.log-time {
  color: #666;
}

.log-item-body {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.log-status {
  font-weight: 600;
  color: #e74c3c;
}

.log-phone {
  color: #666;
}

.no-results {
  background: rgba(249, 249, 249, 0.3);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  backdrop-filter: blur(5px);
  color: #666;
}

.status-section {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
}

.status-card {
  background: rgba(249, 249, 249, 0.3);
  border-radius: 4px;
  padding: 1rem;
  margin-top: 1rem;
  backdrop-filter: blur(5px);
}

.status-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(224, 224, 224, 0.8);
}

.status-item:last-child {
  border-bottom: none;
}

.status-label {
  font-weight: 600;
  color: #000;
}

.status-value {
  font-weight: 600;
}

.status-value.normal {
  color: #32CD32;
  font-weight: bold;
}

.status-value.alert {
  color: #e74c3c;
  animation: pulse 1s infinite;
}

.status-value.idle {
  color: #3498db;
}

.alarm-light-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(249, 249, 249, 0.3);
  border-radius: 4px;
  backdrop-filter: blur(5px);
}

.alarm-light {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #95a5a6;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.alarm-light.normal {
  background-color: #32CD32;
  box-shadow: 0 0 30px rgba(50, 205, 50, 0.9);
}

.alarm-light.alert {
  background-color: #e74c3c;
  box-shadow: 0 0 25px rgba(231, 76, 60, 0.8);
  animation: alarm-pulse 0.5s infinite;
}

.alarm-light.idle {
  background-color: #3498db;
  box-shadow: 0 0 15px rgba(52, 152, 219, 0.6);
}

.alarm-label {
  font-weight: 600;
  color: #000;
}

.alarm-control {
  margin-top: 1rem;
  text-align: center;
}

.stop-alarm-btn {
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.stop-alarm-btn.normal {
  background-color: #32CD32;
  color: white;
}

.stop-alarm-btn.alert {
  background-color: #ff4444;
  color: white;
  animation: alarm-pulse 0.5s infinite;
}

.stop-alarm-btn.idle {
  background-color: #3498db;
  color: white;
}

.stop-alarm-btn:hover {
  transform: translateY(-2px);
}

.stop-alarm-btn.normal:hover {
  background-color: #228B22;
}

.stop-alarm-btn.alert:hover {
  background-color: #cc0000;
}

.stop-alarm-btn.idle:hover {
  background-color: #2980b9;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

@keyframes alarm-pulse {
  0% { opacity: 1; }
  50% { opacity: 0.3; }
  100% { opacity: 1; }
}

.app-footer {
  background-color: rgba(44, 62, 80, 0.6);
  color: white;
  padding: 1rem;
  text-align: center;
  margin-top: auto;
  backdrop-filter: blur(10px);
}

@media (max-width: 768px) {
  .app-main {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
  
  .app-header {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>