# RPA Client

## 安装

### Python

请确保 Python 版本 3.8 及以上

### 依赖

```
selenium==4.9.1
requests==2.31.0
PyYAML==6.0
```

```shell
pip install -r requirements.txt
```

### Chrome

普通桌面版 Chrome 即可。

## Docker

```dockerfile
FROM python:3.8

WORKDIR /app

# 复制依赖到指定目录
COPY ./lib/chromedriver /usr/local/bin/
COPY ./lib/linux_signing_key.pub /app/

# 复制源码到工作目录
COPY ./*.py /app/
COPY ./requirements.txt /app/requirements.txt

# 设置大陆镜像
RUN sed -i 's/ports.ubuntu.com/mirror.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 设置 Google 镜像以及信任密钥
RUN apt-key add /app/linux_signing_key.pub
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# 更新 apt 并安装 Google Chrome
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# 安装依赖
RUN pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```

或者直接运行 [build.sh](build.sh)

## 运行

```shell
python main.py
```