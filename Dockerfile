FROM python:3.7

# Create a working directory.
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./ /app
EXPOSE 8000

# Finally, run gunicorn.
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8000", "app:server"]