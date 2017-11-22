FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY django.conf /etc/nginx/conf.d/

VOLUME /usr/share/nginx/static /var/run/gunicorn
