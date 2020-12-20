# DashPortfolio
Dash application mean to be used as a laboratory for various projects of machine learning/deep learning.

## Heroku configuration

Heroku dynos assign a port randomly, for this reason it is necessary __not to specify any port mapping in the dockerfile__ in the command that runs the concurrent server with gunicorn.

```dockerfile
FROM python:3.7

# Create a working directory.
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./ /app
# Finally, run gunicorn.
CMD [ "gunicorn", "--workers=5", "--threads=1", "app:server"]
 ```
