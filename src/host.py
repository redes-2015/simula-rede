"""Represents a computer (host) on the network simulation."""

import time
import queue
from ircClient import IrcClient
from ircServer import IrcServer

# -------------------------------------------------------------


class Host:

    def __init__(self, name):
        """Initializes a computer with the given hostname."""
        self.name = name
        # Initializes empty attributes
        self.ipAddr = self.routerAddr = self.dnsAddr = None
        self.thread = None
        self.apps = {}
        self.simQueue = queue.LifoQueue()
        self.netQueue = queue.LifoQueue()
        # TODO: Check if application must be inserted in host

    def setIp(self, ipAddr, routerAddr, dnsAddr):
        """Define atributos da configuração de IP do computador."""
        self.ipAddr = ipAddr
        self.routerAddr = routerAddr
        self.dnsAddr = dnsAddr

    def addApp(self, appName, appType):
        if appType == 'ircc':
            self.apps[appName] = IrcClient()
        elif appType == 'ircs':
            self.apps[appName] = IrcServer()
        elif appType == 'dnss':
            pass
            #self.apps[appName] = DnsServer()

    def addSimQueue(self, msg):
        self.simQueue.put(msg)

    def proc(self, item):
        print("DEBUG: comando na thread", item)

    def runThread(self):
        """Host's infinite thread loop. Receives and sends messages
           to other hosts."""
        #print("Host '%s' started!" % self.name)
        while(True):
            item = self.simQueue.get()
            self.proc(item)
            self.simQueue.task_done()

