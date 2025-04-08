<template>
  <div class="parameter-display">
    <!-- 基础参数部分 -->
    <div class="params-section basic-params">
      <div 
        v-for="param in basicParameters" 
        :key="param.key" 
        class="indicator"
      >
        <span class="indicator-label">{{ param.label }}:</span>
        <span class="indicator-value">{{ param.value }}</span>
      </div>
    </div>

    <!-- 算法指标部分 -->
    <div v-if="showMetrics" class="params-section metrics-params">
      <div class="metrics-title">算法指标</div>
      <div 
        v-for="param in metricParameters" 
        :key="param.key" 
        class="indicator metric-indicator"
        :class="{ 'fade-in': showMetrics }"
      >
        <span class="indicator-label">{{ param.label }}:</span>
        <span class="indicator-value">{{ param.value }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ParameterDisplay',
  props: {
    customParams: {
      type: Object,
      default: () => ({})
    },
    showMetrics: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      defaultBasicParams: [
        { label: '重采样点数', value: '200', key: 'resamplePoints' },
        { label: '中心区域边长', value: '20', key: 'centerAreaLength' },
        { label: '领域半径', value: '5', key: 'neighborRadius' },
        { label: '最小点数', value: '5', key: 'minPoints' }
      ],
      defaultMetricParams: [
        { label: 'DBI', value: '0.2192', key: 'dbi' },
        { label: 'CH', value: '3492', key: 'ch' },
        { label: 'SC', value: '0.9379', key: 'sc' }
      ]
    };
  },
  computed: {
    basicParameters() {
      return this.defaultBasicParams.map(param => ({
        ...param,
        value: this.customParams[param.key] ? String(this.customParams[param.key]) : param.value
      }));
    },
    metricParameters() {
      return this.defaultMetricParams.map(param => ({
        ...param,
        value: this.customParams[param.key] ? String(this.customParams[param.key]) : param.value
      }));
    }
  }
};
</script>

<style scoped>
.parameter-display {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
  z-index: 10;
  background-color: rgba(1, 42, 87, 0.9);
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.params-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metrics-params {
  border-top: 1px solid rgba(76, 152, 226, 0.3);
  padding-top: 15px;
  margin-top: 5px;
}

.metrics-title {
  color: #4c98e2;
  font-size: 14px;
  margin-bottom: 8px;
  font-weight: bold;
}

.indicator {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  align-items: center;
  margin-bottom: 2px;
}

.metric-indicator {
  opacity: 0;
  transform: translateY(10px);
}

.metric-indicator.fade-in {
  animation: slideIn 0.5s forwards;
}

.indicator-label {
  color: #ffffff;
  margin-right: 10px;
  flex-shrink: 0;
}

.indicator-value {
  color: #00b3ff;
  font-weight: bold;
  text-align: right;
  min-width: 60px;
  padding-left: 5px;
  position: relative;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 