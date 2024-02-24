FROM python:3.7

# 设置 Python 环境变量
ENV PYTHONUNBUFFERED 1

# 安装 MySQL 客户端库
RUN apt-get update && apt-get install -y --fix-missing default-libmysqlclient-dev


# 创建项目目录并设置工作目录
RUN mkdir /app
WORKDIR /app

# 复制项目依赖文件并安装依赖
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 复制项目文件
COPY . /app/



# 运行 Django 项目
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# 移除\r in windows
# RUN sed -i 's/\r//' ./start.sh

# 给start.sh可执行权限
RUN chmod +x ./start.sh

# 数据迁移，并使用uwsgi启动服务
ENTRYPOINT /bin/bash ./start.sh
