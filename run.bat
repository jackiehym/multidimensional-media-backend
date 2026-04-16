@echo off
REM 启动后端服务
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload