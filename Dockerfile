FROM python:2.7
ADD . /root/Book-book
WORKDIR /root
RUN pip install -r requirements.txt
