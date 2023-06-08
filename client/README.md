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

## 流程

### 引导

程序入口为[main.py](main.py)，会实例化一个位于[rpa.py](rpa.py)的`RPA`对象，并在主线程中无限循环。

### rpa.py RPA

通过`AppManager`启动指定数量位于[app.py](app.py)的`App`对象，通过子线程运行所有`App`对象，定时检查是否需要重启`App`。

### app.py App

每个`App`维护一个浏览器和若干个任务，`App`会循环处理任务：

- 如果当前已经无更多任务，会向服务端请求一定数量的任务，
- 当一个任务执行完成后，会向服务端发送更新请求，更新完成后立即尝试执行下一个任务。
- 如果服务端返回任务数量为`0`，则线程会休眠一段时间，防止 CPU 耗尽。
- 执行任务前对比本地脚本是否存在，且版本号是否匹配，如果不匹配则先向服务端拉取对应的脚本，任务脚本由`ScriptManager`维护。