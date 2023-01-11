FROM python:3.7-slim
# Use the python latest image
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN echo > admin_public_url.txt

# Install the required packages of the application
RUN pip install --no-cache-dir -r requirements.txt

# Bind the port and refer to the app.py app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server:app