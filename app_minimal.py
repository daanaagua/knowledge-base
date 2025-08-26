from flask import Flask, request, jsonify, render_template_string
import os
import json
import requests
from datetime import datetime

app = Flask(__name__)

# 简化的HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI知识库</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        textarea { width: 100%; height: 100px; margin: 10px 0; padding: 10px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: white; border-radius: 4px; }
        .loading { color: #666; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI知识库</h1>
        <form id="queryForm">
            <textarea id="question" placeholder="请输入您的问题..."></textarea>
            <button type="submit">提交问题</button>
        </form>
        <div id="result" class="result" style="display:none;"></div>
    </div>

    <script>
        document.getElementById('queryForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const question = document.getElementById('question').value;
            const resultDiv = document.getElementById('result');
            
            if (!question.trim()) {
                alert('请输入问题');
                return;
            }
            
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<div class="loading">正在处理您的问题...</div>';
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.innerHTML = `<h3>回答：</h3><p>${data.answer}</p>`;
                } else {
                    resultDiv.innerHTML = `<p style="color: red;">错误: ${data.error}</p>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">请求失败: ${error.message}</p>`;
            }
        });
    </script>
</body>
</html>
'''

# 简化的知识库数据
KNOWLEDGE_BASE = {
    "AI": "人工智能（Artificial Intelligence）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
    "机器学习": "机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。",
    "深度学习": "深度学习是机器学习的一个子集，使用多层神经网络来模拟人脑的工作方式。",
    "Python": "Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名，广泛用于数据科学、AI和Web开发。",
    "Flask": "Flask是一个轻量级的Python Web框架，用于快速开发Web应用程序。"
}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)