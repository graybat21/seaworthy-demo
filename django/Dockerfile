FROM python:3.6-slim-jessie

# Install production things:
# - Gunicorn as the WSGI server
# - psycopg2 to be able to connect to PostgreSQL
RUN pip install --no-cache gunicorn psycopg2

# Set up the entrypoint script
COPY docker-entrypoint.sh /entrypoint.sh
RUN mkdir /var/run/gunicorn
ENTRYPOINT ["/entrypoint.sh"]

# Copy in and install the source
WORKDIR /app
COPY . .
RUN pip install --no-cache -e .

# Configure Django and collect static files
ENV DJANGO_SETTINGS_MODULE chips.settings
RUN django-admin collectstatic --noinput

# Provide an argument to Gunicorn (the WSGI app module)
CMD ["chips.wsgi:application"]
