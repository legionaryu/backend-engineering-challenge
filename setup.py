import os
from setuptools import setup


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="unbabel",
    version="1.0.0",
    author="Vitaliano Palmieri Neto",
    author_email="vitaliano.neto@gmail.com",
    description=(
        "This module helps you to parse the log files from Unbabel translation requests"
    ),
    license="MIT",
    keywords="unbabel programming challenge backend",
    url="https://github.com/legionaryu/backend-engineering-challenge",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["unbabel_cli"],
)
