# 终端区运行态势感知系统

这是一个基于Vue.js开发的终端区运行态势感知系统，用于可视化和分析航空航迹数据。系统实时展示多条航迹运行态势，提供参数设置和数据分析功能，帮助用户直观了解空域运行状况。

## 功能特点

- **航迹可视化**：实时展示多条航迹运行态势，支持不同颜色标识不同方向航线
- **实时动态更新**：航迹点位实时刷新，直观反映飞行器动态
- **坐标系统**：提供X/Y坐标系显示（单位：千米），范围X: -100km~150km，Y: -150km~200km
- **交互控制**：支持缩放视图、暂停/继续动画等操作
- **参数配置**：可动态调整重采样点数、中心区域边长、邻域半径等关键参数
- **航迹统计分析**：实时统计不同方向的航迹数量及分布情况
- **数据可视化**：提供柱状图、饼图等多种图表展示统计数据
- **蓝色主题界面**：专业化的深蓝配色方案，符合航空监控系统美学

## 系统架构

系统由以下主要组件构成：

- **TrackChart**: 航迹运行态势图，核心可视化组件
- **ParamSettingDialog**: 参数设置对话框，用于调整系统参数
- **StatisticsChart**: 统计数据图表，展示航迹分布和分析结果
- **DirectionPanel**: 方向面板，展示各方向航迹基本信息
- **ParameterDisplay**: 参数显示面板，展示当前系统参数
- **ControlButtons**: 控制按钮组，提供系统主要功能入口

## 技术栈

- **前端框架**: Vue 3
- **构建工具**: Vite
- **可视化库**: ECharts 5
- **UI组件**: Element Plus
- **数据处理**: JavaScript内置函数和自定义算法

## 安装与运行

```bash
# 安装依赖
npm install

# 开发模式运行
npm run dev

# 构建生产版本
npm run build
```

## 使用流程

1. **启动系统**：执行`npm run dev`启动开发服务器
2. **数据加载**：点击"选择数据"按钮上传或选择航迹数据文件（支持.mat格式）
3. **参数配置**：点击"设置参数"按钮打开参数设置对话框，调整以下参数：
   - 重采样点数：影响航迹点密度，默认200
   - 中心区域边长：设置中心区域大小（千米），默认20km
   - 邻域半径：设置点位聚类半径（千米），默认5km
   - 最小点数：设置聚类最小点数，默认5个
4. **交通流识别**：点击"识别交通流"执行航迹聚类算法
5. **查看结果**：在"分析结果"面板查看详细的聚类结果和统计信息

## 主要功能详解

### 航迹图（TrackChart）

- 实时展示多条不同方向的航迹点和轨迹线
- 提供缩放控制（+/-按钮），可放大查看局部细节
- 中心点标记和中心区域可视化
- 坐标轴配置：X/Y轴范围可随缩放动态调整
- 航迹点颜色编码：不同方向使用不同颜色标识

### 参数设置（ParamSettingDialog）

- 蓝色主题界面，专业美观
- 四项核心参数可调整：
  - 重采样点数（50-500）
  - 中心区域边长（5-50km）
  - 邻域半径（1-10km）
  - 最小点数（3-20）
- 参数调整后实时应用到系统

### 统计图表（StatisticsChart）

- 柱状图展示各方向航迹数量
- 饼图展示航迹占比分布
- 支持图表交互和数据筛选

## 性能优化

- 使用节流函数控制频繁更新
- 动画帧率优化，减少资源占用
- 在打开参数设置对话框时自动暂停航迹动画，减轻系统负担

## 最近更新

- **UI优化**：参数设置对话框更新为蓝色主题，提升专业感和美观度
- **动画优化**：移除雷达扫描效果和涟漪动画，提升界面稳定性
- **坐标调整**：优化X/Y轴坐标范围和刻度，更符合实际应用需求
- **交互改进**：在打开参数设置对话框时自动暂停航迹动画，避免白条闪烁
- **缩放功能**：优化缩放比例和效果，提升用户体验

## 开发环境推荐

- [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (并禁用Vetur)
- Node.js 16+
- npm 8+

## 配置自定义

详见 [Vite配置参考](https://vitejs.dev/config/)。

## 主要指标说明

- DBI：Davies-Bouldin指数，衡量聚类效果
- CH：Calinski-Harabasz指数，衡量聚类紧密度
- SC：轮廓系数，衡量聚类的有效性

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).
