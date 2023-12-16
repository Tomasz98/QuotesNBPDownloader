FROM python:3.9-slim

# Instalacja cron
RUN apt-get update && apt-get install -y cron

# Kopiowanie skryptu cron do kontenera
COPY crontab /etc/cron.d/my-cron-job

# Nadanie uprawnień wykonywalnych
RUN chmod 0644 /etc/cron.d/my-cron-job
RUN touch /var/log/cron.log

# Aplikacja
WORKDIR /app
COPY requirements .
RUN pip install --no-cache-dir -r requirements
COPY . .
RUN chmod +x /app/main.py

# Uruchomienie cron w tle
CMD cron -f
