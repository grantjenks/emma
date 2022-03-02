"""Clear screeshots

"""

import datetime as dt
import pytz

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

from ...models import Screenshot


class Command(BaseCommand):
    help = 'Clear screenshots'

    def handle(self, *args, **options):
        pacific = pytz.timezone('US/Pacific')
        now_utc = dt.datetime.utcnow().replace(tzinfo=pytz.utc)
        now = now_utc.astimezone(pacific)
        yesterday = now - dt.timedelta(days=1)
        yester_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        yester_end = yester_start + dt.timedelta(days=1) - dt.timedelta(microseconds=1)
        screenshots = list(
            Screenshot.objects.all()
            .filter(time__gte=yester_start)
            .filter(time__lte=yester_end)
        )
        iterator = tqdm(screenshots, desc='Deleting Screenshots')
        for screenshot in iterator:
            screenshot.delete()
        contents_iterator = settings.MEDIA_ROOT.glob('contents/**/*.png')
        iterator = tqdm(contents_iterator, desc='Crawling Contents')
        contents_paths = list(iterator)
        references = dict.fromkeys(contents_paths, 0)
        screenshots_iterator = settings.MEDIA_ROOT.glob('screenshots/**/*.png')
        iterator = tqdm(screenshots_iterator, desc='Crawling Symlinks')
        screenshots_paths = list(iterator)
        iterator = tqdm(screenshots_paths, desc='Resolving Symlinks')
        for screenshot_path in iterator:
            target_path = screenshot_path.resolve()
            if target_path in references:
                references[target_path] += 1
        for contents_path, count in references.items():
            if count > 0:
                continue
            # TODO
