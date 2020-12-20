FROM python:3.7

# Create a working directory.
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./ /app
# Finally, run gunicorn.
CMD [ "gunicorn", "--workers=5", "--threads=1", "app:server"]