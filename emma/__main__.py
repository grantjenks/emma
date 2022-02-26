import django
import os
import rumps
import socketserver
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


if __name__ == '__main__':
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
