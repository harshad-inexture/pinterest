FROM python:3.9-alpine

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev

COPY ./requirements.txt /Pinterest-Clone/requirements.txt

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
