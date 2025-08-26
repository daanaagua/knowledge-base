import streamlit as st
import pandas as pd
from vector_store import KnowledgeBase
from aliyun_embedder import AliYunEmbedder
from doubao_ai import DoubaoAI
from file_processor import process_uploaded_file
import os
import time

# 设置页面配置
st.set_page_config(
    page_title="智能知识库系统 - 阿里云 & 豆包集成",
    page_icon="📚",
    layout="wide"
)

# 初始化知识库和AI客户端
@st.cache_resource
def init_knowledge_base():
    # 从环境变量获取API密钥，使用默认值作为备选
    aliyun_api_key = os.getenv("ALIYUN_API_KEY", "sk-8a1b33b774344ba98cf22fc660b6c9a2")
    doubao_api_key = os.getenv("DOUBAO_API_KEY", "af304f26-0164-4318-84e7-d70ac67f2e07")
    
    # 初始化嵌入器
    embedder = AliYunEmbedder(api_key=aliyun_api_key)
    
    # 初始化知识库
    kb = KnowledgeBase(embedder=embedder)
    
    # 初始化豆包AI
    doubao = DoubaoAI(api_key=doubao_api_key)
    
    return kb, doubao

# 加载示例数据
def load_sample_data():
    """加载示例知识库数据"""
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
        },
        {
            "text": "Transformer架构在自然语言处理中取得了突破性进展",
            "category": "NLP",
            "source": "现代架构"
        },
        {
            "text": "卷积神经网络在图像识别任务中表现出色",
            "category": "CV",
            "source": "神经网络应用"
        },
        {
            "text": "BERT模型通过双向编码器实现更好的语言理解",
            "category": "NLP", 
            "source": "预训练模型"
        },
        {
            "text": "生成对抗网络可以生成逼真的图像和数据",
            "category": "生成模型",
            "source": "创造性AI"
        },
        {
            "text": "知识图谱将信息组织成结构化的语义网络",
            "category": "知识表示",
            "source": "数据结构"
        }
    ]
    return sample_data

