# 使用官方Python运行时作为基础镜像
# 可调基础镜像，默认使用 Python 3.12 slim
ARG PYTHON_IMAGE=python:3.12-slim
FROM ${PYTHON_IMAGE}

# 可选代理（通过 --build-arg 传入，加速 apt/pip）
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}
ENV NO_PROXY=${NO_PROXY}

# 设置工作目录
WORKDIR /app

# （可选）系统依赖
# 为了减少网络开销与失败率，默认跳过 apt 安装；如需 ffmpeg/curl，可在后续镜像中自行安装

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 安装应用
RUN pip install -e .

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONPATH=/app
ENV LDDC_CONFIG_PATH=/app/config

# 创建配置目录
RUN mkdir -p /app/config

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://localhost:8000/').read()" || exit 1

# 启动命令（使用包内主应用）
CMD ["python", "-m", "uvicorn", "LDDC.api.main:app", "--host", "0.0.0.0", "--port", "8000"]