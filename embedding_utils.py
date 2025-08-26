import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextEmbedder:
    """文本嵌入生成器类"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        初始化文本嵌入模型
        
        Args:
            model_name: 预训练模型名称，默认为 all-MiniLM-L6-v2
        """
        self.model_name = model_name
        self.model = None
        self.embedding_dim = None
        logger.info(f"正在加载嵌入模型: {model_name}")
        self._load_model()
    
    def _load_model(self):
        """加载预训练模型"""
        try:
            self.model = SentenceTransformer(self.model_name)
            # 测试获取向量维度
            test_embedding = self.model.encode(["测试文本"])
            self.embedding_dim = test_embedding.shape[1]
            logger.info(f"模型加载成功，向量维度: {self.embedding_dim}")
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            raise
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        对单个文本生成嵌入向量
        
        Args:
            text: 输入文本
            
        Returns:
            numpy数组表示的嵌入向量
        """
        if not self.model:
            raise ValueError("模型未初始化")
        
        embedding = self.model.encode([text])
        return embedding[0]
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        批量生成文本嵌入向量
        
        Args:
            texts: 文本列表
            
        Returns:
            嵌入向量矩阵 (n_samples, embedding_dim)
        """
        if not self.model:
            raise ValueError("模型未初始化")
        
        embeddings = self.model.encode(texts)
        return embeddings
    
    def get_embedding_dim(self) -> int:
        """获取嵌入向量的维度"""
        return self.embedding_dim

# 工具函数
def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    计算两个向量的余弦相似度
    
    Args:
        vec1: 向量1
        vec2: 向量2
        
    Returns:
        余弦相似度分数 (0-1之间)
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

def find_similar_vectors(
    query_vector: np.ndarray, 
    vectors: np.ndarray, 
    top_k: int = 5
) -> Tuple[List[int], List[float]]:
    """
    在向量集合中查找与查询向量最相似的向量
    
    Args:
        query_vector: 查询向量
        vectors: 向量集合
        top_k: 返回最相似的前k个结果
        
    Returns:
        (索引列表, 相似度分数列表)
    """
    similarities = []
    for i, vector in enumerate(vectors):
        similarity = cosine_similarity(query_vector, vector)
        similarities.append((i, similarity))
    
    # 按相似度降序排序
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    indices = [idx for idx, _ in similarities[:top_k]]
    scores = [score for _, score in similarities[:top_k]]
    
    return indices, scores

if __name__ == "__main__":
    # 测试代码
    embedder = TextEmbedder()
    
    # 测试单个文本嵌入
    text = "机器学习是人工智能的重要分支"
    embedding = embedder.embed_text(text)
    print(f"文本: {text}")
    print(f"嵌入向量维度: {embedding.shape}")
    print(f"嵌入向量前10维: {embedding[:10]}")
    
    # 测试批量嵌入
    texts = [
        "深度学习基于神经网络",
        "自然语言处理处理文本数据",
        "计算机视觉处理图像数据"
    ]
    embeddings = embedder.embed_batch(texts)
    print(f"\n批量嵌入形状: {embeddings.shape}")
    
    # 测试相似度计算
    sim = cosine_similarity(embeddings[0], embeddings[1])
    print(f"相似度分数: {sim:.4f}")