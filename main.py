from flask import Flask, request, jsonify, render_template_string
from vector_store import KnowledgeBase
from aliyun_embedder import AliYunEmbedder
from doubao_ai import DoubaoAI
import os
import json

app = Flask(__name__)

# 初始化知识库和AI客户端
def init_knowledge_base():
    aliyun_api_key = os.getenv("ALIYUN_API_KEY", "sk-8a1b33b774344ba98cf22fc660b6c9a2")
    doubao_api_key = os.getenv("DOUBAO_API_KEY", "af304f26-0164-4318-84e7-d70ac67f2e07")
    
    embedder = AliYunEmbedder(api_key=aliyun_api_key)
    kb = KnowledgeBase(embedder=embedder)
    doubao = DoubaoAI(api_key=doubao_api_key)
    
    return kb, doubao

kb, doubao = init_knowledge_base()

# 加载示例数据
def load_sample_data():
    sample_data = [
        {
            "text": "机器学习是人工智能的重要分支，专注于算法和统计模型",
            "category": "机器学习",
            "source": "AI基础知识"
        },
        {
            "text": "深度学习基于神经网络，能够自动学习数据的层次特征",
            "category": "深度学习", 
            "source": "神经网络基础"
        },
        {
            "text": "自然语言处理使计算机能够理解、解释和生成人类语言",
            "category": "NLP",
            "source": "语言处理技术"
        },
        {
            "text": "计算机视觉让机器能够理解和分析视觉信息",
            "category": "CV",
            "source": "图像处理技术"
        },
        {
            "text": "强化学习通过试错学习最优决策策略",
            "category": "强化学习",
            "source": "决策算法"
        }
    ]
    return sample_data