def main():
    st.title("📚 智能知识库系统 - 阿里云 & 豆包集成")
    st.markdown("基于阿里云text-embedding-v4和豆包AI的语义搜索知识库")
    
    # 初始化知识库和AI客户端
    kb, doubao = init_knowledge_base()
    
    # 侧边栏
    with st.sidebar:
        st.header("系统设置")
        
        # API密钥设置
        st.subheader("API配置")
        aliyun_api_key = st.text_input("阿里云API Key:", value=os.getenv("ALIYUN_API_KEY", "sk-8a1b33b774344ba98cf22fc660b6c9a2"), type="password")
        doubao_api_key = st.text_input("豆包API Key:", value=os.getenv("DOUBAO_API_KEY", "af304f26-0164-4318-84e7-d70ac67f2e07"), type="password")
        doubao_model_id = st.text_input("豆包模型ID:", value="ep-20250714212604-xmv9d")
        
        if st.button("🔄 应用API设置"):
            os.environ["ALIYUN_API_KEY"] = aliyun_api_key
            os.environ["DOUBAO_API_KEY"] = doubao_api_key
            st.cache_resource.clear()
            st.rerun()
        
        st.divider()
        
        # 知识库统计
        st.subheader("知识库统计")
        if hasattr(kb.vector_store, 'texts'):
            st.write(f"文档数量: {len(kb.vector_store.texts)}")
            st.write(f"向量维度: {kb.vector_store.embedding_dim}")
        
        st.divider()
        
        # 添加文档区域
        st.subheader("添加新文档")
        new_text = st.text_area("输入文档内容:", height=100)
        category = st.text_input("分类标签:")
        source = st.text_input("来源:")
        
        if st.button("📝 添加文档") and new_text:
            metadata = {"category": category, "source": source}
            kb.add_documents([new_text], [metadata])
            st.success("文档添加成功!")
            time.sleep(1)
            st.rerun()
        
        st.divider()
        
        # 文件上传区域
        st.subheader("文件上传")
        uploaded_file = st.file_uploader("选择DOCX或XLSX文件", type=["docx", "xlsx"])
        file_category = st.text_input("文件分类标签:", key="file_category")
        file_source = st.text_input("文件来源:", key="file_source")
        
        if uploaded_file and st.button("📤 上传文件"):
            file_ext = uploaded_file.name.split('.')[-1].lower()
            if file_ext in ['docx', 'xlsx']:
                with st.spinner("处理文件中..."):
                    try:
                        texts = process_uploaded_file(uploaded_file, file_ext)
                        if texts:
                            metadata = {"category": file_category, "source": file_source}
                            kb.add_documents(texts, [metadata] * len(texts))
                            st.success(f"文件上传成功！提取了 {len(texts)} 条文本")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("文件内容为空，请检查文件格式")
                    except Exception as e:
                        st.error(f"文件处理失败: {e}")
            else:
                st.error("不支持的文件格式，请上传DOCX或XLSX文件")
    
    # 主内容区
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 语义搜索", "🤖 智能问答", "📊 知识库管理", "ℹ️ 系统信息"])
    
    with tab1:
        st.header("语义搜索")
        
        # 搜索参数
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input("输入搜索查询:", placeholder="例如: 机器学习算法", key="search_query")
        with col2:
            top_k = st.slider("返回结果数:", 1, 10, 5, key="search_top_k")
            similarity_threshold = st.slider("相似度阈值:", 0.0, 1.0, 0.6, 0.1, key="search_threshold")
        
        if query:
            with st.spinner("正在搜索..."):
                results = kb.search(query, top_k=top_k, similarity_threshold=similarity_threshold)
            
            if results:
                st.success(f"找到 {len(results)} 个相关结果")
                
                for i, result in enumerate(results, 1):
                    with st.expander(f"结果 #{i} - 相似度: {result['similarity']:.3f}"):
                        st.write(f"**内容:** {result['text']}")
                        if result['metadata']:
                            st.write(f"**分类:** {result['metadata'].get('category', '无')}")
                            st.write(f"**来源:** {result['metadata'].get('source', '无')}")
            else:
                st.warning("未找到相关结果，请尝试调整搜索条件")
    
    with tab2:
        st.header("智能问答")
        st.info("基于知识库内容的智能问答，使用豆包AI生成回答")
        
        # 问答参数
        qa_query = st.text_input("输入您的问题:", placeholder="例如: 机器学习是什么？", key="qa_query")
        qa_top_k = st.slider("检索文档数:", 1, 10, 3, key="qa_top_k")
        qa_threshold = st.slider("检索阈值:", 0.0, 1.0, 0.5, 0.1, key="qa_threshold")
        
        if st.button("🧠 生成回答", key="generate_answer") and qa_query:
            with st.spinner("正在检索知识库并生成回答..."):
                # 首先检索相关文档
                results = kb.search(qa_query, top_k=qa_top_k, similarity_threshold=qa_threshold)
                
                if results:
                    # 构建上下文
                    context = "\n".join([f"{i+1}. {result['text']}" for i, result in enumerate(results)])
                    
                    # 使用豆包AI生成回答
                    try:
                        answer = doubao.knowledge_base_qa(
                            model=doubao_model_id,
                            query=qa_query,
                            context=context
                        )
                        
                        st.success("回答生成完成!")
                        st.markdown("### 💡 AI回答:")
                        st.write(answer)
                        
                        st.markdown("### 📚 参考内容:")
                        for i, result in enumerate(results, 1):
                            with st.expander(f"参考文档 #{i} - 相似度: {result['similarity']:.3f}"):
                                st.write(result['text'])
                                if result['metadata']:
                                    st.write(f"分类: {result['metadata'].get('category', '无')}")
                                    st.write(f"来源: {result['metadata'].get('source', '无')}")
                    
                    except Exception as e:
                        st.error(f"生成回答时出错: {e}")
                else:
                    st.warning("未找到相关文档，无法生成回答")
    
    with tab3:
        st.header("知识库管理")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("初始化知识库")
            if st.button("📥 加载示例数据"):
                sample_data = load_sample_data()
                texts = [item["text"] for item in sample_data]
                metadata = [{"category": item["category"], "source": item["source"]} 
                           for item in sample_data]
                
                kb.add_documents(texts, metadata)
                st.success("示例数据加载完成!")
                time.sleep(1)
                st.rerun()
            
            st.divider()
            
            st.subheader("导出知识库")
            if st.button("💾 保存知识库"):
                kb.save("my_knowledge_base")
                st.success("知识库已保存到文件!")
        
        with col2:
            st.subheader("导入知识库")
            if st.button("📤 加载知识库") and os.path.exists("my_knowledge_base.index"):
                kb.load("my_knowledge_base")
                st.success("知识库加载完成!")
                time.sleep(1)
                st.rerun()
            elif not os.path.exists("my_knowledge_base.index"):
                st.info("没有找到已保存的知识库文件")
    
    with tab4:
        st.header("系统信息")
        
        st.subheader("技术架构")
        st.markdown("""
        - **嵌入模型**: 阿里云 text-embedding-v4 (最高2048维)
        - **AI引擎**: 豆包大模型
        - **向量存储**: FAISS 高效相似度搜索
        - **前端界面**: Streamlit Web应用
        - **搜索算法**: 余弦相似度 + 近似最近邻
        """)
        
        st.subheader("使用说明")
        st.markdown("""
        1. 在侧边栏配置API密钥和模型ID
        2. 添加文档或加载示例数据构建知识库
        3. 使用语义搜索查找相关文档
        4. 使用智能问答获取AI生成的回答
        5. 使用管理功能保存/加载知识库
        """)
        
        st.subheader("性能指标")
        if hasattr(kb.vector_store, 'index'):
            stats = kb.vector_store.get_stats()
            st.write(f"- 总文档数: {stats['total_documents']}")
            st.write(f"- 索引大小: {stats['index_size']}")
            st.write(f"- 向量维度: {stats['embedding_dim']}")

if __name__ == "__main__":
    main()