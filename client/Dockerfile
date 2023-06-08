FROM python:3.8

WORKDIR /app

COPY ./lib/chromedriver /usr/local/bin/
COPY ./lib/linux_signing_key.pub /app/

COPY ./*.py /app/
COPY ./*.yml /app/
COPY ./requirements.txt /app/requirements.txt

RUN sed -i 's/ports.ubuntu.com/mirror.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

RUN apt-key add /app/linux_signing_key.pub

RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
