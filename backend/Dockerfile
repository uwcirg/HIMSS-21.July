FROM python:3.7

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install --requirement requirements.txt

COPY . .

EXPOSE 5000

CMD gunicorn --bind "0.0.0.0:${P_PORT:-5000}" backend_app.wsgi:app
