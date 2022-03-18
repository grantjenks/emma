import pathlib
import subprocess
import tempfile
import time

from ScriptingBridge import SBApplication
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Screenshot

RUNNING = True


class Command(BaseCommand):
    help = 'Snoop on other programs using Apple scripting'

    def handle(self, *args, **options):
        chrome = SBApplication.applicationWithBundleIdentifier_('com.google.Chrome')
        while True:
            if chrome.frontmost():
                for window in chrome.windows().get():
                    tab = window.activeTab()
                    title = tab.title()
                    url = tab.URL()
                    print(title, url)
                    break
            else:
                print('no focus')
            time.sleep(0.5)

    def window_title(self):
        from AppKit import NSWorkspace
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID,
        )

        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        bundle_identifier = app.bundleIdentifier()
        pid = app.processIdentifier()
        options = kCGWindowListOptionOnScreenOnly
        window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)

        for window in window_list:
            window_pid = window['kCGWindowOwnerPID']
            window_title = window.get('kCGWindowName', u'Unknown')
            if pid == window_pid:
                print(bundle_identifier, window_title)
