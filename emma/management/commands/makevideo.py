import hashlib
import os
import pathlib
import shutil
import subprocess
import tqdm

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Make video'

    def add_arguments(self, parser):
        parser.add_argument('output', type=pathlib.Path)

    def handle(self, *args, **options):
        output = options['output']
        if output.exists():
            output.unlink()
        args = ['ffmpeg', '-loglevel', 'warning', '-f', 'image2pipe', '-i', '-', output]
        proc = subprocess.Popen(args, stdin=subprocess.PIPE)
        screenshots_path = settings.MEDIA_ROOT / 'screenshots'
        png_files = sorted(screenshots_path.glob('**/*-1.png'))
        last = None
        for png_file in tqdm.tqdm(png_files):
            with png_file.open('rb') as reader:
                data = reader.read()
            hasher = hashlib.sha256(data)
            digest = hasher.digest()
            if digest == last:
                continue
            proc.stdin.write(data)
            last = digest
        proc.stdin.close()
        proc.wait()
