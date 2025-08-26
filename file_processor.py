import io
from docx import Document
import pandas as pd
from typing import List, Tuple
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_docx_file(file) -> List[str]:
    """
    处理DOCX文件，提取文本内容
    
    Args:
        file: 上传的文件对象
        
    Returns:
        提取的文本段落列表
    """
    try:
        doc = Document(io.BytesIO(file.read()))
        texts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # 忽略空段落
                texts.append(paragraph.text.strip())
        logger.info(f"从DOCX文件中提取了 {len(texts)} 个段落")
        return texts
    except Exception as e:
        logger.error(f"处理DOCX文件时出错: {e}")
        raise

def process_xlsx_file(file) -> List[str]:
    """
    处理XLSX文件，提取文本内容
    
    Args:
        file: 上传的文件对象
        
    Returns:
        提取的文本内容列表
    """
    try:
        df = pd.read_excel(io.BytesIO(file.read()))
        texts = []
        
        # 提取所有单元格的文本内容
        for column in df.columns:
            for cell in df[column].dropna():
                if isinstance(cell, str) and cell.strip():
                    texts.append(cell.strip())
                elif not isinstance(cell, str) and not pd.isna(cell):
                    texts.append(str(cell).strip())
        
        logger.info(f"从XLSX文件中提取了 {len(texts)} 条文本")
        return texts
    except Exception as e:
        logger.error(f"处理XLSX文件时出错: {e}")
        raise

def process_uploaded_file(file, file_type: str) -> List[str]:
    """
    处理上传的文件，根据文件类型调用相应的处理函数
    
    Args:
        file: 上传的文件对象
        file_type: 文件类型 ('docx' 或 'xlsx')
        
    Returns:
        提取的文本内容列表
    """
    if file_type == 'docx':
        return process_docx_file(file)
    elif file_type == 'xlsx':
        return process_xlsx_file(file)
    else:
        raise ValueError(f"不支持的文件类型: {file_type}")

# 示例使用
if __name__ == "__main__":
    # 测试代码
    print("文件处理器测试")
    # 这里可以添加测试代码，但由于需要实际文件，暂时省略