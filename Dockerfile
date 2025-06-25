FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-utils \
    x11-apps \
    scrot \
    xdotool \
    wmctrl \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxtst-dev \
    libgtk-3-0 \
    libsm6 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir pywhatkit schedule pyautogui

ENV DISPLAY=:0

CMD ["python", "app.py"]
