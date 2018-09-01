import cgi
import time

import pytest
from seaworthy.logs import output_lines

from fixtures import *  # noqa: F401,F403


def mime_type(content_type):
    return cgi.parse_header(content_type)[0]


# class TestDjangoContainer:
#     @pytest.mark.clean_postgresql_container
#     def test_db_tables_created(self, django_container, postgresql_container):
#         """
#         When the Django container starts, it runs its migrations and some
#         database tables are created in PostgreSQL.
#         """
#         django_logs = django_container.get_logs().decode("utf-8")
#         assert "Running migrations" in django_logs

#         psql_output = postgresql_container.exec_psql(
#             ("SELECT COUNT(*) FROM information_schema.tables WHERE "
#              "table_schema='public';"))

#         count = int(psql_output)
#         assert count > 0


class TestNginxContainer:
    def test_admin_page(self, nginx_container):
        """
        When we try to access a page served by Django, for example, the Django
        admin page, that page is returned via Nginx.
        """
        client = nginx_container.http_client()
        response = client.get("/admin")

        assert response.status_code == 200
        assert mime_type(response.headers["content-type"]) == "text/html"
        assert "<title>Log in | Django site admin</title>" in response.text

    def test_static_file(self, nginx_container):
        """
        When we try to access a file served directly by Nginx, for example, a
        static file, that file is returned by Nginx.
        """
        client = nginx_container.http_client()
        response = client.get("/static/icecream/images/background.gif")

        assert response.status_code == 200
        assert mime_type(response.headers["content-type"]) == "image/gif"

    def test_access_logs(self, nginx_container):
        """
        When we make a request against Nginx, the request is logged to the
        access log which is output to stdout.
        """
        old_logs = output_lines(nginx_container.get_logs(stderr=False))

        client = nginx_container.http_client()
        response = client.get("/static/icecream/images/background.gif")

        # Wait a moment for the access log to be recoreded
        time.sleep(0.1)
        logs = output_lines(nginx_container.get_logs(stderr=False))
        new_logs = logs[len(old_logs):]

        [log_line] = new_logs
        assert (
            "GET /static/icecream/images/background.gif HTTP/1.1" in log_line)
        assert str(response.status_code) in log_line
