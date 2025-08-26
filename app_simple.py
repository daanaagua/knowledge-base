from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

# 简化版知识库（使用内存存储）
knowledge_base = [
    {"text": "机器学习是人工智能的重要分支，专注于算法和统计模型", "category": "机器学习", "source": "AI基础知识"},
    {"text": "深度学习基于神经网络，能够自动学习数据的层次特征", "category": "深度学习", "source": "神经网络基础"},
    {"text": "自然语言处理使计算机能够理解、解释和生成人类语言", "category": "NLP", "source": "语言处理技术"},
    {"text": "计算机视觉让机器能够理解和分析视觉信息", "category": "CV", "source": "图像处理技术"},
    {"text": "强化学习通过试错学习最优决策策略", "category": "强化学习", "source": "决策算法"}
]

def simple_search(query, top_k=5):
    """简单的关键词搜索"""
    results = []
    query_lower = query.lower()
    
    for item in knowledge_base:
        if query_lower in item["text"].lower():
            results.append({
                "text": item["text"],
                "similarity": 0.8,  # 模拟相似度
                "metadata": {"category": item["category"], "source": item["source"]}
            })
    
    return results[:top_k]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能知识库系统（简化版）</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .btn { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; }
        .result-item { margin-bottom: 15px; padding: 10px; background: white; border-radius: 4px; border-left: 4px solid #007bff; }
        .similarity { color: #28a745; font-weight: bold; }
        .loading { text-align: center; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 智能知识库系统（简化版）</h1>
            <p>基于关键词搜索的知识库演示</p>
        </div>
        
        <div class="form-group">
            <label>搜索查询:</label>
            <input type="text" id="searchQuery" placeholder="例如: 机器学习">
        </div>
        <button class="btn" onclick="performSearch()">搜索</button>
        
        <div class="form-group" style="margin-top: 30px;">
            <label>添加新文档:</label>
            <textarea id="newText" rows="3" placeholder="输入新文档内容"></textarea>
        </div>
        <div class="form-group">
            <label>分类:</label>
            <input type="text" id="category" placeholder="例如: 机器学习">
        </div>
        <button class="btn" onclick="addDocument()">添加文档</button>
        
        <div id="results"></div>
    </div>

    <script>
        async function performSearch() {
            const query = document.getElementById('searchQuery').value;
            if (!query) {
                alert('请输入搜索查询');
                return;
            }
            
            document.getElementById('results').innerHTML = '<div class="loading">正在搜索...</div>';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                displayResults(data.results);
            } catch (error) {
                document.getElementById('results').innerHTML = '<div class="result">搜索失败: ' + error.message + '</div>';
            }
        }
        
        function displayResults(results) {
            const container = document.getElementById('results');
            if (results.length === 0) {
                container.innerHTML = '<div class="result">未找到相关结果</div>';
                return;
            }
            
            let html = '<div class="result"><h3>搜索结果:</h3>';
            results.forEach((result, index) => {
                html += `
                    <div class="result-item">
                        <div class="similarity">匹配度: ${result.similarity.toFixed(1)}</div>
                        <div><strong>内容:</strong> ${result.text}</div>
                        <div><strong>分类:</strong> ${result.metadata.category}</div>
                        <div><strong>来源:</strong> ${result.metadata.source}</div>
                    </div>
                `;
            });
            html += '</div>';
            container.innerHTML = html;
        }
        
        async function addDocument() {
            const text = document.getElementById('newText').value;
            const category = document.getElementById('category').value;
            
            if (!text) {
                alert('请输入文档内容');
                return;
            }
            
            try {
                const response = await fetch('/api/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, category })
                });
                
                const data = await response.json();
                if (data.success) {
                    alert('文档添加成功！');
                    document.getElementById('newText').value = '';
                    document.getElementById('category').value = '';
                }
            } catch (error) {
                alert('添加失败: ' + error.message);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query', '')
        results = simple_search(query)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add', methods=['POST'])
def add_document():
    try:
        data = request.json
        text = data.get('text', '')
        category = data.get('category', '其他')
        
        knowledge_base.append({
            "text": text,
            "category": category,
            "source": "用户添加"
        })
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': '知识库系统运行正常'})

if __name__ == '__main__':
    app.run(debug=True)