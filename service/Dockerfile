# FROM python:3
FROM 9f4d442f66f7
ENV PYTHONBUFFERED 1
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
# CMD ["python", "manage.py", "runserver"]