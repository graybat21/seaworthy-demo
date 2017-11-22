import os


def pytest_addoption(parser):
    parser.addoption(
        "--django-image", action="store",
        default=os.environ.get("DJANGO_IMAGE", "seaworthy-demo:django"),
        help="Django Docker image to test")
    parser.addoption(
        "--nginx-image", action="store",
        default=os.environ.get("NGINX_IMAGE", "seaworthy-demo:nginx"),
        help="Nginx Docker image to test")


def pytest_report_header(config):
    return "\n".join((
        "Django Docker image: {}".format(config.getoption("--django-image")),
        "Nginx Docker image: {}".format(config.getoption("--nginx-image")),
    ))
