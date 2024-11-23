FROM python:3.11-slim

WORKDIR /usr/src/app

# Umgebungsvariable für Setuptools
ENV SETUPTOOLS_USE_DISTUTILS=stdlib
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System-Pakete installieren, einschließlich distutils
RUN apt-get update && apt-get install -y \
    python3-distutils \
    python3-setuptools \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    git \
    && apt-get clean

# Upgrade von pip und Installation der Abhängigkeiten
RUN /usr/local/bin/python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des Projekts
COPY . .

# Arbeitsverzeichnis für das Backend setzen
RUN cd ./filmflix_backend

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]