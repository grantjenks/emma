"""Make a video from screenshots

Convert mkv video to mp4 for Mac:

$ ffmpeg -i input.mkv -vcodec libx264 -pix_fmt yuv420p output.mp4

Slow down mkv video so that it plays more slowly:

$ ffmpeg -i input.mkv -filter:v "setpts=2.0*PTS" output.mkv

"""

import datetime as dt
import hashlib
import os
import pathlib
import shutil
import subprocess
import tqdm
import pytz

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Screenshot


class Command(BaseCommand):
    help = 'Make video'

    def add_arguments(self, parser):
        parser.add_argument('--start')
        parser.add_argument('--stop')
        parser.add_argument('--date')
        parser.add_argument('--display', type=int)
        parser.add_argument('output', type=pathlib.Path)

    def handle(self, *args, **options):
        display = options['display'] or 0
        output = options['output']
        if output.exists():
            output.unlink()
        screenshots = Screenshot.objects.order_by('time')
        screenshots = screenshots.filter(display=display)
        pacific = pytz.timezone('US/Pacific')
        if options['date'] is not None:
            date = options['date']
            assert options['start'] is None and options['stop'] is None
            options['start'] = f'{date}T00:00:00'
            options['stop'] = f'{date}T23:59:59'
        if options['start'] is not None:
            start = dt.datetime.strptime(options['start'], '%Y-%m-%dT%H:%M:%S')
            start = pacific.localize(start)
            screenshots = screenshots.filter(time__gte=start)
        if options['stop'] is not None:
            stop = dt.datetime.strptime(options['stop'], '%Y-%m-%dT%H:%M:%S')
            stop = pacific.localize(stop)
            screenshots = screenshots.filter(time__lte=stop)
        screenshots = list(screenshots)
        args = ['ffmpeg', '-loglevel', 'warning', '-f', 'image2pipe', '-i', '-', output]
        proc = subprocess.Popen(args, stdin=subprocess.PIPE)
        last = None
        for screenshot in tqdm.tqdm(screenshots):
            with screenshot.image.open('rb') as reader:
                data = reader.read()
            hasher = hashlib.sha256(data)
            digest = hasher.digest()
            if digest == last:
                continue
            proc.stdin.write(data)
            last = digest
        proc.stdin.close()
        proc.wait()
