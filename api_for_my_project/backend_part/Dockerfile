# Скачиваю нужный образ python
FROM python:3.12-slim
# устанавливаю рабочую директорию внутри контейнера
WORKDIR /app
# копирую файл с зависимостями
COPY requirements.txt .
# Устанавливаю зависимости
RUN pip install --no-cache-dir -r requirements.txt
# копирую код всего приложения
COPY . .
# указываю порт на котором слушаем приложение
EXPOSE 8000
 # команды для запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","8000"]