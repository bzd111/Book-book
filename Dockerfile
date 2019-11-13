FROM python:3.7-alpine
# FROM python:3.7
ADD . /opt/book
WORKDIR /opt/book
# RUN apk add --no-cache bash git openssh gcc musl-dev libxml2-dev libxmlsec1-dev
RUN apk add --no-cache bash git openssh gcc musl-dev libxml2-dev libxslt-dev
# RUN yum install bash git openssh -y
# RUN useradd redis
# RUN chown redis:redis -R /opt/Book-book
RUN pip install -r /opt/book/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENTRYPOINT ["python", "-m", "main"]

