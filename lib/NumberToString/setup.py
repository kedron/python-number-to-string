# NumberToString/setup.py
# TODO: automatically generate this from a template at build time
import os
from setuptools import setup

setup(
    name = "NumberToString",
    version = "0.0.1",
    author = "Kedron Touvell",
    author_email = "kedron@gmail.com",
    url = "https://github.com/kedron/python-number-to-string",
    description = ("Convert a number to a localized string representation of that number."),
    license = "BSD",
    packages=['NumberToString', 'NumberToString/tests'],
    package_data = {
        'NumberToString' : ['share/*/LC_MESSAGES/*.mo'],  # Compiled message catalogs
        'NumberToString/tests' : ['*.testcases'],  # Compiled message catalogs
    },
    exclude_package_data = {
        '' : ['*.po', '*.pot'], # Non-compiled message catalogs
    },
)
