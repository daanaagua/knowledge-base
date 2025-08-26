import numpy as np
import faiss
import pickle
import os
from typing import List, Dict, Tuple, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """向量存储和检索类，使用FAISS进行高效相似度搜索"""
    
    def __init__(self, embedding_dim: int = 1024):
        """
        初始化向量存储
        
        Args:
            embedding_dim: 嵌入向量的维度 (支持1024, 1536, 2048等)
        """
        self.embedding_dim = embedding_dim
        self.index = None
        self.texts = []  # 存储原始文本
        self.metadata = []  # 存储元数据
        self._initialize_index()
    
    def _initialize_index(self):
        """初始化FAISS索引"""
        # 使用内积相似度（余弦相似度的近似）
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        logger.info(f"初始化FAISS索引，维度: {self.embedding_dim}")
    
    def add_documents(self, texts: List[str], embeddings: np.ndarray, 
                     metadata: Optional[List[Dict]] = None):
        """
        添加文档到向量存储
        
        Args:
            texts: 文本列表
            embeddings: 对应的嵌入向量
            metadata: 可选的元数据列表
        """
        if len(texts) != len(embeddings):
            raise ValueError("文本数量和嵌入向量数量不匹配")
        
        if embeddings.shape[1] != self.embedding_dim:
            raise ValueError(f"嵌入向量维度不匹配，期望 {self.embedding_dim}，实际 {embeddings.shape[1]}")
        
        # 转换为float32并标准化向量（FAISS需要float32类型）
        embeddings = embeddings.astype(np.float32)
        faiss.normalize_L2(embeddings)
        
        # 添加到索引
        self.index.add(embeddings)
        
        # 存储文本和元数据
        self.texts.extend(texts)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(texts))
        
        logger.info(f"添加了 {len(texts)} 个文档到向量存储")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5, 
               similarity_threshold: float = 0.6) -> List[Dict]:
        """
        搜索相似的文档
        
        Args:
            query_embedding: 查询向量的嵌入
            top_k: 返回最相似的前k个结果
            similarity_threshold: 相似度阈值，只返回高于此阈值的结果
            
        Returns:
            相似文档列表，包含文本、相似度和元数据
        """
        if self.index.ntotal == 0:
            return []
        
        # 标准化查询向量
        query_embedding = query_embedding.astype(np.float32)
        faiss.normalize_L2(query_embedding.reshape(1, -1))
        
        # 搜索最相似的向量
        distances, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < 0:  # FAISS返回-1表示没有足够的结果
                continue
            
            # 将内积距离转换为余弦相似度
            similarity = float(distance)
            
            if similarity >= similarity_threshold:
                result = {
                    'text': self.texts[idx],
                    'similarity': similarity,
                    'metadata': self.metadata[idx],
                    'rank': i + 1
                }
                results.append(result)
        
        return results
    
    def save(self, filepath: str):
        """保存向量存储到文件"""
        # 创建目录
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # 保存FAISS索引
        faiss.write_index(self.index, f"{filepath}.index")
        
        # 保存文本和元数据
        data = {
            'texts': self.texts,
            'metadata': self.metadata,
            'embedding_dim': self.embedding_dim
        }
        
        with open(f"{filepath}.data", 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"向量存储已保存到: {filepath}")
    
    def load(self, filepath: str):
        """从文件加载向量存储"""
        # 加载FAISS索引
        self.index = faiss.read_index(f"{filepath}.index")
        
        # 加载文本和元数据
        with open(f"{filepath}.data", 'rb') as f:
            data = pickle.load(f)
        
        self.texts = data['texts']
        self.metadata = data['metadata']
        self.embedding_dim = data['embedding_dim']
        
        logger.info(f"向量存储已加载，包含 {len(self.texts)} 个文档")
    
    def get_stats(self) -> Dict:
        """获取向量存储的统计信息"""
        return {
            'total_documents': len(self.texts),
            'embedding_dim': self.embedding_dim,
            'index_size': self.index.ntotal
        }

class KnowledgeBase:
    """知识库管理类，整合嵌入生成和向量存储"""
    
    def __init__(self, embedder=None, model_name: str = 'all-MiniLM-L6-v2'):
        """
        初始化知识库
        
        Args:
            embedder: 嵌入器实例，如果为None则使用默认的TextEmbedder
            model_name: 嵌入模型名称（仅当embedder为None时使用）
        """
        if embedder is None:
            from .embedding_utils import TextEmbedder
            self.embedder = TextEmbedder(model_name)
        else:
            self.embedder = embedder
            
        self.vector_store = VectorStore(self.embedder.get_embedding_dim())
        logger.info("知识库初始化完成")
    
    def add_documents(self, texts: List[str], metadata: Optional[List[Dict]] = None):
        """
        添加文档到知识库
        
        Args:
            texts: 文本列表
            metadata: 可选的元数据列表
        """
        logger.info(f"正在为 {len(texts)} 个文档生成嵌入...")
        embeddings = self.embedder.embed_batch(texts)
        self.vector_store.add_documents(texts, embeddings, metadata)
    
    def search(self, query: str, top_k: int = 5, 
               similarity_threshold: float = 0.6) -> List[Dict]:
        """
        在知识库中搜索
        
        Args:
            query: 查询文本
            top_k: 返回最相似的前k个结果
            similarity_threshold: 相似度阈值
            
        Returns:
            相似文档列表
        """
        query_embedding = self.embedder.embed_text(query)
        return self.vector_store.search(query_embedding, top_k, similarity_threshold)
    
    def save(self, filepath: str):
        """保存知识库"""
        self.vector_store.save(filepath)
    
    def load(self, filepath: str):
        """加载知识库"""
        self.vector_store.load(filepath)

# 示例使用
if __name__ == "__main__":
    # 创建知识库实例
    kb = KnowledgeBase()
    
    # 示例文档
    documents = [
        "机器学习是人工智能的重要分支，专注于算法和统计模型",
        "深度学习基于神经网络，能够自动学习数据的层次特征",
        "自然语言处理使计算机能够理解、解释和生成人类语言",
        "计算机视觉让机器能够理解和分析视觉信息",
        "强化学习通过试错学习最优决策策略"
    ]
    
    # 添加文档到知识库
    kb.add_documents(documents)
    
    # 搜索示例
    query = "人工智能的机器学习"
    results = kb.search(query, top_k=3)
    
    print(f"查询: '{query}'")
    print("搜索结果:")
    for result in results:
        print(f"相似度: {result['similarity']:.3f} - {result['text']}")
    
    # 保存知识库
    kb.save("example_knowledge_base")