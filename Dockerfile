# Использовать официальный образ родительского образа / слепка.
FROM python:3.9

# Установка рабочей директории, откуда выполняются команды внутриконтейнера.
WORKDIR /blackjack_django

# Скопировать все файлы с локальной машины внутрь файловой системывиртуального образа.
COPY . .

# Запустить команду внутри образа, установка зависимостей.
RUN pip install --upgrade pip && pip install -r requirements.txt
#RUN chmod +x entrypoint.sh
RUN chmod +x /blackjack_django/entrypoint.sh

# Добавить мета-информацию к образу для открытия порта к прослушиванию.
#EXPOSE 8000 80 81

# Выполнить команду внутри контейнера
#CMD ["python", "./manage.py",  "runserver", "0.0.0.0:8000"]

ENTRYPOINT ["/blackjack_django/entrypoint.sh"]
