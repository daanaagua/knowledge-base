@echo off
echo 设置本地开发环境...

echo 创建虚拟环境...
python -m venv venv

echo 激活虚拟环境...
call venv\Scripts\activate

echo 安装开发依赖...
pip install -r requirements.txt
pip install -r requirements_web.txt

echo 安装开发工具...
pip install pytest flask-testing python-dotenv

echo 创建环境变量文件...
if not exist .env (
    echo ALIYUN_API_KEY=sk-8a1b33b774344ba98cf22fc660b6c9a2 > .env
    echo DOUBAO_API_KEY=af304f26-0164-4318-84e7-d70ac67f2e07 >> .env
    echo FLASK_ENV=development >> .env
    echo FLASK_DEBUG=True >> .env
)

echo 开发环境设置完成！
echo 使用以下命令启动开发服务器：
echo   call venv\Scripts\activate
echo   python main.py
pause