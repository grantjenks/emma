"""Utilities for Emma
"""

import django
import os

from django.core.management import call_command
from pynput import keyboard


def call(command):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emma.settings')
    django.setup()
    call_command(*command)
