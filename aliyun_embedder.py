import os
import numpy as np
from openai import OpenAI
from typing import List, Optional
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AliYunEmbedder:
    """阿里云百炼大模型文本嵌入生成器"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化阿里云嵌入模型
        
        Args:
            api_key: 阿里云API Key，如果为None则从环境变量获取
            base_url: 阿里云API基础URL，如果为None使用默认值
        """
        self.api_key = api_key or os.getenv("ALIYUN_API_KEY", "sk-8a1b33b774344ba98cf22fc660b6c9a2")
        self.base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.client = None
        self.embedding_dim = 1024  # 默认维度，可根据需要调整
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化OpenAI客户端"""
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info("阿里云嵌入模型客户端初始化成功")
        except Exception as e:
            logger.error(f"客户端初始化失败: {e}")
            raise
    
    def embed_text(self, text: str, dimensions: int = 1024) -> np.ndarray:
        """
        对单个文本生成嵌入向量
        
        Args:
            text: 输入文本
            dimensions: 向量维度 (1024, 1536, 2048)
            
        Returns:
            numpy数组表示的嵌入向量
        """
        if not self.client:
            raise ValueError("客户端未初始化")
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-v4",
                input=text,
                dimensions=dimensions,
                encoding_format="float"
            )
            
            embedding = np.array(response.data[0].embedding)
            self.embedding_dim = dimensions
            return embedding
            
        except Exception as e:
            logger.error(f"嵌入生成失败: {e}")
            raise
    
    def embed_batch(self, texts: List[str], dimensions: int = 1024, batch_size: int = 10) -> np.ndarray:
        """
        批量生成文本嵌入向量
        
        Args:
            texts: 文本列表
            dimensions: 向量维度
            batch_size: 批量处理大小
            
        Returns:
            嵌入向量矩阵 (n_samples, dimensions)
        """
        if not self.client:
            raise ValueError("客户端未初始化")
        
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-v4",
                    input=batch_texts,
                    dimensions=dimensions,
                    encoding_format="float"
                )
                
                batch_embeddings = [np.array(item.embedding) for item in response.data]
                embeddings.extend(batch_embeddings)
                
                logger.info(f"已处理 {min(i + batch_size, len(texts))}/{len(texts)} 个文本")
                time.sleep(0.1)  # 避免速率限制
                
            except Exception as e:
                logger.error(f"批量嵌入生成失败: {e}")
                raise
        
        return np.array(embeddings)
    
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

if __name__ == "__main__":
    # 测试代码
    embedder = AliYunEmbedder()
    
    # 测试单个文本嵌入
    text = "机器学习是人工智能的重要分支"
    embedding = embedder.embed_text(text, dimensions=1024)
    print(f"文本: {text}")
    print(f"嵌入向量维度: {embedding.shape}")
    print(f"嵌入向量前10维: {embedding[:10]}")
    
    # 测试批量嵌入
    texts = [
        "深度学习基于神经网络",
        "自然语言处理处理文本数据",
        "计算机视觉处理图像数据"
    ]
    embeddings = embedder.embed_batch(texts, dimensions=1024)
    print(f"\n批量嵌入形状: {embeddings.shape}")
    
    # 测试相似度计算
    sim = cosine_similarity(embeddings[0], embeddings[1])
    print(f"相似度分数: {sim:.4f}")