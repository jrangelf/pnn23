FROM ubuntu:focal 

WORKDIR /app


#RUN apt update && apt install -y --no-install-recommends \
#    build-essential \
#    && rm -rf /var/lib/apt/lists/*

RUN apt update -y
RUN apt upgrade -y

RUN apt install build-essential python3 -y
RUN apt install python-dev -y
RUN apt install python3-pip -y


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

ENV PATH="/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"
ENV PYTHONPATH=/app



#CMD ["gunicorn", "--bind", "0.0.0.0:8008", "--reload", "wsgi:app"]
CMD ["gunicorn", "--bind", "0.0.0.0:8008", "--worker-class", "gevent", "--workers", "9", "wsgi:app"]
