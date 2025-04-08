<template>
  <div class="track-chart">
    <div class="chart-title">航迹运行态势</div>
    <div ref="chartContainer" class="chart-container"></div>
    <div class="chart-controls">
      <div class="zoom-controls">
        <button @click="zoomIn" class="zoom-button">+</button>
        <button @click="zoomOut" class="zoom-button">-</button>
      </div>
      <div class="track-info">
        <span class="track-count">当前航迹：{{ trackCount }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrackChart',
  props: {
    // 添加新的属性来控制动画暂停
    pauseAnimation: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      chart: null,
      trackCount: 5,
      animationTimer: null,
      tracks: [],
      zoom: 1,
      isDataFromFile: false,
      dataInfo: null,
      // 图表参数
      chartParams: {
        resamplePoints: 200,
        centerAreaLength: 20,
        neighborRadius: 5,
        minPoints: 5
      }
    };
  },
  mounted() {
    this.initChart();
    window.addEventListener('resize', this.resizeChart);
    
    // 启动动画
    this.startTrackAnimation();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resizeChart);
    if (this.chart) {
      this.chart.dispose();
    }
    if (this.animationTimer) {
      clearInterval(this.animationTimer);
    }
  },
  methods: {
    initChart() {
      this.chart = this.$echarts.init(this.$refs.chartContainer);
      this.updateChart();
    },
    updateChart() {
      // 方向和名称
      const directions = [
        { angle: Math.PI * 0.75, color: '#00ff00', name: '西北' }, // 西北
        { angle: Math.PI * 0.25, color: '#ffff00', name: '东北' }, // 东北
        { angle: Math.PI * 1.25, color: '#ff0000', name: '西南' }, // 西南
        { angle: Math.PI * 1.75, color: '#00ffff', name: '东南' }, // 东南
        { angle: Math.PI * 1.0, color: '#ffffff', name: '西' }     // 额外航迹
      ];
      
      // 初始化航迹数据
      if (this.tracks.length === 0) {
        directions.forEach((dir, i) => {
          this.tracks.push({
            data: this.generateDirectionalTrack(dir.angle, 400000),
            color: dir.color,
            name: dir.name,
            currentIndex: 5 // 从第5个点开始显示
          });
        });
      }
      
      // 准备系列数据
      const series = this.tracks.map(track => {
        return {
          name: track.name,
          type: 'scatter',
          data: track.data.slice(0, track.currentIndex),
          symbolSize: 4,
          symbol: 'circle',
          itemStyle: {
            color: track.color
          },
          emphasis: {
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 2,
              shadowColor: track.color,
              shadowBlur: 10
            }
          }
        };
      });
      
      // 添加轨迹线
      const lineSeries = this.tracks.map(track => {
        return {
          name: track.name + '轨迹',
          type: 'line',
          data: track.data.slice(0, track.currentIndex),
          showSymbol: false,
          lineStyle: {
            color: track.color,
            width: 1,
            opacity: 0.5
          },
          emphasis: {
            lineStyle: {
              width: 2,
              opacity: 1
            }
          },
          zlevel: 1
        };
      });
      
      series.push(...lineSeries);
      
      // 雷达背景圆圈
      series.push({
        type: 'scatter',  // 使用普通scatter代替effectScatter
        coordinateSystem: 'cartesian2d',
        zlevel: 0,
        symbolSize: function (val) {
          return 400000 / 5000;
        },
        // 移除rippleEffect
        itemStyle: {
          color: 'rgba(0, 179, 255, 0.1)',  // 降低透明度
          shadowBlur: 0
        },
        data: [[0, 0]]
      });
      
      // 添加中心点
      series.push({
        type: 'scatter',
        zlevel: 2,
        symbolSize: 10,
        itemStyle: {
          color: '#00b3ff',
          shadowBlur: 10,
          shadowColor: '#00b3ff'
        },
        data: [[0, 0]]
      });
      
      // 根据参数添加中心区域边长可视化
      if (this.chartParams.centerAreaLength > 0) {
        const centerLength = this.chartParams.centerAreaLength * 1000; // 转换为米
        series.push({
          name: '中心区域',
          type: 'line',
          zlevel: 0,
          lineStyle: {
            color: 'rgba(76, 152, 226, 0.5)',
            width: 1,
            type: 'dashed'
          },
          symbol: 'none',
          data: [
            [-centerLength, -centerLength],
            [centerLength, -centerLength],
            [centerLength, centerLength],
            [-centerLength, centerLength],
            [-centerLength, -centerLength]
          ]
        });
      }

      const option = {
        backgroundColor: 'transparent',
        grid: {
          left: '5%',
          right: '5%',
          top: '30px',
          bottom: '40px',
          containLabel: true
        },
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            if (params.seriesName.includes('轨迹')) return '';
            if (params.seriesName === '中心区域') return '中心区域边界';
            
            if (params.value[0] === 0 && params.value[1] === 0) {
              return '中心点';
            }
            
            return `${params.seriesName}方向<br/>
                    X: ${(params.value[0]/1000).toFixed(1)}km<br/>
                    Y: ${(params.value[1]/1000).toFixed(1)}km`;
          }
        },
        legend: {
          data: directions.map(d => d.name),
          right: 10,
          top: 0,
          textStyle: {
            color: '#fff'
          },
          itemWidth: 10,
          itemHeight: 10,
          selected: {
            '中心区域': true
          }
        },
        xAxis: {
          type: 'value',
          name: 'X/km',
          nameLocation: 'middle',
          nameGap: 30,
          nameTextStyle: {
            color: '#fff',
            fontSize: 14,
            padding: [10, 0, 0, 0]
          },
          min: -100000 * (1/this.zoom),
          max: 150000 * (1/this.zoom),
          interval: 50000 * (1/this.zoom),
          axisLine: {
            lineStyle: {
              color: '#4c98e2'
            }
          },
          axisLabel: {
            color: '#fff',
            formatter: function(value) {
              return (value / 1000).toFixed(1);
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(76, 152, 226, 0.2)'
            }
          }
        },
        yAxis: {
          type: 'value',
          name: 'Y/km',
          nameLocation: 'middle',
          nameGap: 45,
          nameTextStyle: {
            color: '#fff',
            fontSize: 14,
            padding: [0, 0, 10, 0]
          },
          min: -150000 * (1/this.zoom),
          max: 200000 * (1/this.zoom),
          interval: 50000 * (1/this.zoom),
          axisLine: {
            lineStyle: {
              color: '#4c98e2'
            }
          },
          axisLabel: {
            color: '#fff',
            formatter: function(value) {
              return (value / 1000).toFixed(1);
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(76, 152, 226, 0.2)'
            }
          }
        },
        series: series
      };

      this.chart.setOption(option, true);
    },
    generateDirectionalTrack(angle, length) {
      const points = [];
      // 起点
      let x = 0;
      let y = 0;
      
      // 方向向量
      const dx = Math.cos(angle) * (length / 50);
      const dy = Math.sin(angle) * (length / 50);
      
      // 根据重采样点数调整点的数量和间隔
      const pointCount = Math.max(30, Math.min(100, this.chartParams.resamplePoints / 4));
      
      // 生成航迹点
      for (let i = 0; i < pointCount; i++) {
        const noiseScale = Math.max(2000, Math.min(15000, 20000 - this.chartParams.resamplePoints * 10));
        x += dx + (Math.random() - 0.5) * noiseScale;
        y += dy + (Math.random() - 0.5) * noiseScale;
        points.push([x, y]);
      }
      
      return points;
    },
    startTrackAnimation() {
      if (this.animationTimer) {
        clearInterval(this.animationTimer);
      }
      
      this.animationTimer = setInterval(() => {
        // 检查是否暂停动画
        if (this.pauseAnimation) {
          return;
        }
        
        let anyActive = false;
        this.tracks.forEach(track => {
          if (track.currentIndex < track.data.length - 1) {
            track.currentIndex++;
            anyActive = true;
          }
        });
        
        if (anyActive) {
          this.updateChart();
        } else {
          clearInterval(this.animationTimer);
        }
      }, 200);
    },
    stopTrackAnimation() {
      if (this.animationTimer) {
        clearInterval(this.animationTimer);
        this.animationTimer = null;
      }
    },
    zoomIn() {
      if (this.zoom < 4) {
        this.zoom *= 1.5;
        this.updateChart();
      }
    },
    zoomOut() {
      if (this.zoom > 0.5) {
        this.zoom /= 1.5;
        this.updateChart();
      }
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    },
    updateData(data) {
      if (!data) return;
      
      console.log("更新航迹图数据:", data);
      this.dataInfo = data;
      this.isDataFromFile = true;
      this.trackCount = data.trackCount || this.trackCount;
      
      // 清除现有动画
      if (this.animationTimer) {
        clearInterval(this.animationTimer);
        this.animationTimer = null;
      }
      
      // 重置轨迹数据
      this.tracks = [];
      
      // 基于文件中的数据生成新轨迹
      // 这里根据MAT文件的轨迹数据应当重新生成轨迹
      // 由于我们没有实际解析MAT文件，这里仅进行模拟
      
      // 模拟生成更多的轨迹
      const directions = [
        { angle: Math.PI * 0.75, color: '#00ff00', name: '西北', weight: 0.5 },
        { angle: Math.PI * 0.25, color: '#ffff00', name: '东北', weight: 0.5 },
        { angle: Math.PI * 1.25, color: '#ff0000', name: '西南', weight: 0.5 },
        { angle: Math.PI * 1.75, color: '#00ffff', name: '东南', weight: 3 } // 东南方向权重更高
      ];
      
      // 多生成几个航迹方向
      const extraDirs = [
        { angle: Math.PI * 0.5, color: '#ff00ff', name: '北', weight: 0.3 },
        { angle: Math.PI * 1.0, color: '#ffffff', name: '西', weight: 0.3 },
        { angle: Math.PI * 1.5, color: '#ffaa00', name: '南', weight: 0.3 },
        { angle: Math.PI * 0.0, color: '#00ffaa', name: '东', weight: 0.3 }
      ];
      
      const allDirs = [...directions, ...extraDirs];
      const totalWeight = allDirs.reduce((sum, dir) => sum + dir.weight, 0);
      
      // 生成100条航迹
      const totalTracks = Math.min(100, this.trackCount);
      let trackCount = 0;
      
      // 根据权重分配各方向的航迹数量
      allDirs.forEach(dir => {
        // 计算该方向应分配的航迹数量
        const dirTrackCount = Math.floor((dir.weight / totalWeight) * totalTracks);
        
        // 为该方向生成航迹
        for (let i = 0; i < dirTrackCount; i++) {
          if (trackCount >= totalTracks) break; // 确保不超过总航迹数
          
          const scale = Math.random() * 0.5 + 0.75; // 0.75 - 1.25的随机系数
          const angleVariation = (Math.random() - 0.5) * 0.2; // 在方向上添加小的随机变化
          
          this.tracks.push({
            data: this.generateDirectionalTrack(dir.angle + angleVariation, 400000 * scale),
            color: dir.color,
            name: `${dir.name}航迹${i+1}`,
            currentIndex: 5 // 从第5个点开始显示
          });
          
          trackCount++;
        }
      });
      
      // 如果由于取整导致的航迹总数不足，则在东南方向添加剩余航迹
      while (trackCount < totalTracks) {
        const eastSouthDir = directions[3]; // 东南方向
        const scale = Math.random() * 0.5 + 0.75;
        const angleVariation = (Math.random() - 0.5) * 0.2;
        
        this.tracks.push({
          data: this.generateDirectionalTrack(eastSouthDir.angle + angleVariation, 400000 * scale),
          color: eastSouthDir.color,
          name: `${eastSouthDir.name}航迹${trackCount+1}`,
          currentIndex: 5
        });
        
        trackCount++;
      }
      
      // 重新启动动画
      this.startTrackAnimation();
    },
    // 更新图表参数
    updateChartParams(params) {
      if (!params) return;
      
      console.log("更新图表参数:", params);
      
      // 更新参数
      this.chartParams = {
        ...this.chartParams,
        ...params
      };
      
      // 如果有航迹数据，重新生成航迹
      if (this.tracks.length > 0) {
        // 停止现有动画
        if (this.animationTimer) {
          clearInterval(this.animationTimer);
          this.animationTimer = null;
        }
        
        // 清空现有轨迹
        this.tracks = [];
        
        // 重新加载数据（如果有）
        if (this.dataInfo) {
          this.updateData(this.dataInfo);
        } else {
          // 否则重新初始化
          this.initChart();
        }
      } else {
        // 否则只更新图表
        this.updateChart();
      }
    }
  }
};
</script>

<style scoped>
.track-chart {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 2;
}

.chart-title {
  position: absolute;
  top: 0;
  left: 20px;
  font-size: 16px;
  color: #fff;
  z-index: 3;
}

.chart-controls {
  position: absolute;
  bottom: 10px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 15px;
  z-index: 3;
}

.zoom-controls {
  display: flex;
  gap: 5px;
}

.zoom-button {
  width: 24px;
  height: 24px;
  border: 1px solid #4c98e2;
  background-color: rgba(1, 42, 87, 0.8);
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 4px;
  font-size: 16px;
  transition: all 0.2s;
}

.zoom-button:hover {
  background-color: rgba(0, 179, 255, 0.5);
}

.track-info {
  font-size: 14px;
  color: #fff;
}

.track-count {
  color: #00b3ff;
  font-weight: bold;
}

.radar-effect {
  display: none;
}

.radar-effect::before {
  display: none;
}

@keyframes radarScan {
  0% {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}
</style> 