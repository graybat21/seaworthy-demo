import os
import re

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with open(os.path.join(HERE, *parts)) as f:
        return f.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string")


setup(
    name="seaworthy",
    version=find_version("chips", "__init__.py"),
    license="MIT",
    url="https://github.com/JayH5/seaworthy-demo",
    description="Show off Seaworthy for my blog",
    author="Jamie Hewland",
    author_email="jamie@praekelt.org",
    long_description=read("README.rst"),
    packages=find_packages(),
    install_requires=[
        "django >= 1.11, < 2.0",
        "django-environ",
    ],
)
