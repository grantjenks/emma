import re
import setuptools

with open('journal/__init__.py') as init:
    text = init.read()
    match = re.search(r"__version__ = '(.+)'", text)
    version = match.group(1)

setuptools.setup(
    name='journal',
    version=version,
    packages=['journal'],
    install_requires=[
        'appdirs',
        'django==3.2.*',
        'gunicorn',
        'rumps',
    ],
)
