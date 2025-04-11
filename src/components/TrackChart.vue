<template>
  <div id="plotlyChart"></div>
</template>

<script>
import Plotly from 'plotly.js-dist'

export default {
  name: 'PlotlyChart',
  async mounted() {
    try {
      const response = await fetch('/api/plotly-data')
      const figure = await response.json()
      
      // 直接使用获取到的数据绘制图表
      Plotly.newPlot('plotlyChart', figure.data, figure.layout)
    } catch (error) {
      console.error('加载Plotly数据失败:', error)
    }
  }
}
</script>

<style scoped>
#plotlyChart {
  width: 100%;
  height: 600px;
}
</style>