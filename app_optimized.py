from flask import Flask, request, jsonify, render_template_string
import json
import os
import re
from typing import List, Dict, Any

app = Flask(__name__)

# 优化的知识库存储
class OptimizedKnowledgeBase:
    def __init__(self):
        self.documents = [
            {"id": 1, "text": "机器学习是人工智能的重要分支，专注于算法和统计模型的研究", "category": "机器学习", "source": "AI基础知识"},
            {"id": 2, "text": "深度学习基于神经网络，能够自动学习数据的层次特征表示", "category": "深度学习", "source": "神经网络基础"},
            {"id": 3, "text": "自然语言处理使计算机能够理解、解释和生成人类语言文本", "category": "NLP", "source": "语言处理技术"},
            {"id": 4, "text": "计算机视觉让机器能够理解和分析图像、视频等视觉信息", "category": "CV", "source": "图像处理技术"},
            {"id": 5, "text": "强化学习通过试错学习，让智能体学会在环境中做出最优决策", "category": "强化学习", "source": "决策算法"},
            {"id": 6, "text": "Transformer架构在自然语言处理领域取得了突破性进展", "category": "NLP", "source": "现代架构"},
            {"id": 7, "text": "卷积神经网络CNN在图像识别和计算机视觉任务中表现出色", "category": "CV", "source": "神经网络应用"},
            {"id": 8, "text": "BERT模型通过双向编码器实现更好的语言理解能力", "category": "NLP", "source": "预训练模型"},
            {"id": 9, "text": "生成对抗网络GAN可以生成逼真的图像、文本和其他数据", "category": "生成模型", "source": "创造性AI"},
            {"id": 10, "text": "知识图谱将信息组织成结构化的语义网络，便于推理和查询", "category": "知识表示", "source": "数据结构"}
        ]
        self.next_id = 11
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """改进的搜索算法，支持多关键词和模糊匹配"""
        query_lower = query.lower()
        query_words = re.findall(r'\w+', query_lower)
        
        results = []
        for doc in self.documents:
            text_lower = doc["text"].lower()
            
            # 计算匹配分数
            score = 0
            
            # 完整查询匹配
            if query_lower in text_lower:
                score += 1.0
            
            # 关键词匹配
            word_matches = sum(1 for word in query_words if word in text_lower)
            if word_matches > 0:
                score += word_matches / len(query_words) * 0.8
            
            # 分类匹配
            if query_lower in doc["category"].lower():
                score += 0.6
            
            if score > 0:
                results.append({
                    "text": doc["text"],
                    "similarity": min(score, 1.0),
                    "metadata": {
                        "category": doc["category"],
                        "source": doc["source"],
                        "id": doc["id"]
                    }
                })
        
        # 按相似度排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def add_document(self, text: str, category: str = "其他", source: str = "用户添加") -> bool:
        """添加新文档"""
        if not text.strip():
            return False
        
        self.documents.append({
            "id": self.next_id,
            "text": text.strip(),
            "category": category or "其他",
            "source": source or "用户添加"
        })
        self.next_id += 1
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        categories = {}
        for doc in self.documents:
            cat = doc["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_documents": len(self.documents),
            "categories": categories,
            "latest_id": self.next_id - 1
        }

# 初始化知识库
kb = OptimizedKnowledgeBase()

