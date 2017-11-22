# seaworthy-demo

[![Docker Pulls](https://img.shields.io/docker/pulls/jamiehewland/seaworthy-demo.svg)](https://hub.docker.com/r/jamiehewland/seaworthy-demo/)
[![Build Status](https://travis-ci.org/JayH5/seaworthy-demo.svg?branch=master)](https://travis-ci.org/JayH5/seaworthy-demo)

A demo of [Seaworthy](https://github.com/praekeltfoundation/seaworthy) for my
Docker/Travis blog part 3

This repository is split into three directories:
 1. [`django`](django): All the Django project code and its Dockerfile
 2. [`nginx`](nginx): The Nginx configuration and Dockerfile
 3. [`seaworthy`](seaworthy): The Seaworthy test code

## Architecture
![Basic Django deployment architecture](architecture.png)

The Nginx container (1) receives incoming HTTP requests and proxies them to the
web application container (2). The web application container in the centre
contains the actual application: Django served using
[Gunicorn](http://gunicorn.org). This Django application needs a database to
store its data in, and that’s where the final part comes in — the PostgreSQL
database container (3).

The two volumes are Docker volumes that are shared between the Nginx and web
application containers. The “socket volume” contains Gunicorn’s Unix socket.
Nginx initiates HTTP requests to Gunicorn & Django via this socket. The second
volume is used to share
[Django’s static files](https://docs.djangoproject.com/en/1.11/howto/static-files/)
with Nginx, which Nginx can serve to users efficiently.
