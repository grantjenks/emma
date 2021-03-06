import pathlib
import subprocess
import tempfile
import time

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Screenshot


class Command(BaseCommand):
    help = 'Record screenshots'

    def handle(self, *args, **options):
        while True:
            with tempfile.TemporaryDirectory() as tempdir:
                screens = [f'{tempdir}/{num}.png' for num in range(10)]
                when = timezone.now()
                args = ['screencapture', '-Cx', *screens]
                proc = subprocess.run(args)
                image_paths = pathlib.Path(tempdir).glob('*.png')
                for image_path in image_paths:
                    display = int(str(image_path)[-5:-4])
                    with image_path.open('rb') as image:
                        name = f'{when.isoformat()}-{display}.png'
                        image_file = File(image, name=name)
                        screenshot = Screenshot(
                            display=display,
                            time=when,
                            image=image_file,
                        )
                        screenshot.save()
                    image_path.unlink()
            time.sleep(0.5)
