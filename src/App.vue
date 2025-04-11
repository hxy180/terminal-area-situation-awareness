<script>
import TrackChart from './components/TrackChart.vue';
import StatisticsChart from './components/StatisticsChart.vue';
import ParameterDisplay from './components/ParameterDisplay.vue';
import DirectionPanel from './components/DirectionPanel.vue';
import ControlButtons from './components/ControlButtons.vue';
import TechBackground from './components/TechBackground.vue';
import DataLoading from './components/DataLoading.vue';
import ParamSettingDialog from './components/ParamSettingDialog.vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'App',
  components: {
    TrackChart,
    StatisticsChart,
    ParameterDisplay,
    DirectionPanel,
    ControlButtons,
    TechBackground,
    DataLoading,
    ParamSettingDialog
  },
  data() {
    return {
      loading: true,
      loadingText: '系统数据初始化中...',
      timeDisplay: '',
      headerInfo: {
        date: '',
        time: '',
        status: '系统运行正常'
      },
      selectedFile: null,
      trackData: null,
      showParamDialog: false,
      showMetrics: false,
      showParams: false,
      showStatistics: false,
      showTrackChart: false,
      analyzeLoading: false,
      algorithmParams: {
        resamplePoints: 200,
        centerAreaLength: 20,
        neighborRadius: 5,
        minPoints: 5
      }
    };
  },
  mounted() {
    // 模拟加载完成
    setTimeout(() => {
      this.loading = false;
    }, 3000);
    
    // 更新时间显示
    this.updateTime();
    setInterval(this.updateTime, 1000);
  },
  methods: {
    handleButtonClick(action, file) {
      switch(action) {
        case 'selectData':
          if (file) {
            this.selectedFile = file;
            this.handleMatFile(file);
            // 重置所有显示状态
            this.showMetrics = false;
            this.showParams = false;
            this.showStatistics = false;
            this.showTrackChart = false;
            // 重置算法参数中的指标值
            const { resamplePoints, centerAreaLength, neighborRadius, minPoints } = this.algorithmParams;
            this.algorithmParams = {
              resamplePoints,
              centerAreaLength,
              neighborRadius,
              minPoints
            };
          }
          break;
        case 'setParams':
          this.showParamDialog = true;
          this.showParams = true;
          break;
        case 'identifyTraffic':
          if (!this.trackData) {
            ElMessage({
              message: '请先选择有效的MAT格式航迹数据',
              type: 'warning'
            });
            return;
          }
          
          this.loading = true;
          this.loadingText = '交通流识别算法运行中...';
          setTimeout(() => {
            this.loading = false;
            
            // 更新算法结果指标并显示
            this.updateAlgorithmMetrics();
            this.showMetrics = true;
            this.showParams = true;
            this.showTrackChart = true;
            
            // 在识别交通流后更新TrackChart数据
            this.$nextTick(() => {
              if (this.$refs.trackChart) {
                this.$refs.trackChart.updateData(this.trackData);
              }
            });
            
            ElMessage({
              message: '交通流识别完成',
              type: 'success'
            });
          }, 3000);
          break;
        case 'analyzeResults':
          if (!this.trackData) {
            ElMessage({
              message: '请先选择有效的MAT格式航迹数据并识别交通流',
              type: 'warning'
            });
            return;
          }
          
          // 显示加载动画
          this.analyzeLoading = true;
          this.loadingText = '分析结果生成中...';
          this.loading = true;
          
          // 模拟数据分析过程
          setTimeout(() => {
            this.loading = false;
            this.analyzeLoading = false;
            
            // 显示统计图表
            this.showStatistics = true;
            
            ElMessage({
              message: '分析结果已生成',
              type: 'success'
            });
          }, 2000);  // 2秒的分析时间
          break;
      }
    },
    handleFileError(errorMsg) {
      ElMessage({
        message: errorMsg,
        type: 'error'
      });
    },
    handleMatFile(file) {
      this.loading = true;
      this.loadingText = `正在加载 ${file.name}...`;
      
      // 使用FileReader读取文件
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          // 这里只是模拟处理，实际需要使用适当的库解析MAT文件
          // 例如 matjs, netcdf.js 等专业库
          console.log("文件加载完成，大小:", e.target.result.byteLength, "字节");
          
          // 模拟解析过程
          setTimeout(() => {
            // 模拟解析成功
            this.trackData = {
              fileName: file.name,
              trackCount: 100,
              timestamp: new Date().toISOString()
            };
            
            this.loading = false;
            ElMessage({
              message: `已成功加载航迹数据: ${file.name}`,
              type: 'success'
            });
            
            // 更新系统状态
            this.headerInfo.status = '数据已加载，可进行分析';
            
            // 不再直接更新TrackChart，只在点击"识别交通流"时更新
            // this.$refs.trackChart?.updateData(this.trackData);
            
          }, 2000);
        } catch (error) {
          this.loading = false;
          console.error('MAT文件解析失败:', error);
          ElMessage({
            message: 'MAT文件解析失败，请确保文件格式正确',
            type: 'error'
          });
        }
      };
      
      reader.onerror = () => {
        this.loading = false;
        ElMessage({
          message: '文件读取失败，请重试',
          type: 'error'
        });
      };
      
      // 读取文件为ArrayBuffer，适合二进制格式如MAT
      reader.readAsArrayBuffer(file);
    },
    updateTime() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const seconds = String(now.getSeconds()).padStart(2, '0');
      
      this.headerInfo.date = `${year}-${month}-${day}`;
      this.headerInfo.time = `${hours}:${minutes}:${seconds}`;
    },
    onLoadingComplete() {
      ElMessage({
        message: '数据加载完成',
        type: 'success'
      });
    },
    // 保存参数设置
    saveParams(params) {
      console.log('参数设置已保存:', params);
      this.algorithmParams = { ...params };
      
      // 应用参数修改
      this.$refs.trackChart?.updateChartParams?.(params);
      
      ElMessage({
        message: '参数设置已保存',
        type: 'success'
      });
    },
    // 根据参数更新算法结果指标
    updateAlgorithmMetrics() {
      // 模拟计算不同参数下的指标
      // 在实际应用中，这应该是基于算法计算的结果
      
      // 获取当前参数
      const { resamplePoints, centerAreaLength, neighborRadius, minPoints } = this.algorithmParams;
      
      // 模拟计算 - 这里使用简单算法根据参数生成一些"看起来合理"的指标值
      const dbi = (0.5 - Math.pow(neighborRadius / 15, 0.8) * 0.3).toFixed(4);
      const ch = Math.floor(1000 + resamplePoints * 10 + centerAreaLength * 20);
      const sc = (0.7 + (minPoints / 20) * 0.3).toFixed(4);
      
      // 更新指标参数
      this.algorithmParams = {
        ...this.algorithmParams,
        dbi,
        ch,
        sc
      };
    }
  }
}
</script>

