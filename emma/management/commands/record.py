import pathlib
import subprocess
import tempfile
import time

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Screenshot

RUNNING = True


class Command(BaseCommand):
    help = 'Record screenshots'

    def handle(self, *args, **options):
        with open('/Users/grantjenks/log.txt', 'a') as writer:
            wait = 0.5
            last = time.monotonic() - wait
            while RUNNING:
                now = time.monotonic()
                if now - last >= wait:
                    last += wait
                    with tempfile.TemporaryDirectory() as tempdir:
                        screens = [f'{tempdir}/{num}.png' for num in range(10)]
                        when = timezone.now()
                        proc = subprocess.run(['screencapture', '-x', *screens])
                        image_paths = pathlib.Path(tempdir).glob('*.png')
                        for image_path in image_paths:
                            num = int(str(image_path)[-5:-4])
                            with image_path.open('rb') as image:
                                name = f'{when.isoformat()}-{num}.png'
                                image_file = File(image, name=name)
                                screenshot = Screenshot(
                                    num=num,
                                    time=when,
                                    image=image_file,
                                )
                                writer.write('18\n'); writer.flush()
                                screenshot.save()
                                writer.write('19\n'); writer.flush()
                            image_path.unlink()
                time.sleep(0.01)
