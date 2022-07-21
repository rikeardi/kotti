FROM python:3

RUN apt-get update && apt-get install -y tzdata \
    gettext

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/usr/local/lib

WORKDIR /code
COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./runserver.sh /code/

RUN chmod +x runserver.sh
CMD ["/code/runserver.sh"]
