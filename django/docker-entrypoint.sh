#!/usr/bin/env sh
set -e

# Simplified Gunicorn entrypoint script. For a more complete example, see
# https://github.com/praekeltfoundation/docker-django-bootstrap

# No args or looks like options or the APP_MODULE for Gunicorn
if [ "$#" = 0 ] || \
		[ "${1#-}" != "$1" ] || \
		echo "$1" | grep -Eq '^([_A-Za-z]\w*\.)*[_A-Za-z]\w*:[_A-Za-z]\w*$'; then
	set -- gunicorn "$@"
fi

if [ "$1" = 'gunicorn' ]; then
	django-admin migrate --noinput

	# Set some sensible Gunicorn options, needed for things to work with Nginx
	set -- "$@" \
		--bind unix:/var/run/gunicorn/gunicorn.sock
fi

exec "$@"
