# 智能知识库系统 - 基于嵌入模型

这是一个基于嵌入模型的智能知识库系统，使用语义搜索技术实现高效的文档检索。

## 技术原理

### 嵌入模型 (Embedding Models)
嵌入模型将文本转换为高维向量表示，核心原理包括：
- **向量化表示**: 文本 → 高维向量 (通常384-768维)
- **语义保持**: 语义相似的文本在向量空间中距离相近
- **上下文学习**: 基于Transformer架构捕获上下文信息
- **降维技术**: 将稀疏表示压缩为稠密向量

### 知识库架构
1. **文档处理**: 文本清洗、分块、预处理
2. **嵌入生成**: 使用Sentence-BERT生成文本向量
3. **向量存储**: FAISS向量数据库高效存储和检索
4. **语义搜索**: 余弦相似度计算和近似最近邻搜索

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 运行Web应用
```bash
streamlit run knowledge_base/app.py
```

### 2. 命令行使用示例
```python
from vector_store import KnowledgeBase

# 初始化知识库
kb = KnowledgeBase()

# 添加文档
documents = [
    "机器学习是人工智能的重要分支",
    "深度学习基于神经网络架构",
    "自然语言处理处理文本数据"
]
kb.add_documents(documents)

# 语义搜索
results = kb.search("AI机器学习")
for result in results:
    print(f"相似度: {result['similarity']:.3f} - {result['text']}")
```

## 项目结构

```
knowledge_base/
├── embedding_utils.py    # 文本嵌入工具类
├── vector_store.py       # 向量存储和检索类
├── app.py               # Streamlit Web界面
├── requirements.txt     # 项目依赖
└── README.md           # 项目说明
```

## 核心功能

- **语义搜索**: 基于内容的相似度检索，而非关键词匹配
- **实时添加**: 动态添加新文档到知识库
- **持久化存储**: 支持知识库的保存和加载
- **可配置阈值**: 调整相似度阈值过滤结果
- **元数据支持**: 为文档添加分类和来源信息

## 性能特点

- **高效检索**: FAISS支持毫秒级相似度搜索
- **可扩展性**: 支持大规模文档存储
- **准确性**: 基于预训练模型的语义理解
- **灵活性**: 支持多种嵌入模型切换

## 应用场景

- 企业知识管理系统
- 学术文献检索
- 客服问答系统
- 内容推荐引擎
- 智能文档管理

## 模型选择

默认使用 `all-MiniLM-L6-v2` 模型，平衡速度和精度。可根据需要切换其他Sentence-BERT模型：
- `all-mpnet-base-v2` (更高精度)
- `multi-qa-MiniLM-L6-cos-v1` (问答优化)
- `paraphrase-MiniLM-L3-v2` (释义检测)

## 注意事项

1. 首次运行会自动下载预训练模型(约80MB)
2. 建议相似度阈值设置在0.5-0.7之间
3. 文档长度建议在50-500字符以获得最佳效果
4. 支持中英文混合文本处理