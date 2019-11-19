FROM zidy/basic-book:0.2.0
# FROM python:3.7
ADD . /opt/book
WORKDIR /opt/book

ENTRYPOINT ["python", "-m", "main"]
