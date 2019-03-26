FROM python:2.7
ADD . /opt/Book-book
WORKDIR /opt
# RUN useradd redis
# RUN chown redis:redis -R /opt/Book-book
RUN pip install -r /opt/Book-book/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
