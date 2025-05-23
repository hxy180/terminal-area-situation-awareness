<template>
  <el-dialog
    v-model="dialogVisible"
    title="参数设置"
    width="350px"
    :close-on-click-modal="false"
    :show-close="true"
    class="param-dialog"
    @close="handleClose"
  >
    <div class="tech-frame">
      <div class="corner top-left"></div>
      <div class="corner top-right"></div>
      <div class="corner bottom-left"></div>
      <div class="corner bottom-right"></div>
    </div>
    
    <div class="param-setting-container">
      <div class="param-item" v-for="(param, key) in params" :key="key">
        <div class="param-label">{{ param.label }}:</div>
        <div class="param-input">
          <el-input-number 
            v-model="param.value" 
            :min="param.min" 
            :max="param.max"
            :step="param.step"
            :precision="param.precision"
            size="small"
            controls-position="right"
            @change="handleChange(key, $event)"
          />
        </div>
        <div class="param-unit" v-if="param.unit">{{ param.unit }}</div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="resetParams" class="reset-btn">重置</el-button>
        <el-button type="primary" @click="saveParams" class="confirm-btn">确认</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: 'ParamSettingDialog',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    defaultParams: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      dialogVisible: false,
      params: {
        resamplePoints: {
          label: '重采样点数',
          value: 200,
          min: 50,
          max: 500,
          step: 10,
          precision: 0,
          description: '控制航迹重采样时的点数量，数值越大精度越高'
        },
        centerAreaLength: {
          label: '中心区域边长',
          value: 20,
          min: 5,
          max: 50,
          step: 1,
          precision: 0,
          description: '设置识别算法中心区域的边长范围'
        },
        neighborRadius: {
          label: '领域半径',
          value: 5,
          min: 1,
          max: 15,
          step: 0.5,
          precision: 1,
          // unit: 'km',
          description: '聚类算法参数，影响航迹聚类效果'
        },
        minPoints: {
          label: '最小点数',
          value: 5,
          min: 1,
          max: 20,
          step: 1,
          precision: 0,
          // unit: '点',
          description: '聚类算法的最小点数要求，用于过滤噪声点'
        }
      },
      initialParams: {}
    };
  },
  watch: {
    visible: {
      handler(val) {
        this.dialogVisible = val;
        if (val) {
          // 保存初始参数以便重置
          this.initialParams = JSON.parse(JSON.stringify(this.params));
          
          // 如果有传入默认参数，就使用默认参数
          if (this.defaultParams) {
            Object.keys(this.defaultParams).forEach(key => {
              if (this.params[key]) {
                this.params[key].value = this.defaultParams[key];
              }
            });
          }
        }
      },
      immediate: true
    }
  },
  methods: {
    handleClose() {
      this.$emit('update:visible', false);
    },
    resetParams() {
      Object.keys(this.params).forEach(key => {
        if (this.initialParams[key]) {
          this.params[key].value = this.initialParams[key].value;
        }
      });
    },
    saveParams() {
      const paramValues = {};
      Object.keys(this.params).forEach(key => {
        paramValues[key] = this.params[key].value;
      });
      
      this.dialogVisible = false;
      this.$emit('update:visible', false);
      this.$emit('save', paramValues);
    },
    handleChange(key, value) {
      // 参数变化时的处理
    }
  }
};
</script>

<style scoped>
.param-setting-container {
  padding: 15px 10px 5px;
  position: relative;
  z-index: 2;
}

.param-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  background: linear-gradient(145deg, #e6f1ff, #d1e6ff);
  padding: 12px 15px;
  border-radius: 12px;
  border-left: 4px solid #1890ff;
  box-shadow: 0 2px 0 rgba(24, 144, 255, 0.12), 0 4px 10px rgba(32, 82, 149, 0.1);
  position: relative;
}

.param-label {
  width: 100px;
  text-align: right;
  margin-right: 15px;
  font-size: 14px;
  color: #1f5285;
  font-weight: 500;
}

.param-input {
  flex: 1;
  z-index: 2;
}

