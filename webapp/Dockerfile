FROM python:latest

RUN pip install Flask

ADD app.py /app/app.py
ADD startup /startup

EXPOSE 8000

CMD ["/startup"]
