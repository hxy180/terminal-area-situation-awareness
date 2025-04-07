<template>
  <div class="data-loading" v-if="show">
    <div class="loading-container">
      <div class="loading-circle"></div>
      <div class="loading-text">{{ text }}</div>
      <div class="loading-progress-container">
        <div class="loading-progress-bar" :style="{ width: `${progress}%` }"></div>
      </div>
      <div class="loading-percent">{{ progress }}%</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataLoading',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    text: {
      type: String,
      default: '数据加载中...'
    }
  },
  data() {
    return {
      progress: 0,
      interval: null
    };
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.startProgress();
      } else {
        this.stopProgress();
      }
    }
  },
  methods: {
    startProgress() {
      this.progress = 0;
      this.interval = setInterval(() => {
        if (this.progress < 100) {
          this.progress += Math.floor(Math.random() * 5) + 1;
          if (this.progress > 100) this.progress = 100;
        } else {
          this.stopProgress();
          setTimeout(() => {
            this.$emit('loading-complete');
          }, 500);
        }
      }, 100);
    },
    stopProgress() {
      if (this.interval) {
        clearInterval(this.interval);
        this.interval = null;
      }
    }
  },
  beforeUnmount() {
    this.stopProgress();
  }
};
</script>

<style scoped>
.data-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(1, 42, 87, 0.85);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-container {
  width: 400px;
  padding: 30px;
  background-color: rgba(0, 20, 50, 0.8);
  border: 1px solid #4c98e2;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 179, 255, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading-circle {
  width: 80px;
  height: 80px;
  border: 3px solid transparent;
  border-top-color: #00b3ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: #ffffff;
  font-size: 18px;
  margin-bottom: 20px;
  text-align: center;
}

.loading-progress-container {
  width: 100%;
  height: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.loading-progress-bar {
  height: 100%;
  background-color: #00b3ff;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.loading-percent {
  color: #00b3ff;
  font-size: 16px;
  font-weight: bold;
}
</style> 