# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только папку src
COPY . /app/src

# Создаем папку для загрузок (uploads)
RUN mkdir -p /app/src/uploads

# Указываем порт, который будет использовать приложение
EXPOSE 80

# Команда для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]