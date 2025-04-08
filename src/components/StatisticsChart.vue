<template>
  <div class="statistics-chart">
    <div class="chart-title">航迹分布统计</div>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script>
export default {
  name: 'StatisticsChart',
  data() {
    return {
      chart: null,
      timer: null,
      currentData: {
        trackCounts: [0, 0, 0, 0],
        lotwValues: [0, 0, 0, 0]
      },
      targetData: {
        trackCounts: [20, 15, 15, 50],
        lotwValues: [3, 2, 2, 9]
      }
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener('resize', this.resizeChart);
      
      // 直接显示最终数据，不使用动画
      this.currentData = { ...this.targetData };
      this.updateChart();
    });
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resizeChart);
    if (this.chart) {
      this.chart.dispose();
    }
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  methods: {
    initChart() {
      if (this.$refs.chartContainer) {
        this.chart = this.$echarts.init(this.$refs.chartContainer);
        this.updateChart();
      }
    },
    updateChart() {
      const option = {
        backgroundColor: 'transparent',
        title: [{
          text: '航迹数量',
          left: 'center',
          top: '10%',
          textStyle: {
            color: '#fff',
            fontSize: 14
          }
        }, {
          text: '总LOTW值',
          left: 'center',
          top: '55%',
          textStyle: {
            color: '#fff',
            fontSize: 14
          }
        }],
        grid: [{
          left: '10%',
          right: '12%',
          top: '15%',
          height: '35%',
          containLabel: true
        }, {
          left: '10%',
          right: '12%',
          top: '60%',
          height: '35%',
          containLabel: true
        }],
        legend: {
          textStyle: {
            color: '#fff'
          },
          right: 10,
          top: 10
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            let result = params[0].name + '<br/>';
            params.forEach(param => {
              let color = param.color;
              let marker = `<span style="display:inline-block;margin-right:5px;border-radius:50%;width:10px;height:10px;background-color:${color};"></span>`;
              result += marker + param.seriesName + ': ' + param.value + '<br/>';
            });
            return result;
          }
        },
        xAxis: [{
          gridIndex: 0,
          type: 'category',
          data: ['西北', '东北', '西南', '东南'],
          axisLine: {
            lineStyle: {
              color: '#4c98e2'
            }
          },
          axisLabel: {
            color: '#fff',
            fontSize: 12,
            rotate: 0
          }
        }, {
          gridIndex: 1,
          type: 'category',
          data: ['西北', '东北', '西南', '东南'],
          axisLine: {
            lineStyle: {
              color: '#4c98e2'
            }
          },
          axisLabel: {
            color: '#fff',
            fontSize: 12,
            rotate: 0
          }
        }],
        yAxis: [{
          gridIndex: 0,
          type: 'value',
          name: '数量',
          nameTextStyle: {
            color: '#fff',
            padding: [0, 30, 0, 0]
          },
          min: 0,
          max: 60,
          interval: 15,
          axisLine: {
            lineStyle: {
              color: '#4c98e2'
            }
          },
          axisLabel: {
            color: '#fff',
            inside: false,
            showMinLabel: true,
            showMaxLabel: true
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(76, 152, 226, 0.2)'
            }
          },
          position: 'left'
        }, {
          gridIndex: 1,
          type: 'value',
          name: '值',
          nameTextStyle: {
            color: '#fff',
            padding: [0, 30, 0, 0]
          },
          min: 0,
          max: 10,
          interval: 2,
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          axisLabel: {
            color: '#fff',
            inside: false, 
            showMinLabel: true,
            showMaxLabel: true
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.2)'
            }
          },
          position: 'left'
        }],
        series: [
          {
            name: '航迹数量',
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            barWidth: '30%',
            data: this.currentData.trackCounts,
            itemStyle: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#00b3ff' },
                { offset: 1, color: '#0056b3' }
              ]),
              borderRadius: [4, 4, 0, 0]
            },
            emphasis: {
              itemStyle: {
                color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#29cdff' },
                  { offset: 1, color: '#0083ff' }
                ])
              }
            },
            markLine: {
              silent: true,
              symbol: ['none', 'none'],
              lineStyle: {
                color: '#00ffff',
                type: 'solid',
                width: 1,
                opacity: 0.3
              },
              data: [
                { type: 'max', name: '最大值', valueIndex: 0 }
              ]
            }
          },
          {
            name: '总LOTW值',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            barWidth: '30%',
            data: this.currentData.lotwValues,
            itemStyle: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#ff9f43' },
                { offset: 1, color: '#ff5e57' }
              ]),
              borderRadius: [4, 4, 0, 0]
            },
            emphasis: {
              itemStyle: {
                color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#ffbe76' },
                  { offset: 1, color: '#ff7979' }
                ])
              }
            },
            markLine: {
              silent: true,
              symbol: ['none', 'none'],
              lineStyle: {
                color: '#00ffff',
                type: 'solid',
                width: 1,
                opacity: 0.3
              },
              data: [
                { type: 'max', name: '最大值', valueIndex: 0 }
              ]
            }
          }
        ]
      };

      this.chart.setOption(option);
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  }
};
</script>

<style scoped>
.statistics-chart {
  width: 100%;
  height: 100%;
  position: relative;
  animation: fadeInScale 0.6s ease-out;
}

.chart-title {
  position: absolute;
  top: 10px;
  left: 20px;
  font-size: 16px;
  color: #fff;
  z-index: 3;
}

.chart-container {
  width: 100%;
  height: 100%;
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