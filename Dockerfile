FROM python:2.7
ADD . /root/Book-book
WORKDIR /root
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple