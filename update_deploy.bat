@echo off
echo 快速更新和部署脚本
echo.

echo 1. 检查当前状态...
git status

echo.
echo 2. 添加所有修改...
git add .

echo.
set /p commit_msg="请输入提交信息: "
if "%commit_msg%"=="" set commit_msg="更新功能"

echo 3. 提交修改...
git commit -m "%commit_msg%"

echo.
echo 4. 推送到GitHub...
git push origin main

echo.
echo 5. 部署完成！
echo Vercel将自动检测更新并重新部署
echo 请访问Vercel控制台查看部署状态
echo.

echo 6. 打开相关页面...
start https://vercel.com/dashboard
start https://github.com/daanaagua/knowledge-base

pause