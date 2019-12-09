FROM python:3.7-alpine

LABEL Name=ipbook Version=0.0.1
WORKDIR /ipbook

# install sqlite3
RUN apk add sqlite
RUN apk add socat

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

# gen database
RUN ["python", "-c", "from app.models import init_db ; init_db()"]

COPY wsgi.py config.py ./

EXPOSE 5000
CMD ["gunicorn", "--bind", ":5000", "wsgi:app"]