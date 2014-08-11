# NumberToString/setup.py
# TODO: automatically generate this from a template at build time
import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "NumberToString",
    version = "0.0.1",
    author = "Kedron Touvell",
    author_email = "kedron@gmail.com",
    url = "https://github.com/kedron/python-number-to-string",
    description = ("Convert a number to a localized string representation of that number."),
    long_description=read('README.md'),
    license = "BSD",
    packages=['NumberToString'],
    package_data = {
        'NumberToString' : ['share/*/LC_MESSAGES/*.mo'],  # Compiled message catalogs
    },
    exclude_package_data = {
        '' : ['*.po', '*.pot'], # Non-compiled message catalogs
    },
)
