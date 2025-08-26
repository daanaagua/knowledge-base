#!/usr/bin/env python3
"""
知识库系统演示脚本
展示嵌入模型和向量检索的核心功能
"""

import numpy as np
from embedding_utils import TextEmbedder
from vector_store import KnowledgeBase

def main():
    print("🤖 智能知识库系统演示")
    print("=" * 50)
    
    # 初始化知识库
    print("正在初始化知识库和嵌入模型...")
    kb = KnowledgeBase()
    
    # 示例文档数据
    documents = [
        "机器学习是人工智能的重要分支，专注于算法和统计模型",
        "深度学习基于神经网络，能够自动学习数据的层次特征",
        "自然语言处理使计算机能够理解、解释和生成人类语言",
        "计算机视觉让机器能够理解和分析视觉信息",
        "强化学习通过试错学习最优决策策略",
        "Transformer架构在自然语言处理中取得了突破性进展",
        "卷积神经网络在图像识别任务中表现出色",
        "BERT模型通过双向编码器实现更好的语言理解"
    ]
    
    # 添加文档到知识库
    print(f"添加 {len(documents)} 个文档到知识库...")
    kb.add_documents(documents)
    
    print("\n📊 知识库统计信息:")
    stats = kb.vector_store.get_stats()
    print(f"  文档数量: {stats['total_documents']}")
    print(f"  向量维度: {stats['embedding_dim']}")
    print(f"  索引大小: {stats['index_size']}")
    
    # 测试搜索查询
    test_queries = [
        "人工智能的算法",
        "神经网络应用",
        "语言处理技术",
        "图像识别方法"
    ]
    
    print("\n🔍 语义搜索测试:")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n查询: '{query}'")
        results = kb.search(query, top_k=2, similarity_threshold=0.5)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. 相似度: {result['similarity']:.3f}")
                print(f"     内容: {result['text']}")
        else:
            print("  未找到相关结果")
    
    # 演示向量相似度计算
    print("\n📐 向量相似度计算演示:")
    print("=" * 50)
    
    # 获取一些文档的嵌入向量
    text1 = "机器学习算法"
    text2 = "深度学习模型" 
    text3 = "计算机视觉技术"
    
    embedder = TextEmbedder()
    vec1 = embedder.embed_text(text1)
    vec2 = embedder.embed_text(text2)
    vec3 = embedder.embed_text(text3)
    
    # 计算相似度
    sim12 = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    sim13 = np.dot(vec1, vec3) / (np.linalg.norm(vec1) * np.linalg.norm(vec3))
    
    print(f"文本1: '{text1}'")
    print(f"文本2: '{text2}'")
    print(f"文本3: '{text3}'")
    print(f"\n相似度比较:")
    print(f"  文本1 vs 文本2: {sim12:.3f} (语义更相近)")
    print(f"  文本1 vs 文本3: {sim13:.3f}")
    
    # 保存知识库演示
    print("\n💾 知识库持久化演示:")
    save_path = "demo_knowledge_base"
    kb.save(save_path)
    print(f"知识库已保存到: {save_path}")
    
    # 加载知识库演示
    kb_new = KnowledgeBase()
    kb_new.load(save_path)
    print(f"知识库加载成功，包含 {len(kb_new.vector_store.texts)} 个文档")
    
    print("\n✅ 演示完成！")
    print("\n下一步建议:")
    print("1. 运行 'streamlit run app.py' 启动Web界面")
    print("2. 编辑 demo.py 添加自己的文档数据")
    print("3. 尝试不同的查询和相似度阈值")

if __name__ == "__main__":
    main()