from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_main import app

httpserver = HTTPServer(WSGIContainer(app))
httpserver.listen(5000)
IOLoop.instance().start()