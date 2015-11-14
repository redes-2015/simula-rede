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

        # Addresses
        self.ipAddr = self.routerAddr = self.dnsAddr = None

        # Application running on host and link to a router
        self.application = None
        self.link = None

        # Simulator and network itself queues
        self.simQueue = queue.LifoQueue()
        self.netQueue = queue.LifoQueue()

    def setIp(self, ipAddr, routerAddr, dnsAddr):
        """Defines IP numbers for host, its router and DNS server."""
        self.ipAddr = ipAddr
        self.routerAddr = routerAddr
        self.dnsAddr = dnsAddr

    def addApplication(self, appName, appType):
        """Creates an application 'appName' of the specified type."""
        if appType == 'ircc':
            self.application = IrcClient()
        elif appType == 'ircs':
            self.application = IrcServer()
        elif appType == 'dnss':
            pass
            # TODO: self.application = DnsServer()

    def getSimQueue(self):
        """Returns the host's simulator queue."""
        return self.simQueue

    def addSimQueue(self, msg):
        """Adds a message to the host's simulator queue."""
        self.simQueue.put(msg)

    def addLink(self, link):
        """Links the host to a router's buffer queue."""
        self.link = link

    def process(self, packet):
        """Processes a packet received from the network."""
        print("DEBUG: Processing ", packet)

    def runThread(self):
        """Host's infinite thread loop. Receives and sends messages
           to other hosts."""
        while(True):
            packet = self.simQueue.get()
            self.process(packet)
            self.simQueue.task_done()