<template>
  <div class="system-container">
    <TechBackground />
    <DataLoading 
      :show="loading" 
      :text="loadingText"
      @loading-complete="onLoadingComplete" 
    />
    
    <header class="header">
      <div class="header-left">
        <div class="system-status">
          状态: <span class="status-value">{{ headerInfo.status }}</span>
        </div>
        <div v-if="selectedFile" class="file-info">
          当前数据: <span class="file-name">{{ selectedFile.name }}</span>
        </div>
      </div>
      <h1 v-motion :initial="{ opacity: 0, y: -50 }" :enter="{ opacity: 1, y: 0, transition: { delay: 300, duration: 500 } }" class="title">终端区运行态势感知系统</h1>
      <div class="header-right">
        <div class="time-display">
          <div class="date">{{ headerInfo.date }}</div>
          <div class="time">{{ headerInfo.time }}</div>
        </div>
    </div>
  </header>

    <main class="content">
      <div v-motion :initial="{ opacity: 0, x: -50 }" :enter="{ opacity: 1, x: 0, transition: { delay: 500, duration: 500 } }" class="left-panel">
        <div class="panel track-panel">
          <Transition name="fade">
            <TrackChart 
              v-if="showTrackChart"
              ref="trackChart" 
              :pauseAnimation="showParamDialog"
            />
            <div v-else class="no-data-placeholder track-placeholder">
              <div class="placeholder-text">请点击"选择数据"上传数据，然后点击"识别交通流"查看航迹运行态势</div>
            </div>
          </Transition>
          <Transition name="slide-fade">
            <div class="parameter-display-container" v-show="showParams">
              <ParameterDisplay 
                :customParams="algorithmParams"
                :showMetrics="showMetrics"
              />
            </div>
          </Transition>
        </div>
        <div class="panel control-panel">
          <ControlButtons 
            @button-click="handleButtonClick" 
            @file-error="handleFileError"
          />
        </div>
      </div>
      
      <div v-motion :initial="{ opacity: 0, x: 50 }" :enter="{ opacity: 1, x: 0, transition: { delay: 700, duration: 500 } }" class="right-panel">
        <div class="direction-panels">
          <Transition name="fade">
            <div v-if="showStatistics" class="direction-container">
              <DirectionPanel title="航迹数量最多" direction="东南方向" />
              <DirectionPanel title="航迹差异最大" direction="东南方向" />
            </div>
            <div v-else class="no-data-placeholder direction-placeholder">
              <div class="placeholder-text">请点击"分析结果"按钮查看方向分析</div>
            </div>
          </Transition>
        </div>
        <div class="panel chart-panel">
          <Transition name="fade">
            <StatisticsChart v-if="showStatistics" />
            <div v-else class="no-data-placeholder">
              <div class="placeholder-text">请点击"分析结果"按钮查看数据分析</div>
            </div>
          </Transition>
        </div>
      </div>
  </main>
    
    <footer class="footer">
      <div class="tech-info">
        <span v-if="trackData">航迹数：{{ trackData.trackCount }} | </span>
        采样率：1s | 处理状态：{{ headerInfo.status }}
      </div>
      <div class="copyright">© 2025 终端区运行态势感知系统</div>
    </footer>
    
    <!-- 参数设置对话框 -->
    <ParamSettingDialog 
      v-model:visible="showParamDialog"
      :defaultParams="algorithmParams"
      @save="saveParams"
    />
  </div>
