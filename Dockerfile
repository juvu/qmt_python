# 使用官方的Python镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制requirements.txt到容器中
COPY requirements.txt .

# 安装Python依赖
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple/

# 复制项目代码到容器中
COPY . .

# 暴露FastAPI默认端口
EXPOSE 8000

# 设置启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
