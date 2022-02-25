import django
import os
import rumps
import socketserver
import threading
import traceback
import webbrowser

from django.core.servers import basehttp

url = None


class App(rumps.App):
    @rumps.clicked('Journal')
    def journal(self, _):
        webbrowser.open(url)


class WSGIServer(socketserver.ThreadingMixIn, basehttp.WSGIServer):
    pass


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal.settings')
    django.setup()

    address = ('127.0.0.1', 0)
    app = basehttp.get_internal_wsgi_application()
    httpd = WSGIServer(address, basehttp.WSGIRequestHandler)
    httpd.set_app(app)
    # httpd.daemon_threads = True
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()

    host, port = httpd.socket.getsockname()
    url = f'http://{host}:{port}/'

    app = App('J')
    try:
        app.run()
    except BaseException as exc:
        traceback.print_exc()
    httpd.shutdown()
    thread.join()
