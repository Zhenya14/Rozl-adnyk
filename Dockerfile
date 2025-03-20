# Використовуємо офіційний образ Python 3.9
FROM python:3.9-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли `requirements.txt` і бота в контейнер
COPY requirements.txt ./
COPY Rozkladnykbot.py ./

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Визначаємо змінну середовища для токену бота
# Це можна зробити через налаштування в Koyeb або Docker
ENV BOT_TOKEN=your-telegram-bot-token-here

# Команда для запуску бота
CMD ["python", "Rozkladnykbot.py"]
