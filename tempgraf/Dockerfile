FROM alpine:latest

RUN apk add python3 python3-dev gcc libc-dev libffi-dev && \
    python3 -m ensurepip 

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./tempgraf.py .

ENTRYPOINT [ "python3", "tempgraf.py", "/opt/tempgraf/conf/tempgraf.json" ]