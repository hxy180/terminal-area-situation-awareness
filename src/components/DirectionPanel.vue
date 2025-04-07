<template>
  <div class="direction-panel">
    <div class="direction-header">{{ title }}</div>
    <div class="direction-content">
      <span class="typing-text">{{ displayDirection }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DirectionPanel',
  props: {
    title: {
      type: String,
      required: true
    },
    direction: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      displayDirection: '',
      currentIndex: 0,
      typingTimer: null,
      typingComplete: false
    };
  },
  mounted() {
    // 延迟启动打字效果
    setTimeout(() => {
      this.startTypingEffect();
    }, 800);
  },
  beforeUnmount() {
    if (this.typingTimer) {
      clearInterval(this.typingTimer);
    }
  },
  methods: {
    startTypingEffect() {
      this.typingTimer = setInterval(() => {
        if (this.currentIndex < this.direction.length) {
          this.displayDirection = this.direction.substring(0, this.currentIndex + 1);
          this.currentIndex++;
        } else {
          clearInterval(this.typingTimer);
          this.typingComplete = true;
        }
      }, 150);
    }
  }
};
</script>

<style scoped>
.direction-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--panel-background);
  border: 1px solid var(--border-color);
  border-radius: 5px;
  box-shadow: 0 0 15px rgba(0, 179, 255, 0.2);
  overflow: hidden;
  position: relative;
}

.direction-panel::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, 
    transparent 0%, 
    rgba(0, 179, 255, 0.05) 25%, 
    transparent 50%, 
    rgba(0, 179, 255, 0.05) 75%, 
    transparent 100%);
  background-size: 200% 200%;
  animation: shine 8s linear infinite;
  pointer-events: none;
}

@keyframes shine {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 200% 200%;
  }
}

.direction-header {
  padding: 10px;
  background-color: rgba(1, 30, 65, 0.8);
  color: var(--text-color);
  text-align: center;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color);
}

.direction-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 26px;
  font-weight: bold;
  color: var(--highlight-color);
  position: relative;
}

.typing-text {
  position: relative;
  text-shadow: 0 0 10px rgba(0, 179, 255, 0.5);
  animation: pulse 1.5s ease-in-out infinite alternate;
}

/* 完全移除光标效果 */

@keyframes pulse {
  from {
    text-shadow: 0 0 5px rgba(0, 179, 255, 0.5);
  }
  to {
    text-shadow: 0 0 15px rgba(0, 179, 255, 0.8), 0 0 20px rgba(0, 179, 255, 0.5);
  }
}

/* 移除扫描线样式和动画 */
/*.scan-line {
  position: absolute;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--highlight-color), transparent);
  bottom: 10px;
  left: 0;
  animation: scan 3s linear infinite;
  opacity: 0.6;
}

@keyframes scan {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}*/
</style> 