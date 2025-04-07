<template>
  <div class="control-buttons">
    <input 
      id="matFileInput" 
      type="file" 
      accept=".mat" 
      style="display:none;" 
      @change="handleFileSelected"
    />
    <el-button 
      v-for="(button, index) in buttons" 
      :key="index"
      type="primary"
      @click="handleClick(button.action)"
    >
      {{ button.label }}
    </el-button>
  </div>
</template>

<script>
export default {
  name: 'ControlButtons',
  data() {
    return {
      buttons: [
        { label: '选择数据', action: 'selectData' },
        { label: '设置参数', action: 'setParams' },
        { label: '识别交通流', action: 'identifyTraffic' },
        { label: '分析结果', action: 'analyzeResults' }
      ]
    };
  },
  methods: {
    handleClick(action) {
      if (action === 'selectData') {
        // 触发文件选择
        document.getElementById('matFileInput').click();
      } else {
        this.$emit('button-click', action);
      }
    },
    handleFileSelected(event) {
      const file = event.target.files[0];
      if (file) {
        if (file.name.endsWith('.mat')) {
          // 将文件信息发送到父组件
          this.$emit('button-click', 'selectData', file);
          
          // 显示文件名
          console.log('选择的MAT文件:', file.name);
        } else {
          // 提示用户选择正确的文件格式
          this.$emit('file-error', '请选择.mat格式的文件');
        }
      }
      // 重置文件输入以允许选择相同文件
      event.target.value = null;
    }
  }
};
</script>

<style scoped>
.control-buttons {
  display: flex;
  justify-content: space-around;
  width: 100%;
  height: 100%;
  align-items: center;
}

.el-button {
  width: 120px;
  height: 40px;
  background-color: transparent;
  border: 1px solid #4c98e2;
  border-radius: 4px;
  color: #ffffff;
  font-size: 14px;
}

.el-button:hover {
  background-color: #00b3ff;
  border-color: #00b3ff;
  color: #012a57;
}
</style> 