# 初始化示例数据
sample_data = load_sample_data()
texts = [item["text"] for item in sample_data]
metadata = [{"category": item["category"], "source": item["source"]} for item in sample_data]
kb.add_documents(texts, metadata)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能知识库系统</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .tabs { display: flex; margin-bottom: 20px; }
        .tab { padding: 10px 20px; background: #e0e0e0; border: none; cursor: pointer; margin-right: 5px; }
        .tab.active { background: #007bff; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
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
            <h1>📚 智能知识库系统</h1>
            <p>基于阿里云text-embedding-v4和豆包AI的语义搜索知识库</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('search')">🔍 语义搜索</button>
            <button class="tab" onclick="showTab('qa')">🤖 智能问答</button>
            <button class="tab" onclick="showTab('manage')">📊 知识库管理</button>
        </div>
        
        <div id="search" class="tab-content active">
            <h2>语义搜索</h2>
            <div class="form-group">
                <label>搜索查询:</label>
                <input type="text" id="searchQuery" placeholder="例如: 机器学习算法">
            </div>
            <div class="form-group">
                <label>返回结果数:</label>
                <input type="number" id="topK" value="5" min="1" max="10">
            </div>
            <div class="form-group">
                <label>相似度阈值:</label>
                <input type="number" id="threshold" value="0.6" min="0" max="1" step="0.1">
            </div>
            <button class="btn" onclick="performSearch()">搜索</button>
            <div id="searchResults"></div>
        </div>
        
        <div id="qa" class="tab-content">
            <h2>智能问答</h2>
            <div class="form-group">
                <label>您的问题:</label>
                <input type="text" id="qaQuery" placeholder="例如: 机器学习是什么？">
            </div>
            <div class="form-group">
                <label>检索文档数:</label>
                <input type="number" id="qaTopK" value="3" min="1" max="10">
            </div>
            <button class="btn" onclick="performQA()">生成回答</button>
            <div id="qaResults"></div>
        </div>
        
        <div id="manage" class="tab-content">
            <h2>知识库管理</h2>
            <div class="form-group">
                <label>文档内容:</label>
                <textarea id="newText" rows="4" placeholder="输入新文档内容"></textarea>
            </div>
            <div class="form-group">
                <label>分类标签:</label>
                <input type="text" id="category" placeholder="例如: 机器学习">
            </div>
            <div class="form-group">
                <label>来源:</label>
                <input type="text" id="source" placeholder="例如: 技术文档">
            </div>
            <button class="btn" onclick="addDocument()">添加文档</button>
            <div id="manageResults"></div>
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
            const threshold = document.getElementById('threshold').value;
            
            if (!query) {
                alert('请输入搜索查询');
                return;
            }
            
            document.getElementById('searchResults').innerHTML = '<div class="loading">正在搜索...</div>';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query, top_k: parseInt(topK), threshold: parseFloat(threshold) })
                });
                
                const data = await response.json();
                displaySearchResults(data.results);
            } catch (error) {
                document.getElementById('searchResults').innerHTML = '<div class="result">搜索失败: ' + error.message + '</div>';
            }
        }
        
        function displaySearchResults(results) {
            const container = document.getElementById('searchResults');
            if (results.length === 0) {
                container.innerHTML = '<div class="result">未找到相关结果</div>';
                return;
            }
            
            let html = '<div class="result"><h3>搜索结果:</h3>';
            results.forEach((result, index) => {
                html += `
                    <div class="result-item">
                        <div class="similarity">相似度: ${result.similarity.toFixed(3)}</div>
                        <div><strong>内容:</strong> ${result.text}</div>
                        <div><strong>分类:</strong> ${result.metadata.category || '无'}</div>
                        <div><strong>来源:</strong> ${result.metadata.source || '无'}</div>
                    </div>
                `;
            });
            html += '</div>';
            container.innerHTML = html;
        }
        
        async function performQA() {
            const query = document.getElementById('qaQuery').value;
            const topK = document.getElementById('qaTopK').value;
            
            if (!query) {
                alert('请输入问题');
                return;
            }
            
            document.getElementById('qaResults').innerHTML = '<div class="loading">正在生成回答...</div>';
            
            try {
                const response = await fetch('/api/qa', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query, top_k: parseInt(topK) })
                });
                
                const data = await response.json();
                displayQAResults(data);
            } catch (error) {
                document.getElementById('qaResults').innerHTML = '<div class="result">问答失败: ' + error.message + '</div>';
            }
        }
        
        function displayQAResults(data) {
            const container = document.getElementById('qaResults');
            let html = '<div class="result">';
            
            if (data.answer) {
                html += `<h3>💡 AI回答:</h3><div style="margin-bottom: 20px;">${data.answer}</div>`;
            }
            
            if (data.references && data.references.length > 0) {
                html += '<h3>📚 参考内容:</h3>';
                data.references.forEach((ref, index) => {
                    html += `
                        <div class="result-item">
                            <div class="similarity">相似度: ${ref.similarity.toFixed(3)}</div>
                            <div>${ref.text}</div>
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
            
            if (!text) {
                alert('请输入文档内容');
                return;
            }
            
            document.getElementById('manageResults').innerHTML = '<div class="loading">正在添加文档...</div>';
            
            try {
                const response = await fetch('/api/add_document', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, category, source })
                });
                
                const data = await response.json();
                document.getElementById('manageResults').innerHTML = '<div class="result">文档添加成功!</div>';
                
                // 清空表单
                document.getElementById('newText').value = '';
                document.getElementById('category').value = '';
                document.getElementById('source').value = '';
            } catch (error) {
                document.getElementById('manageResults').innerHTML = '<div class="result">添加失败: ' + error.message + '</div>';
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
        query = data.get('query')
        top_k = data.get('top_k', 5)
        threshold = data.get('threshold', 0.6)
        
        results = kb.search(query, top_k=top_k, similarity_threshold=threshold)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/qa', methods=['POST'])
def qa():
    try:
        data = request.json
        query = data.get('query')
        top_k = data.get('top_k', 3)
        
        # 检索相关文档
        results = kb.search(query, top_k=top_k, similarity_threshold=0.5)
        
        if results:
            # 构建上下文
            context = "\n".join([f"{i+1}. {result['text']}" for i, result in enumerate(results)])
            
            # 使用豆包AI生成回答
            try:
                answer = doubao.knowledge_base_qa(
                    model="ep-20250714212604-xmv9d",
                    query=query,
                    context=context
                )
                return jsonify({
                    'answer': answer,
                    'references': results
                })
            except Exception as e:
                return jsonify({
                    'answer': f"抱歉，AI回答生成失败: {str(e)}",
                    'references': results
                })
        else:
            return jsonify({
                'answer': "抱歉，未找到相关文档，无法生成回答。",
                'references': []
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_document', methods=['POST'])
def add_document():
    try:
        data = request.json
        text = data.get('text')
        category = data.get('category', '')
        source = data.get('source', '')
        
        metadata = {'category': category, 'source': source}
        kb.add_documents([text], [metadata])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)