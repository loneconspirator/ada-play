#!/usr/bin/python
import threading
import cherrypy

#cherrypy.config.update({'server.socket_port': 80})

class HelloWorld(object):
    def __init__(self, queue):
        self.queue = queue

    def index(self):
        return open("web/index.html")
    index.exposed = True

class Server(threading.Thread):
    def __init__(self, logger, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.logger = logger
        self.logger.debug("HTTP Server Created")

    def run(self):
        try:
            cherrypy.quickstart(HelloWorld(self.queue))
        except Exception as e:
            self.logger.exception("Exception in server: " + str(e))
