<template>
  <div class="statistics-chart">
    <div class="chart-title">航迹分布统计</div>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script>
// 图表配置
const CHART_CONFIG = {
  DIRECTIONS: ['西北', '东北', '西南', '东南'],
  COLORS: {
    TRACK: {
      START: '#00b3ff',
      END: '#0056b3',
      HOVER_START: '#29cdff',
      HOVER_END: '#0083ff'
    },
    LOTW: {
      START: '#ff9f43',
      END: '#ff5e57',
      HOVER_START: '#ffbe76',
      HOVER_END: '#ff7979'
    }
  },
  AXIS: {
    TRACK: {
      MAX: 200,
      INTERVAL: 50  
    },
    LOTW: {
      MAX: 1200000,
      INTERVAL: 300000
    }
  }
};

export default {
  name: 'StatisticsChart',
  
  data() {
    return {
      chart: null,
      chartData: {
        trackCounts: [0, 0, 0, 0],
        lotwValues: [0, 0, 0, 0]
      }
    };
  },

  async mounted() {
    this.initChart();
    try {
      const response = await fetch('/api/analysis-results');
      const data = await response.json();
      this.updateChartData(data);
    } catch (error) {
      console.error('读取分析结果失败:', error);
      // 使用默认数据
      this.updateChartData();
    }
    window.addEventListener('resize', this.resizeChart);
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.resizeChart);
    this.disposeChart();
  },

  methods: {
    initChart() {
      if (this.$refs.chartContainer) {
        this.chart = this.$echarts.init(this.$refs.chartContainer);
      }
    },

    disposeChart() {
      if (this.chart) {
        this.chart.dispose();
        this.chart = null;
      }
    },

    updateChartData(newData) {

      if (newData) {
        this.chartData = { ...newData };
      } else {
        this.chartData = {
          trackCounts: [60, 15, 15, 50],
          lotwValues: [3, 2, 2, 9]
        };
      }
      this.updateChart();
    },

    createChartOption() {
      return {
        backgroundColor: 'transparent',
        title: this.createTitleOption(),
        grid: this.createGridOption(),
        tooltip: this.createTooltipOption(),
        xAxis: this.createXAxisOption(),
        yAxis: this.createYAxisOption(),
        series: this.createSeriesOption()
      };
    },

    createTitleOption() {
      return [{
        text: '航迹数量',
        left: 'center',
        top: '10%',
        textStyle: { color: '#fff', fontSize: 14 }
      }, {
        text: '最大DTW距离',
        left: 'center',
        top: '55%',
        textStyle: { color: '#fff', fontSize: 14 }
      }];
    },

    createGridOption() {
      return [{
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
      }];
    },

    createTooltipOption() {
      return {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        formatter: this.formatTooltip
      };
    },

    formatTooltip(params) {
      let result = params[0].name + '<br/>';
      params.forEach(param => {
        const marker = `<span style="display:inline-block;margin-right:5px;border-radius:50%;width:10px;height:10px;background-color:${param.color};"></span>`;
        result += marker + param.seriesName + ': ' + param.value + '<br/>';
      });
      return result;
    },

    createXAxisOption() {
      const baseAxis = {
        type: 'category',
        data: CHART_CONFIG.DIRECTIONS,
        axisLine: { lineStyle: { color: '#4c98e2' } },
        axisLabel: { color: '#fff', fontSize: 12, rotate: 0 }
      };
      return [
        { ...baseAxis, gridIndex: 0 },
        { ...baseAxis, gridIndex: 1 }
      ];
    },

    createYAxisOption() {
      return [{
        gridIndex: 0,
        type: 'value',
        name: '数量',
        ...this.createBaseYAxisOption(CHART_CONFIG.AXIS.TRACK)
      }, {
        gridIndex: 1,
        type: 'value',
        name: '值',
        ...this.createBaseYAxisOption(CHART_CONFIG.AXIS.LOTW)
      }];
    },

    createBaseYAxisOption(config) {
      return {
        nameTextStyle: { color: '#fff', padding: [0, 30, 0, 0] },
        min: 0,
        max: config.MAX,
        interval: config.INTERVAL,
        axisLine: { lineStyle: { color: '#4c98e2' } },
        axisLabel: {
          color: '#fff',
          inside: false,
          showMinLabel: true,
          showMaxLabel: true
        },
        splitLine: { lineStyle: { color: 'rgba(76, 152, 226, 0.2)' } },
        position: 'left'
      };
    },

    createSeriesOption() {
      return [
        this.createBarSeries('航迹数量', 0, 0, this.chartData.trackCounts, CHART_CONFIG.COLORS.TRACK),
        this.createBarSeries('最大DTW距离', 1, 1, this.chartData.lotwValues, CHART_CONFIG.COLORS.LOTW)
      ];
    },

    createBarSeries(name, xIndex, yIndex, data, colors) {
      return {
        name,
        type: 'bar',
        xAxisIndex: xIndex,
        yAxisIndex: yIndex,
        barWidth: '30%',
        data,
        itemStyle: {
          color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: colors.START },
            { offset: 1, color: colors.END }
          ]),
          borderRadius: [4, 4, 0, 0]
        },
        emphasis: {
          itemStyle: {
            color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: colors.HOVER_START },
              { offset: 1, color: colors.HOVER_END }
            ])
          }
        },
        label: {
          show: false,
          position: 'top',
          color: '#fff',
          fontSize: 12
        },
        emphasis: {
          label: {
            show: true
          },
          itemStyle: {
            color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: colors.HOVER_START },
              { offset: 1, color: colors.HOVER_END }
            ])
          }
        }
      };
    },

    createMarkLineOption() {
      return {
        silent: true,
        symbol: ['none', 'none'],
        label: {
          show: false  // 隐藏标记线上的数字标签
        },
        lineStyle: {
          color: '#00ffff',
          type: 'solid',
          width: 1,
          opacity: 0.3
        },
        data: [{ type: 'max', name: '最大值', valueIndex: 0 }]
      };
    },

    updateChart() {
      if (this.chart) {
        const option = this.createChartOption();
        this.chart.setOption(option);
      }
    },

    resizeChart() {
      this.chart?.resize();
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
  z-index: 2;
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