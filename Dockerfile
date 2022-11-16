FROM python:3.9.0
ENV PYTHONUNBUFFERED 1
WORKDIR /var/www/html/
COPY . .
RUN pip install -r requirements.txt
#EXPOSE 8000
#CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]