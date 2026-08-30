FROM python:3.12-slim # Скачиваю нужный образ python

WORKDIR /app # устанавливаю рабочую директорию внутри контейнера

COPY requirements.txt . # копирую файл с зависимостями

RUN pip install --no-cache-dir -r requirements.txt # Устанавливаю зависимости

COPY . . # копирую код всего приложения

EXPOSE 8000 # указываю порт на котором слушаем приложение

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","8000"] # команды для запуска