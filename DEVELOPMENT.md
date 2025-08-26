# 开发工作流程指南

## 1. 本地开发环境设置

### 首次设置
```bash
# 进入项目目录
cd d:\test8\knowledge_base

# 运行设置脚本
setup_dev.bat

# 或手动设置
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements_web.txt
```

### 环境变量配置
复制 `.env.example` 为 `.env` 并填入您的API密钥：
```
ALIYUN_API_KEY=sk-8a1b33b774344ba98cf22fc660b6c9a2
DOUBAO_API_KEY=af304f26-0164-4318-84e7-d70ac67f2e07
FLASK_ENV=development
FLASK_DEBUG=True
```

## 2. 本地开发和测试

### 启动开发服务器
```bash
# 激活虚拟环境
venv\Scripts\activate

# 启动Streamlit版本（原版）
streamlit run app.py

# 或启动Flask版本（Web版）
python main.py

# 或启动简化版本
python app_simple.py
```

### 访问地址
- Streamlit版本: http://localhost:8501
- Flask版本: http://localhost:5000
- 简化版本: http://localhost:5000

### 测试功能
```bash
# 运行测试（如果有）
python -m pytest tests/

# 手动测试API
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "机器学习"}'
```

## 3. 版本更新流程

### 步骤1: 本地开发
1. 激活虚拟环境: `venv\Scripts\activate`
2. 修改代码（添加新功能）
3. 本地测试确保功能正常
4. 更新文档和版本号

### 步骤2: 提交到Git
```bash
# 查看修改
git status
git diff

# 添加修改的文件
git add .

# 提交修改
git commit -m "feat: 添加新功能描述"

# 推送到GitHub
git push origin main
```

### 步骤3: Vercel自动部署
- Vercel会自动检测到GitHub的更新
- 自动触发重新部署
- 通常2-3分钟完成部署

### 步骤4: 验证部署
1. 访问Vercel提供的URL
2. 测试新功能是否正常工作
3. 检查日志确认无错误

## 4. 常用开发命令

### Git操作
```bash
# 查看当前状态
git status

# 查看提交历史
git log --oneline -10

# 创建新分支开发功能
git checkout -b feature/new-feature

# 合并分支
git checkout main
git merge feature/new-feature

# 回滚到上一个版本
git reset --hard HEAD~1
```

### 依赖管理
```bash
# 安装新依赖
pip install package_name

# 更新requirements.txt
pip freeze > requirements.txt

# 或只更新Web版本依赖
pip freeze | grep -E "(flask|requests|numpy)" > requirements_web.txt
```

## 5. 调试技巧

### 本地调试
```python
# 在代码中添加调试信息
import logging
logging.basicConfig(level=logging.DEBUG)

# 使用print调试
print(f"Debug: {variable_name}")

# 使用断点调试
import pdb; pdb.set_trace()
```

### Vercel日志查看
1. 登录Vercel控制台
2. 选择项目
3. 点击"Functions"标签
4. 查看实时日志和错误信息

## 6. 常见问题解决

### 依赖安装失败
```bash
# 清理缓存重新安装
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

### 环境变量问题
```bash
# 检查环境变量是否加载
python -c "import os; print(os.getenv('ALIYUN_API_KEY'))"
```

### 端口占用
```bash
# Windows查看端口占用
netstat -ano | findstr :5000

# 杀死进程
taskkill /PID <PID> /F
```

## 7. 版本发布最佳实践

### 语义化版本控制
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式化
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

### 发布检查清单
- [ ] 本地测试通过
- [ ] 代码已提交到Git
- [ ] 更新了文档
- [ ] 检查了依赖版本
- [ ] 验证了环境变量
- [ ] 测试了主要功能

## 8. 高级功能开发

### 添加新的API端点
```python
@app.route('/api/new-feature', methods=['POST'])
def new_feature():
    try:
        data = request.json
        # 处理逻辑
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 添加新的前端功能
1. 修改HTML模板
2. 添加JavaScript函数
3. 更新CSS样式
4. 测试用户交互

### 数据库集成（可选）
```python
# 使用SQLite作为轻量数据库
import sqlite3

def init_db():
    conn = sqlite3.connect('knowledge_base.db')
    # 创建表结构
    return conn
```

## 9. 性能优化

### 缓存策略
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query):
    # 缓存搜索结果
    pass
```

### 异步处理
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def async_search(query):
    # 异步搜索处理
    pass
```

## 10. 监控和日志

### 添加日志记录
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("应用启动")
```

### 性能监控
```python
import time

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} 执行时间: {end_time - start_time:.2f}秒")
        return result
    return wrapper