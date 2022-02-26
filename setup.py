import re
import setuptools

with open('emma/__init__.py') as init:
    text = init.read()
    match = re.search(r"__version__ = '(.+)'", text)
    version = match.group(1)

setuptools.setup(
    name='emma',
    version=version,
    packages=['emma'],
    install_requires=[
        'appdirs',
        'django==3.2.*',
        'gunicorn',
        'rumps',
    ],
)
