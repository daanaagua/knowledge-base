import os
from openai import OpenAI
from typing import List, Dict, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DoubaoAI:
    """豆包AI问答集成类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化豆包AI客户端
        
        Args:
            api_key: 豆包API Key，如果为None则从环境变量获取
            base_url: 豆包API基础URL，如果为None使用默认值
        """
        self.api_key = api_key or os.getenv("DOUBAO_API_KEY", "af304f26-0164-4318-84e7-d70ac67f2e07")
        self.base_url = base_url or "https://ark.cn-beijing.volces.com/api/v3"
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化OpenAI客户端"""
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info("豆包AI客户端初始化成功")
        except Exception as e:
            logger.error(f"客户端初始化失败: {e}")
            raise
    
    def chat_completion(self, 
                       model: str, 
                       messages: List[Dict], 
                       **kwargs) -> str:
        """
        调用豆包AI进行聊天补全
        
        Args:
            model: 模型端点ID
            messages: 消息列表
            **kwargs: 其他参数
            
        Returns:
            AI回复内容
        """
        if not self.client:
            raise ValueError("客户端未初始化")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"豆包AI调用失败: {e}")
            raise
    
    def knowledge_base_qa(self, 
                         model: str,
                         query: str, 
                         context: str,
                         system_prompt: Optional[str] = None) -> str:
        """
        基于知识库上下文进行问答
        
        Args:
            model: 模型端点ID
            query: 用户查询
            context: 知识库检索到的上下文
            system_prompt: 系统提示词
            
        Returns:
            AI回复内容
        """
        if not system_prompt:
            system_prompt = """你是一个专业的AI助手，请根据提供的知识库上下文内容回答用户的问题。
如果上下文中有相关信息，请基于上下文回答；如果没有相关信息，请如实告知用户你不知道。
请保持回答准确、简洁、有帮助。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"知识库上下文：\n{context}\n\n用户问题：{query}"}
        ]
        
        return self.chat_completion(model, messages)
    
    def multi_turn_conversation(self, 
                               model: str,
                               conversation_history: List[Dict],
                               system_prompt: Optional[str] = None) -> str:
        """
        多轮对话处理
        
        Args:
            model: 模型端点ID
            conversation_history: 对话历史
            system_prompt: 系统提示词
            
        Returns:
            AI回复内容
        """
        if not system_prompt:
            system_prompt = "你是一个有帮助的AI助手，请根据对话历史回应用户。"
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        
        return self.chat_completion(model, messages)

# 示例使用
if __name__ == "__main__":
    # 初始化豆包AI
    doubao = DoubaoAI()
    
    # 测试知识库问答
    test_context = """
    机器学习是人工智能的重要分支，专注于算法和统计模型。
    深度学习基于神经网络，能够自动学习数据的层次特征。
    自然语言处理使计算机能够理解、解释和生成人类语言。
    """
    
    test_query = "机器学习是什么？"
    
    response = doubao.knowledge_base_qa(
        model="ep-20250714212604-xmv9d",  # 替换为您的推理端点ID
        query=test_query,
        context=test_context
    )
    
    print(f"问题: {test_query}")
    print(f"回答: {response}")