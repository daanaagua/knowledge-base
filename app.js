const express = require('express');
const path = require('path');

const app = express();
app.use(express.json());
app.use(express.static('public'));

// 知识库数据
const KNOWLEDGE_DATA = {
    "AI人工智能": {
        keywords: ["ai", "人工智能", "artificial intelligence", "智能", "机器智能"],
        content: "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。"
    },
    "机器学习": {
        keywords: ["机器学习", "machine learning", "ml", "算法", "模型训练"],
        content: "机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。"
    },
    "深度学习": {
        keywords: ["深度学习", "deep learning", "神经网络", "neural network"],
        content: "深度学习是机器学习的一个子集，使用多层神经网络来模拟人脑的工作方式。"
    }
};

// 搜索函数
function searchKnowledge(query) {
    const results = [];
    const queryLower = query.toLowerCase();
    
    for (const [title, data] of Object.entries(KNOWLEDGE_DATA)) {
        for (const keyword of data.keywords) {
            if (queryLower.includes(keyword)) {
                results.push({
                    title: title,
                    content: data.content,
                    score: keyword.length
                });
                break;
            }
        }
    }
    
    return results.sort((a, b) => b.score - a.score).slice(0, 5);
}

// 路由
app.get('/', (req, res) => {
    res.send(`
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>Node.js 知识库</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
            input, button { padding: 10px; margin: 5px; }
            button { background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
            .result { margin-top: 20px; padding: 15px; background: white; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Node.js 知识库</h1>
            <input type="text" id="question" placeholder="请输入问题..." style="width: 70%;">
            <button onclick="search()">搜索</button>
            <div id="results"></div>
        </div>
        
        <script>
            async function search() {
                const question = document.getElementById('question').value;
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });
                const data = await response.json();
                
                let html = '<div class="result"><h3>搜索结果:</h3>';
                data.results.forEach(result => {
                    html += \`<div><strong>\${result.title}</strong><br>\${result.content}</div><br>\`;
                });
                html += '</div>';
                document.getElementById('results').innerHTML = html;
            }
        </script>
    </body>
    </html>
    `);
});

app.post('/api/search', (req, res) => {
    const { question } = req.body;
    const results = searchKnowledge(question || '');
    res.json({ results, timestamp: new Date().toISOString() });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

module.exports = app;