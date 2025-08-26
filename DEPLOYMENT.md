# 智能知识库系统部署指南

## 部署到GitHub和Vercel

### 前提条件
1. 安装Git (您已经安装了PortableGit)
2. 拥有GitHub账号
3. 拥有Vercel账号 (可以用GitHub账号登录)

### 步骤1: 上传到GitHub

#### 方法1: 使用命令行 (推荐)
1. 打开PowerShell，进入knowledge_base目录:
   ```powershell
   cd d:\test8\knowledge_base
   ```

2. 初始化Git仓库:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: 智能知识库系统"
   ```

3. 在GitHub上创建新仓库:
   - 访问 https://github.com/new
   - 仓库名称: `knowledge-base`
   - 设置为Public
   - 不要初始化README

4. 连接并推送到GitHub:
   ```powershell
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/knowledge-base.git
   git push -u origin main
   ```

#### 方法2: 使用GitHub Desktop
1. 打开GitHub Desktop
2. 点击 "Add an Existing Repository from your Hard Drive"
3. 选择 `d:\test8\knowledge_base` 目录
4. 点击 "Publish repository"
5. 设置仓库名称为 `knowledge-base`
6. 确保选择 "Public"
7. 点击 "Publish Repository"

### 步骤2: 部署到Vercel

1. 访问 https://vercel.com
2. 使用GitHub账号登录
3. 点击 "New Project"
4. 选择您刚创建的 `knowledge-base` 仓库
5. 配置项目:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: 留空
   - Output Directory: ./
   - Install Command: pip install -r requirements_web.txt

6. 设置环境变量:
   点击 "Environment Variables" 添加:
   - `ALIYUN_API_KEY`: 您的阿里云API密钥
   - `DOUBAO_API_KEY`: 您的豆包API密钥

7. 点击 "Deploy"

### 步骤3: 访问应用

部署完成后，Vercel会提供一个URL，例如:
`https://knowledge-base-xxx.vercel.app`

您可以通过这个URL在任何设备上访问您的知识库系统。

## 功能说明

### Web版本功能
- **语义搜索**: 输入查询词，系统会返回相关文档
- **智能问答**: 基于知识库内容生成AI回答
- **文档管理**: 添加新文档到知识库

### API接口
- `GET /`: 主页面
- `POST /api/search`: 语义搜索
- `POST /api/qa`: 智能问答
- `POST /api/add_document`: 添加文档

## 环境变量配置

在Vercel中需要设置以下环境变量:

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| ALIYUN_API_KEY | 阿里云API密钥 | sk-xxx |
| DOUBAO_API_KEY | 豆包API密钥 | af304f26-xxx |

## 故障排除

### 常见问题

1. **部署失败**: 检查requirements_web.txt中的依赖是否正确
2. **API调用失败**: 确认环境变量设置正确
3. **搜索无结果**: 确认知识库已加载示例数据

### 日志查看
在Vercel控制台的Functions标签页可以查看运行日志。

## 本地开发

如果需要本地测试Web版本:

```bash
pip install -r requirements_web.txt
python main.py
```

然后访问 http://localhost:5000

## 更新部署

当您修改代码后，只需推送到GitHub:

```bash
git add .
git commit -m "更新说明"
git push
```

Vercel会自动重新部署。