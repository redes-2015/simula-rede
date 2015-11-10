"""Represents a computer (host) on the network simulation."""

import time

# -------------------------------------------------------------


class Host:

    def __init__(self, name):
        """Initializes a computer with the given hostname."""
        self.name = name
        # Initializes empty attributes
        self.ipAddr = self.routerAddr = self.dnsAddr = None
        self.thread = None
        # TODO: Check if application must be inserted in host

    def setIp(self, ipAddr, routerAddr, dnsAddr):
        """Define atributos da configuração de IP do computador."""
        self.ipAddr = ipAddr
        self.routerAddr = routerAddr
        self.dnsAddr = dnsAddr

    def runThread(self):
        """Host's infinite thread loop. Receives and sends messages
           to other hosts."""
        while(True):
            print("Host '%s' running!" % self.name)
            time.sleep(5)
