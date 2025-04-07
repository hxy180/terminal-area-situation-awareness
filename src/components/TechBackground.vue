<template>
  <div class="tech-background">
    <div class="grid-overlay"></div>
    <div class="particles-container">
      <div v-for="i in 50" :key="i" class="particle" 
           :style="{ 
             top: `${Math.random() * 100}%`, 
             left: `${Math.random() * 100}%`,
             width: `${Math.random() * 4 + 1}px`,
             height: `${Math.random() * 4 + 1}px`,
             animationDelay: `${Math.random() * 5}s`,
             animationDuration: `${Math.random() * 10 + 5}s`
           }">
      </div>
    </div>
    <div class="scan-line"></div>
    <div class="corner top-left"></div>
    <div class="corner top-right"></div>
    <div class="corner bottom-left"></div>
    <div class="corner bottom-right"></div>
  </div>
</template>

<script>
export default {
  name: 'TechBackground',
};
</script>

<style scoped>
.tech-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(to right, rgba(76, 152, 226, 0.1) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(76, 152, 226, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  opacity: 0.3;
}

.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  background-color: rgba(0, 179, 255, 0.6);
  border-radius: 50%;
  animation: float linear infinite;
  opacity: 0;
}

@keyframes float {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-100px) translateX(20px);
    opacity: 0;
  }
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: rgba(0, 179, 255, 0.5);
  box-shadow: 0 0 10px 2px rgba(0, 179, 255, 0.7);
  animation: scan 8s linear infinite;
}

@keyframes scan {
  0% {
    top: -10px;
  }
  100% {
    top: 100%;
  }
}

.corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border-color: rgba(0, 179, 255, 0.7);
  border-style: solid;
  border-width: 0;
}

.top-left {
  top: 20px;
  left: 20px;
  border-top-width: 2px;
  border-left-width: 2px;
}

.top-right {
  top: 20px;
  right: 20px;
  border-top-width: 2px;
  border-right-width: 2px;
}

.bottom-left {
  bottom: 20px;
  left: 20px;
  border-bottom-width: 2px;
  border-left-width: 2px;
}

.bottom-right {
  bottom: 20px;
  right: 20px;
  border-bottom-width: 2px;
  border-right-width: 2px;
}
</style> 