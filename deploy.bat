@echo off
echo 正在初始化Git仓库...
git init

echo 添加所有文件到Git...
git add .

echo 提交文件...
git commit -m "Initial commit: 智能知识库系统"

echo 请输入您的GitHub用户名:
set /p username=

echo 请输入仓库名称 (默认: knowledge-base):
set /p reponame=
if "%reponame%"=="" set reponame=knowledge-base

echo 创建GitHub仓库并推送...
git branch -M main
git remote add origin https://github.com/%username%/%reponame%.git

echo 推送到GitHub...
git push -u origin main

echo 部署完成！
echo GitHub仓库地址: https://github.com/%username%/%reponame%
echo.
echo 接下来请访问 https://vercel.com 进行Vercel部署:
echo 1. 登录Vercel
echo 2. 点击 "New Project"
echo 3. 导入您的GitHub仓库
echo 4. 设置环境变量 ALIYUN_API_KEY 和 DOUBAO_API_KEY
echo 5. 部署完成后即可访问
pause