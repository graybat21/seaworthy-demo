import time

import pytest
from seaworthy.definitions import ContainerDefinition, VolumeDefinition
from seaworthy.containers.postgresql import PostgreSQLContainer
from seaworthy.logs import output_lines

DJANGO_IMAGE = pytest.config.getoption("--django-image")
NGINX_IMAGE = pytest.config.getoption("--nginx-image")


class DjangoContainer(ContainerDefinition):
    WAIT_PATTERNS = (r"Booting worker",)

    def __init__(self, name, socket_volume, static_volume, db_url,
                 image=DJANGO_IMAGE):
        super().__init__(name, image, self.WAIT_PATTERNS)
        self.socket_volume = socket_volume
        self.static_volume = static_volume
        self.db_url = db_url

    def base_kwargs(self):
        return {
            "volumes": {
                self.socket_volume.inner(): "/var/run/gunicorn",
                self.static_volume.inner(): "/app/static:ro",
            },
            "environment": {
                "DATABASE_URL": self.db_url,
                "ALLOWED_HOSTS": "0.0.0.0",
            },
        }

    def exec_django_admin(self, *args):
        return output_lines(self.inner().exec_run(["django-admin"] + args))


class NginxContainer(ContainerDefinition):
    def __init__(self, name, gunicorn_volume, static_volume,
                 image=NGINX_IMAGE):
        super().__init__(name, image)
        self.gunicorn_volume = gunicorn_volume
        self.static_volume = static_volume

    def base_kwargs(self):
        return {
            "volumes": {
                self.gunicorn_volume.inner(): "/var/run/gunicorn",
                self.static_volume.inner(): "/usr/share/nginx/static:ro",
            },
            "ports": {"80/tcp": None},
        }

    def wait_for_start(self):
        """
        Override wait_for_start for a specialised readiness check.
        """
        deadline = time.monotonic() + self.wait_timeout
        with self.http_client() as client:
            while True:
                timeout = max(deadline - time.monotonic(), 0.001)
                try:
                    client.get('/', timeout=timeout)
                    break
                except Exception:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Timed out waiting for a response.")
                    time.sleep(0.1)


socket_volume = VolumeDefinition("socket")
socket_volume_fixture = socket_volume.pytest_fixture("socket_volume")
static_volume = VolumeDefinition("static")
static_volume_fixture = static_volume.pytest_fixture("static_volume")


postgresql_container = PostgreSQLContainer("postgresql")
postgresql_fixture, clean_postgresql_fixture = (
    postgresql_container.pytest_clean_fixtures("postgresql_container"))

django_container = DjangoContainer("django", socket_volume, static_volume,
                                   postgresql_container.database_url())
django_fixture = django_container.pytest_fixture(
    "django_container",
    dependencies=["socket_volume", "static_volume", "postgresql_container"])

nginx_container = NginxContainer("nginx", socket_volume, static_volume)
nginx_fixture = nginx_container.pytest_fixture(
    "nginx_container",
    dependencies=["socket_volume", "static_volume", "django_container"])

# Allow all the fixtures to be imported like `from fixtures import *`
__all__ = [
    "clean_postgresql_fixture",
    "django_fixture",
    "nginx_fixture",
    "postgresql_fixture",
    "socket_volume_fixture",
    "static_volume_fixture",
]
