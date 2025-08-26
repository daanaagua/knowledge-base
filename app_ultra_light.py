from flask import Flask, request, jsonify, render_template_string
import json
import re
from datetime import datetime

app = Flask(__name__)

# 超轻量级知识库 - 使用简单文本匹配
KNOWLEDGE_DATA = {
    "AI人工智能": {
        "keywords": ["ai", "人工智能", "artificial intelligence", "智能", "机器智能"],
        "content": "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统，包括学习、推理、感知和语言理解。"
    },
    "机器学习": {
        "keywords": ["机器学习", "machine learning", "ml", "算法", "模型训练"],
        "content": "机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。通过算法和统计模型，系统可以从数据中学习模式。"
    },
    "深度学习": {
        "keywords": ["深度学习", "deep learning", "神经网络", "neural network", "dl"],
        "content": "深度学习是机器学习的一个子集，使用多层神经网络来模拟人脑的工作方式，特别擅长处理图像、语音和自然语言。"
    },
    "自然语言处理": {
        "keywords": ["nlp", "自然语言处理", "natural language processing", "文本处理", "语言模型"],
        "content": "自然语言处理（NLP）是人工智能的一个分支，专注于使计算机能够理解、解释和生成人类语言。"
    },
    "Python编程": {
        "keywords": ["python", "编程", "程序设计", "代码", "开发"],
        "content": "Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名，广泛用于数据科学、AI开发和Web应用。"
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>轻量级AI知识库</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { color: #1e293b; font-size: 2.5rem; margin-bottom: 10px; }
        .header p { color: #64748b; font-size: 1.1rem; }
        .search-box { background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; }
        .input-group input, .input-group textarea { width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 16px; transition: border-color 0.2s; }
        .input-group input:focus, .input-group textarea:focus { outline: none; border-color: #3b82f6; }
        .btn { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s; }
        .btn:hover { transform: translateY(-1px); }
        .results { background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); display: none; }
        .result-item { padding: 20px; margin-bottom: 15px; background: #f8fafc; border-radius: 8px; border-left: 4px solid #3b82f6; }
        .result-title { font-weight: 600; color: #1e293b; margin-bottom: 10px; font-size: 1.1rem; }
        .result-content { color: #4b5563; line-height: 1.6; }
        .loading { text-align: center; color: #6b7280; font-style: italic; }
        .no-results { text-align: center; color: #9ca3af; }
        .knowledge-topics { background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .topics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .topic-tag { background: #eff6ff; color: #1d4ed8; padding: 8px 16px; border-radius: 20px; text-align: center; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
        .topic-tag:hover { background: #dbeafe; transform: translateY(-1px); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 AI知识库</h1>
            <p>轻量级智能问答系统</p>
        </div>
        
        <div class="search-box">
            <form id="searchForm">
                <div class="input-group">
                    <label for="question">请输入您的问题：</label>
                    <textarea id="question" rows="3" placeholder="例如：什么是机器学习？Python有什么特点？"></textarea>
                </div>
                <button type="submit" class="btn">🔍 搜索答案</button>
            </form>
        </div>
        
        <div id="results" class="results"></div>
        
        <div class="knowledge-topics">
            <h3 style="color: #1e293b; margin-bottom: 10px;">💡 知识主题</h3>
            <p style="color: #64748b; margin-bottom: 20px;">点击下方标签快速了解相关知识</p>
            <div class="topics-grid">
                <div class="topic-tag" onclick="quickSearch('AI人工智能')">🤖 人工智能</div>
                <div class="topic-tag" onclick="quickSearch('机器学习')">📊 机器学习</div>
                <div class="topic-tag" onclick="quickSearch('深度学习')">🧠 深度学习</div>
                <div class="topic-tag" onclick="quickSearch('自然语言处理')">💬 NLP</div>
                <div class="topic-tag" onclick="quickSearch('Python编程')">🐍 Python</div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('searchForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const question = document.getElementById('question').value.trim();
            if (!question) {
                alert('请输入问题');
                return;
            }
            await performSearch(question);
        });
        
        async function performSearch(question) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = '<div class="loading">🔍 正在搜索相关知识...</div>';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });
                
                const data = await response.json();
                displayResults(data.results, question);
            } catch (error) {
                resultsDiv.innerHTML = '<div class="no-results">❌ 搜索失败，请稍后重试</div>';
            }
        }
        
        function displayResults(results, question) {
            const resultsDiv = document.getElementById('results');
            
            if (results.length === 0) {
                resultsDiv.innerHTML = '<div class="no-results">😔 未找到相关知识，请尝试其他关键词</div>';
                return;
            }
            
            let html = `<h3 style="color: #1e293b; margin-bottom: 20px;">📚 搜索结果 (${results.length}条)</h3>`;
            results.forEach((result, index) => {
                html += `
                    <div class="result-item">
                        <div class="result-title">${result.title}</div>
                        <div class="result-content">${result.content}</div>
                    </div>
                `;
            });
            
            resultsDiv.innerHTML = html;
        }
        
        function quickSearch(topic) {
            document.getElementById('question').value = topic;
            performSearch(topic);
        }
    </script>
</body>
</html>
'''

def search_knowledge(query):
    """简单的关键词匹配搜索"""
    results = []
    query_lower = query.lower()
    
    for title, data in KNOWLEDGE_DATA.items():
        # 检查关键词匹配
        for keyword in data["keywords"]:
            if keyword in query_lower:
                results.append({
                    "title": title,
                    "content": data["content"],
                    "score": len(keyword)  # 简单评分
                })
                break
    
    # 按评分排序
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]  # 返回前5个结果

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'results': [], 'error': '问题不能为空'})
        
        results = search_knowledge(question)
        
        return jsonify({
            'results': results,
            'query': question,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'results': [], 'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

if __name__ == '__main__':
    app.run(debug=True)