.param-unit {
  margin-left: 10px;
  width: 30px;
  font-size: 14px;
  color: #4b7eb9;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-dialog) {
  background: linear-gradient(145deg, #e1eeff, #c5dcff);
  border-radius: 15px;
  border: 1px solid rgba(24, 144, 255, 0.3);
  box-shadow: 0 10px 30px rgba(24, 144, 255, 0.2);
  overflow: hidden;
  backdrop-filter: blur(5px);
}

:deep(.el-dialog__header) {
  background: linear-gradient(to right, #d0e3ff, #b8d5ff);
  padding: 15px 20px;
  margin-right: 0;
  border-radius: 15px 15px 0 0;
  border-bottom: 1px solid rgba(24, 144, 255, 0.2);
  position: relative;
}

:deep(.el-dialog__title) {
  color: #1f5285;
  font-size: 18px;
  font-weight: bold;
  letter-spacing: 2px;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: #4b7eb9;
}

:deep(.el-dialog__headerbtn:hover .el-dialog__close) {
  color: #1890ff;
}

:deep(.el-dialog__body) {
  padding: 20px 15px;
  background: linear-gradient(135deg, #d5e7ff 0%, #e8f2ff 100%);
  color: #1f5285;
  position: relative;
  overflow: hidden;
}

:deep(.el-dialog__footer) {
  border-top: 1px solid rgba(24, 144, 255, 0.2);
  padding: 15px 20px;
  background: linear-gradient(to right, #d0e3ff, #b8d5ff);
}

:deep(.el-input-number) {
  width: 100%;
  --el-input-bg-color: rgba(255, 255, 255, 0.9);
  --el-input-text-color: #1f5285;
  --el-input-border-color: rgba(24, 144, 255, 0.3);
  --el-input-hover-border-color: rgba(24, 144, 255, 0.6);
  --el-input-focus-border-color: #1890ff;
}

:deep(.el-input-number__decrease),
:deep(.el-input-number__increase) {
  background: linear-gradient(145deg, #e6f1ff, #d1e6ff) !important;
  color: #4b7eb9 !important;
  border-color: rgba(24, 144, 255, 0.3) !important;
  transition: all 0.3s ease;
}

:deep(.el-input-number__decrease:hover),
:deep(.el-input-number__increase:hover) {
  color: #1890ff !important;
  background: linear-gradient(145deg, #d1e6ff, #e6f1ff) !important;
  box-shadow: 0 0 8px rgba(24, 144, 255, 0.3);
}

:deep(.el-input__inner) {
  box-shadow: 0 2px 4px rgba(24, 144, 255, 0.08) inset;
  background-color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

:deep(.el-input__inner:focus) {
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2), 0 2px 4px rgba(24, 144, 255, 0.08) inset;
}

.reset-btn {
  background: linear-gradient(145deg, #e6f1ff, #d1e6ff);
  border-color: rgba(24, 144, 255, 0.3);
  color: #4b7eb9;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.reset-btn:hover {
  background: linear-gradient(145deg, #d1e6ff, #e6f1ff);
  border-color: rgba(24, 144, 255, 0.5);
  color: #1890ff;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(24, 144, 255, 0.2);
}

.confirm-btn {
  background: linear-gradient(145deg, #1890ff, #0073e6);
  border-color: #1890ff;
  color: #ffffff;
  font-weight: bold;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.confirm-btn:hover {
  background: linear-gradient(145deg, #0081f1, #1890ff);
  border-color: #0b7dfa;
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(24, 144, 255, 0.3);
}

/* 科技感边框 */
.tech-frame {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.corner {
  position: absolute;
  width: 25px;
  height: 25px;
  border: 2px solid #1890ff;
  opacity: 0.7;
}

.top-left {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
}

.top-right {
  top: 0;
  right: 0;
  border-left: none;
  border-bottom: none;
}

.bottom-left {
  bottom: 0;
  left: 0;
  border-right: none;
  border-top: none;
}

.bottom-right {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
}
</style> 