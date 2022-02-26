import argparse
import django
import os
import rumps
import socketserver
import subprocess
import threading
import traceback
import webbrowser

from django.core.servers import basehttp
from django.contrib.staticfiles.handlers import StaticFilesHandler

url = None


class App(rumps.App):
    @rumps.clicked('Emma')
    def emma(self, _):
        webbrowser.open(url)


class WSGIServer(socketserver.ThreadingMixIn, basehttp.WSGIServer):
    pass


def main():
    global url
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emma.settings')
    django.setup()

    address = ('127.0.0.1', 0)
    app = basehttp.get_internal_wsgi_application()
    httpd = WSGIServer(address, basehttp.WSGIRequestHandler)
    httpd.set_app(StaticFilesHandler(app))
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()

    host, port = httpd.socket.getsockname()
    url = f'http://{host}:{port}/'

    app = App('E')
    try:
        app.run()
    except BaseException as exc:
        traceback.print_exc()
    httpd.shutdown()
    thread.join()


def load():
    subprocess.run('ln -s /Users/grantjenks/repos/emma/emma.daemon.plist ~/Library/LaunchAgents/', shell=True)
    subprocess.run('launchctl load ~/Library/LaunchAgents/emma.daemon.plist', shell=True)


def unload():
    subprocess.run('launchctl unload ~/Library/LaunchAgents/emma.daemon.plist', shell=True)
    subprocess.run('rm ~/Library/LaunchAgents/emma.daemon.plist', shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?', choices=['', 'load', 'unload', 'reload'])
    args = parser.parse_args()

    if args.command is None:
        main()
    elif args.command == 'load':
        load()
    elif args.command == 'unload':
        unload()
    elif args.command == 'reload':
        unload()
        load()
