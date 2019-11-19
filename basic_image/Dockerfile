FROM python:3.7-alpine

ADD requirements.txt requirements.txt

RUN apk add --no-cache bash git openssh gcc musl-dev libxml2-dev libxslt-dev tzdata
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
