import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as echarts from 'echarts'
import { MotionPlugin } from '@vueuse/motion'
import 'animate.css'

const app = createApp(App)
app.use(ElementPlus)
app.use(MotionPlugin)
app.config.globalProperties.$echarts = echarts
app.mount('#app')
