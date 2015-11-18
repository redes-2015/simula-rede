from threading import Thread
from queue import LifoQueue, Empty, Full

class Application(object):

    def __init__(self, name, host):
        self.name = name
        self.host = host

    def addSimQueue(self, msg):
        """Adds a message to the host's simulator queue."""
        self.host.simQueue.put(msg)

    def getHost(self):
        return self.host
