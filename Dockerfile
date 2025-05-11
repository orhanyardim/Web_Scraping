FROM python:3.10-slim

# Sistem güncelle ve cron kur
RUN apt-get update && apt-get install -y cron

# Gerekli Python paketlerini yükle
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH="${PYTHONPATH}:/app/src"


# Uygulama dosyalarını kopyala
COPY . .

# Cron job dosyasını ekle
COPY cronjob /etc/cron.d/scrape-cron

# Cron job dosyasına uygun izinleri ver
RUN chmod 0644 /etc/cron.d/scrape-cron

# Crontab’a ekle
RUN crontab /etc/cron.d/scrape-cron

# Log dosyası oluştur
RUN touch /var/log/cron.log

# Cron ve uygulamayı başlat
CMD cron && tail -f /var/log/cron.log
