# 修改 app.py
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import json
import time

# 加载 .env 文件配置
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)  # 用于会话管理

# 读取环境变量
MINIMAX_API_KEY = os.getenv('MINIMAX_API_KEY', '')
MINIMAX_GROUP_ID = os.getenv('MINIMAX_GROUP_ID', '')

# 缓存机制
cache = {}
cache_timeout = 3600  # 缓存1小时

# 校验 API 密钥是否配置
if not MINIMAX_API_KEY or not MINIMAX_GROUP_ID:
    print("⚠️ 警告：未配置 MINIMAX_API_KEY 或 MINIMAX_GROUP_ID，请在 .env 文件中填写真实密钥！")

@app.route('/')
def index():
    """根路由：渲染 templates 文件夹下的 index.html"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"加载页面失败：{str(e)}<br>请确认 templates 文件夹下有 index.html 文件", 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """API endpoint: Receive keyword, call Minimax API to generate content (supports multi-turn conversation)"""
    try:
        if not request.is_json:
            return jsonify({'error': 'Invalid request format, please use JSON format'}), 400
        
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        reset = data.get('reset', False)  # Reset conversation history
        
        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400
        
        if not MINIMAX_API_KEY or not MINIMAX_GROUP_ID:
            return jsonify({'error': 'Please configure valid MINIMAX_API_KEY and MINIMAX_GROUP_ID in .env file first'}), 500
        
        # 初始化或重置对话历史
        if reset or 'conversation' not in session:
            session['conversation'] = []
        
        # 添加用户消息到对话历史
        session['conversation'].append({
            'role': 'user',
            'content': keyword
        })
        
        # 调用 API 生成回复
        content = call_minimax_api(session['conversation'])
        
        # 添加模型回复到对话历史
        session['conversation'].append({
            'role': 'assistant',
            'content': content
        })
        
        # 限制对话历史长度，避免过长
        if len(session['conversation']) > 10:  # 最多保存10轮对话
            session['conversation'] = session['conversation'][-10:]
        
        # 返回生成的内容和完整对话历史
        return jsonify({
            'content': content,
            'conversation': session['conversation']
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def call_minimax_api(conversation):
    """Call Minimax M2.7 model (supports multi-turn conversation)"""
    url = 'https://api.minimax.chat/v1/text/chatcompletion_v2'
    
    headers = {
        'Authorization': f'Bearer {MINIMAX_API_KEY}',
        'Content-Type': 'application/json',
        'Group-Id': MINIMAX_GROUP_ID
    }
    
    # Build system prompt
    system_prompt = "You are a creative assistant focused on University of Nottingham Ningbo China (UNNC) campus content. Please respond in English and generate content related to UNNC campus life, studies, and activities."
    
    # Build complete message list with system prompt and conversation history
    messages = [{
        'role': 'system',
        'content': system_prompt
    }] + conversation
    
    # Simplified payload
    payload = {
        'model': 'minimax-m2.7',
        'messages': messages,
        'temperature': 0.7,
        'max_tokens': 500,
        'group_id': MINIMAX_GROUP_ID
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  
        
        # 解析 M2.7 模型的返回结果
        result = response.json()
        if not result:
            raise Exception("API 返回结果为空")
        
        # 优先提取 reasoning_content 字段
        content = ""
        if 'reasoning_content' in result and result['reasoning_content'].strip():
            content = result['reasoning_content'].strip()
        # 其次尝试 reply 字段
        elif 'reply' in result and result['reply'].strip():
            content = result['reply'].strip()
        # 最后尝试 choices 字段
        elif 'choices' in result and isinstance(result['choices'], list) and len(result['choices']) > 0:
            content = result['choices'][0].get('message', {}).get('content', '').strip()
        
        # 如果所有字段都为空，返回原始结果以便调试
        if not content:
            content = f"调试信息：{json.dumps(result, ensure_ascii=False)}"
        
        return content
            
    except requests.exceptions.Timeout:
        raise Exception("请求超时，请检查网络连接")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"API 请求失败：HTTP {e.response.status_code}，详情：{e.response.text}")
    except ValueError as e:
        raise Exception(f"解析 API 返回结果失败：{str(e)}")
    except Exception as e:
        raise Exception(f"调用 API 出错：{str(e)}")

if __name__ == '__main__':
    print('🚀 Starting UNNC Campus AIGC Generator...')
    print('🌐 Please open in browser: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)