</template>

<style>
.parameter-display-container {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 5px;
  background-color: rgba(1, 42, 87, 0.9);
  border: 1px solid var(--border-color);
  border-radius: 5px;
  width: 220px;
  backdrop-filter: blur(5px);
  box-shadow: 0 0 15px rgba(0, 179, 255, 0.3);
  z-index: 100;
}

.system-container {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
  position: relative;
}

.content {
  display: flex;
  height: calc(100vh - 120px);
  padding: 20px;
  gap: 20px;
}

.left-panel {
  flex: 7;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-panel {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.track-panel {
  flex: 1;
  position: relative;
}

.control-panel {
  height: 80px;
}

.direction-panels {
  display: flex;
  height: 180px;
}

.chart-panel {
  flex: 1;
}

.header {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  padding: 0 30px;
  background: linear-gradient(90deg, rgba(1, 42, 87, 0.8) 0%, rgba(0, 102, 204, 0.4) 50%, rgba(1, 42, 87, 0.8) 100%);
}

.header-left, .header-right {
  width: 200px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.system-status {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
  color: #ffffff;
}

.file-info {
  font-size: 12px;
  color: #cccccc;
}

.file-name {
  color: #66ccff;
  font-weight: bold;
}

.status-value {
  color: #2ecc71;
  font-weight: bold;
  white-space: nowrap;
}

.time-display {
  font-size: 14px;
  color: #ffffff;
  text-align: right;
}

.date, .time {
  margin: 2px 0;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: var(--text-color);
  text-shadow: 0 0 10px var(--highlight-color);
  letter-spacing: 2px;
  position: relative;
  animation: glow 1.5s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    text-shadow: 0 0 5px #00b3ff, 0 0 10px #00b3ff;
  }
  to {
    text-shadow: 0 0 10px #00b3ff, 0 0 20px #00b3ff, 0 0 30px #00b3ff;
  }
}

.panel {
  background-color: rgba(1, 42, 87, 0.7);
  border: 1px solid var(--border-color);
  border-radius: 5px;
  box-shadow: 0 0 15px rgba(0, 179, 255, 0.2);
  padding: 15px;
  position: relative;
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
}

.panel:hover {
  box-shadow: 0 0 20px rgba(0, 179, 255, 0.4);
}

.footer {
  height: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  background: rgba(1, 42, 87, 0.8);
  color: #ccc;
  font-size: 12px;
  border-top: 1px solid var(--border-color);
}

.tech-info, .copyright {
  max-width: 50%;
}

/* 添加占位符的样式 */
.no-data-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(1, 42, 87, 0.5);
  border-radius: 5px;
}

.track-placeholder {
  background-image: linear-gradient(rgba(1, 42, 87, 0.5), rgba(0, 102, 204, 0.3));
}

.placeholder-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  text-align: center;
  padding: 20px;
  max-width: 80%;
}

/* 添加淡入淡出过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 添加脉冲边框效果 */
.track-panel::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border: 2px solid transparent;
  border-radius: 7px;
  background: linear-gradient(45deg, rgba(0, 179, 255, 0), rgba(0, 179, 255, 0.8), rgba(0, 179, 255, 0)) border-box;
  animation: borderPulse 4s linear infinite;
  z-index: -1;
}

@keyframes borderPulse {
  0% {
    opacity: 0.2;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.2;
  }
}

/* 添加过渡动画样式 */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

.slide-fade-enter-to,
.slide-fade-leave-from {
  transform: translateX(0);
  opacity: 1;
}

.direction-container {
    display: flex;
  gap: 20px;
  width: 100%;
  height: 100%;
  animation: fadeInScale 0.6s ease-out;
}

.direction-placeholder {
  height: 100%;
  background-color: rgba(1, 42, 87, 0.7);
  border: 1px solid var(--border-color);
  border-radius: 5px;
  box-shadow: 0 0 15px rgba(0, 179, 255, 0.2);
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
}

.direction-placeholder:hover {
  box-shadow: 0 0 20px rgba(0, 179, 255, 0.4);
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>