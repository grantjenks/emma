"""Clear screeshots

"""

import datetime as dt
import pytz

from contextlib import suppress
from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

from ...models import Screenshot


class Command(BaseCommand):
    help = 'Clear screenshots'

    def add_arguments(self, parser):
        parser.add_argument('--start')
        parser.add_argument('--stop')
        parser.add_argument('--date')
        parser.add_argument('--display', type=int)

    def handle(self, *args, **options):
        screenshots = Screenshot.objects.order_by('time')
        if options['display'] is not None:
            screenshots = screenshots.filter(display=display)
        if options['date'] is not None:
            assert options['start'] is None and options['stop'] is None
            date = dt.date.fromisoformat(options['date'])
            tomorrow = date + dt.timedelta(days=1)
            options['start'] = f'{date}T00:00:00'
            options['stop'] = f'{tomorrow}T00:00:00'
        pacific = pytz.timezone('US/Pacific')
        if options['start'] is not None:
            start = dt.datetime.strptime(options['start'], '%Y-%m-%dT%H:%M:%S')
            start = pacific.localize(start)
            screenshots = screenshots.filter(time__gte=start)
        if options['stop'] is not None:
            stop = dt.datetime.strptime(options['stop'], '%Y-%m-%dT%H:%M:%S')
            stop = pacific.localize(stop)
            screenshots = screenshots.filter(time__lte=stop)
        screenshots = list(screenshots.only('id'))
        iterator = tqdm(screenshots, desc='Deleting Screenshots')
        for screenshot in iterator:
            screenshot.image.delete()
            screenshot.delete()
        contents_iterator = settings.MEDIA_ROOT.glob('contents/**/*.png')
        iterator = tqdm(contents_iterator, desc='Crawling Contents')
        contents_paths = list(iterator)
        references = dict.fromkeys(contents_paths, 0)
        screenshots_iterator = settings.MEDIA_ROOT.glob('screenshots/**/*.png')
        iterator = tqdm(screenshots_iterator, desc='Crawling Symlinks')
        screenshots_paths = list(iterator)
        iterator = tqdm(screenshots_paths, desc='Resolving Symlinks')
        missing_target_paths = []
        for screenshot_path in iterator:
            target_path = screenshot_path.resolve()
            try:
                references[target_path] += 1
            except KeyError:
                pair = screenshot_path, target_path
                missing_target_paths.append(pair)
        iterator = tqdm(missing_target_paths, desc='Missing Target Paths')
        media_root_length = len(str(settings.MEDIA_ROOT))
        for screenshot_path, target_path in iterator:
            image_path = str(screenshot_path)[media_root_length + 1:]
            with suppress(Screenshot.DoesNotExist):
                screenshot = Screenshot.objects.get(image=image_path)
                screenshot.delete()
            screenshot_path.unlink()
        iterator = tqdm(references.items(), desc='Removing Contents')
        for contents_path, count in iterator:
            if count > 0:
                continue
            contents_path.unlink()
        dir_iterator = settings.MEDIA_ROOT.glob('**/')
        iterator = tqdm(dir_iterator, desc='Crawling Directories')
        directories = list(iterator)
        directories.reverse()
        directories.pop()
        iterator = tqdm(directories, desc='Removing Empty Directories')
        for directory in iterator:
            with suppress(OSError):
                directory.rmdir()
