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

#Копирую entrypoint и делаю файл исполнянемым
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# указываю порт на котором слушаем приложение
EXPOSE 8000
 # команда для запуска
ENTRYPOINT ["/entrypoint.sh"]