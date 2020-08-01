FROM ubuntu

COPY requirements.txt /

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y python3.6 python3-pip

RUN pip3 install -r /requirements.txt

EXPOSE 8000

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
