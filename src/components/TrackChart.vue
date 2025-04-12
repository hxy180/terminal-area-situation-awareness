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

      const customLayout = {
        ...figure.layout,
        margin: { t: 0, b: 0, l: 0, r: 0 },
        autosize: true,
        scene: {
          ...figure.layout.scene,
          camera: {
            eye: { x: 1.5, y: 1.5, z: 1.5 }
          },
          aspectratio: { x: 1, y: 1, z: 0.8 },
          aspectmode: 'manual'
        }
      }
      
      Plotly.newPlot('plotlyChart', figure.data, customLayout)
    } catch (error) {
      console.error('加载Plotly数据失败:', error)
    }
  }
}
</script>

<style scoped>
#plotlyChart {
  width: 100%;
  height: 700px;
}
</style>