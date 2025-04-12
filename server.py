from flask import Flask, send_file, jsonify, request
import json  # 添加json模块
import subprocess  # 新增：用于执行系统命令

app = Flask(__name__)

@app.route('/api/plotly-data')
def get_plotly_data():
    return send_file('./result/plotly_data.json')

@app.route('/api/analysis-results')
def get_analysis_results():
    with open('./result/analysis_results.json', 'r') as f:
        analysis_data = json.load(f)
    return jsonify(analysis_data)

# 新增：执行 echo 命令的接口
@app.route('/api/echo', methods=['POST'])
def execute_echo():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # 使用 subprocess 执行 echo 命令
        result = subprocess.run(['echo', message], 
                              capture_output=True, 
                              text=True, 
                              shell=True)
        
        # 读取参数文件
        try:
            with open('./result/result_param.json', 'r') as f:
                params = json.load(f)
                dbi = params.get('dbi', 0)
                ch = params.get('ch', 0)
                sc = params.get('sc', 0)
        except Exception as e:
            print(f"读取参数文件失败: {str(e)}")
            dbi, ch, sc = 0, 0, 0
        
        return jsonify({
            'success': result.returncode == 0,
            'returncode': result.returncode,
            'output': result.stdout,
            'error': result.stderr,
            'params': {
                'dbi': dbi,
                'ch': ch,
                'sc': sc
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=5000)  # 启用调试模式