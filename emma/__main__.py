import argparse
import contextlib
import django
import getpass
import os
import pathlib
import rumps
import socketserver
import subprocess
import threading
import traceback
import webbrowser

from django.core.servers import basehttp
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management import call_command

url = None


class App(rumps.App):
    @rumps.clicked('Emma')
    def emma(self, _):
        webbrowser.open(url)


class WSGIServer(socketserver.ThreadingMixIn, basehttp.WSGIServer):
    pass


@contextlib.contextmanager
def run_server():
    global url
    address = ('127.0.0.1', 0)
    app = basehttp.get_internal_wsgi_application()
    httpd = WSGIServer(address, basehttp.WSGIRequestHandler)
    httpd.set_app(StaticFilesHandler(app))
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()
    host, port = httpd.socket.getsockname()
    url = f'http://{host}:{port}/'
    yield
    httpd.shutdown()
    server_thread.join()


@contextlib.contextmanager
def run_recorder():
    from emma.management.commands import record
    recorder_thread = threading.Thread(target=call_command, args=('record',))
    recorder_thread.start()
    yield
    record.RUNNING = False
    recorder_thread.join()


def run():
    with run_server(), run_recorder():
        app = App('E')
        try:
            app.run()
        except BaseException:
            traceback.print_exc()


def load():
    plist_path = pathlib.Path(__file__).parent / 'emma.daemon.plist'
    with plist_path.open() as reader:
        template = reader.read()
    launch_path = pathlib.Path('~/Library/LaunchAgents/emma.daemon.plist')
    launch_path = launch_path.expanduser()
    with launch_path.open('w') as writer:
        text = template.format(user=getpass.getuser())
        writer.write(text)
    subprocess.run(['launchctl', 'load', str(launch_path)])


def unload():
    launch_path = pathlib.Path('~/Library/LaunchAgents/emma.daemon.plist')
    launch_path = launch_path.expanduser()
    subprocess.run(['launchctl', 'unload', str(launch_path)])
    with contextlib.suppress(FileNotFoundError):
        launch_path.unlink()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command',
        nargs='?',
        choices=['', 'load', 'unload', 'reload'],
    )
    args = parser.parse_args()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emma.settings')
    django.setup()

    call_command('migrate', '--verbosity', '0')

    if args.command is None:
        run()
    elif args.command == 'load':
        load()
    elif args.command == 'unload':
        unload()
    elif args.command == 'reload':
        unload()
        load()


if __name__ == '__main__':
    main()