# 简单的问答系统
def generate_answer(query: str, context_docs: List[Dict]) -> str:
    """基于检索到的文档生成简单回答"""
    if not context_docs:
        return "抱歉，我没有找到相关信息来回答您的问题。"
    
    # 提取相关信息
    relevant_info = []
    for doc in context_docs[:3]:  # 只使用前3个最相关的文档
        relevant_info.append(doc["text"])
    
    # 简单的模板回答
    if "是什么" in query or "什么是" in query:
        return f"根据知识库信息：{relevant_info[0]}"
    elif "如何" in query or "怎么" in query:
        return f"关于您的问题，相关信息如下：{' '.join(relevant_info[:2])}"
    else:
        return f"根据搜索结果，相关信息包括：{relevant_info[0]}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能知识库系统 - 优化版</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .main-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .tabs { display: flex; margin-bottom: 30px; border-bottom: 2px solid #f0f0f0; }
        .tab { padding: 15px 25px; background: none; border: none; cursor: pointer; font-size: 16px; color: #666; transition: all 0.3s; }
        .tab.active { color: #667eea; border-bottom: 3px solid #667eea; font-weight: bold; }
        .tab:hover { color: #667eea; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        .form-group input, .form-group textarea { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; transition: border-color 0.3s; }
        .form-group input:focus, .form-group textarea:focus { outline: none; border-color: #667eea; }
        .btn { padding: 12px 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 600; transition: transform 0.2s; }
        .btn:hover { transform: translateY(-2px); }
        .btn:active { transform: translateY(0); }
        .result { margin-top: 25px; }
        .result-item { margin-bottom: 20px; padding: 20px; background: #f8f9fa; border-radius: 10px; border-left: 5px solid #667eea; }
        .similarity { color: #28a745; font-weight: bold; margin-bottom: 10px; }
        .result-text { font-size: 16px; line-height: 1.6; margin-bottom: 10px; }
        .result-meta { font-size: 14px; color: #666; }
        .loading { text-align: center; color: #667eea; font-size: 18px; padding: 40px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
        .stat-card { background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; }
        .stat-number { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; margin-top: 5px; }
        .answer-section { background: #e8f4fd; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #007bff; }
        .answer-title { color: #007bff; font-weight: bold; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 智能知识库系统</h1>
            <p>优化版 - 快速搜索与智能问答</p>
        </div>
        
        <div class="main-card">
            <div class="tabs">
                <button class="tab active" onclick="showTab('search')">🔍 语义搜索</button>
                <button class="tab" onclick="showTab('qa')">🤖 智能问答</button>
                <button class="tab" onclick="showTab('manage')">📊 知识库管理</button>
                <button class="tab" onclick="showTab('stats')">📈 统计信息</button>
            </div>
            
            <div id="search" class="tab-content active">
                <h2>🔍 语义搜索</h2>
                <div class="form-group">
                    <label>搜索查询:</label>
                    <input type="text" id="searchQuery" placeholder="例如: 机器学习算法、深度学习应用">
                </div>
                <div class="form-group">
                    <label>返回结果数:</label>
                    <input type="number" id="topK" value="5" min="1" max="10">
                </div>
                <button class="btn" onclick="performSearch()">开始搜索</button>
                <div id="searchResults"></div>
            </div>
            
            <div id="qa" class="tab-content">
                <h2>🤖 智能问答</h2>
                <div class="form-group">
                    <label>您的问题:</label>
                    <input type="text" id="qaQuery" placeholder="例如: 什么是机器学习？深度学习如何工作？">
                </div>
                <button class="btn" onclick="performQA()">获取答案</button>
                <div id="qaResults"></div>
            </div>
            
            <div id="manage" class="tab-content">
                <h2>📊 知识库管理</h2>
                <div class="form-group">
                    <label>文档内容:</label>
                    <textarea id="newText" rows="4" placeholder="输入新的知识内容..."></textarea>
                </div>
                <div class="form-group">
                    <label>分类标签:</label>
                    <input type="text" id="category" placeholder="例如: 机器学习、深度学习、NLP">
                </div>
                <div class="form-group">
                    <label>来源:</label>
                    <input type="text" id="source" placeholder="例如: 技术文档、研究论文">
                </div>
                <button class="btn" onclick="addDocument()">添加文档</button>
                <div id="manageResults"></div>
            </div>
            
            <div id="stats" class="tab-content">
                <h2>📈 统计信息</h2>
                <button class="btn" onclick="loadStats()">刷新统计</button>
                <div id="statsResults"></div>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // 隐藏所有标签页内容
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // 移除所有标签页的active类
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // 显示选中的标签页
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        async function performSearch() {
            const query = document.getElementById('searchQuery').value;
            const topK = document.getElementById('topK').value;
            
            if (!query.trim()) {
                alert('请输入搜索查询');
                return;
            }
            
            document.getElementById('searchResults').innerHTML = '<div class="loading">🔍 正在搜索...</div>';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query, top_k: parseInt(topK) })
                });
                
                const data = await response.json();
                displaySearchResults(data.results);
            } catch (error) {
                document.getElementById('searchResults').innerHTML = '<div class="result">❌ 搜索失败: ' + error.message + '</div>';
            }
        }
        
        function displaySearchResults(results) {
            const container = document.getElementById('searchResults');
            if (results.length === 0) {
                container.innerHTML = '<div class="result">😔 未找到相关结果，请尝试其他关键词</div>';
                return;
            }
            
            let html = '<div class="result"><h3>✨ 搜索结果:</h3>';
            results.forEach((result, index) => {
                html += `
                    <div class="result-item">
                        <div class="similarity">📊 相似度: ${(result.similarity * 100).toFixed(1)}%</div>
                        <div class="result-text">${result.text}</div>
                        <div class="result-meta">
                            🏷️ 分类: ${result.metadata.category} | 📚 来源: ${result.metadata.source}
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            container.innerHTML = html;
        }
        
        async function performQA() {
            const query = document.getElementById('qaQuery').value;
            
            if (!query.trim()) {
                alert('请输入您的问题');
                return;
            }
            
            document.getElementById('qaResults').innerHTML = '<div class="loading">🤖 正在思考...</div>';
            
            try {
                const response = await fetch('/api/qa', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                displayQAResults(data);
            } catch (error) {
                document.getElementById('qaResults').innerHTML = '<div class="result">❌ 问答失败: ' + error.message + '</div>';
            }
        }
        
        function displayQAResults(data) {
            const container = document.getElementById('qaResults');
            let html = '<div class="result">';
            
            if (data.answer) {
                html += `
                    <div class="answer-section">
                        <div class="answer-title">💡 AI 回答:</div>
                        <div>${data.answer}</div>
                    </div>
                `;
            }
            
            if (data.references && data.references.length > 0) {
                html += '<h3>📚 参考资料:</h3>';
                data.references.forEach((ref, index) => {
                    html += `
                        <div class="result-item">
                            <div class="similarity">📊 相关度: ${(ref.similarity * 100).toFixed(1)}%</div>
                            <div class="result-text">${ref.text}</div>
                            <div class="result-meta">
                                🏷️ ${ref.metadata.category} | 📚 ${ref.metadata.source}
                            </div>
                        </div>
                    `;
                });
            }
            
            html += '</div>';
            container.innerHTML = html;
        }
        
        async function addDocument() {
            const text = document.getElementById('newText').value;
            const category = document.getElementById('category').value;
            const source = document.getElementById('source').value;
            
            if (!text.trim()) {
                alert('请输入文档内容');
                return;
            }
            
            document.getElementById('manageResults').innerHTML = '<div class="loading">📝 正在添加...</div>';
            
            try {
                const response = await fetch('/api/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, category, source })
                });
                
                const data = await response.json();
                if (data.success) {
                    document.getElementById('manageResults').innerHTML = '<div class="result">✅ 文档添加成功！</div>';
                    // 清空表单
                    document.getElementById('newText').value = '';
                    document.getElementById('category').value = '';
                    document.getElementById('source').value = '';
                }
            } catch (error) {
                document.getElementById('manageResults').innerHTML = '<div class="result">❌ 添加失败: ' + error.message + '</div>';
            }
        }
        
        async function loadStats() {
            document.getElementById('statsResults').innerHTML = '<div class="loading">📊 加载统计信息...</div>';
            
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                displayStats(data);
            } catch (error) {
                document.getElementById('statsResults').innerHTML = '<div class="result">❌ 加载失败: ' + error.message + '</div>';
            }
        }
        
        function displayStats(stats) {
            const container = document.getElementById('statsResults');
            let html = '<div class="stats-grid">';
            
            html += `
                <div class="stat-card">
                    <div class="stat-number">${stats.total_documents}</div>
                    <div class="stat-label">📄 总文档数</div>
                </div>
            `;
            
            Object.entries(stats.categories).forEach(([category, count]) => {
                html += `
                    <div class="stat-card">
                        <div class="stat-number">${count}</div>
                        <div class="stat-label">🏷️ ${category}</div>
                    </div>
                `;
            });
            
            html += '</div>';
            container.innerHTML = html;
        }
        
        // 页面加载时自动加载统计信息
        window.addEventListener('load', () => {
            loadStats();
        });
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
        top_k = data.get('top_k', 5)
        
        results = kb.search(query, top_k)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/qa', methods=['POST'])
def qa():
    try:
        data = request.json
        query = data.get('query', '')
        
        # 搜索相关文档
        results = kb.search(query, top_k=3)
        
        # 生成回答
        answer = generate_answer(query, results)
        
        return jsonify({
            'answer': answer,
            'references': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add', methods=['POST'])
def add_document():
    try:
        data = request.json
        text = data.get('text', '')
        category = data.get('category', '其他')
        source = data.get('source', '用户添加')
        
        success = kb.add_document(text, category, source)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        stats = kb.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok', 
        'message': '智能知识库系统运行正常',
        'version': '2.0-optimized'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)