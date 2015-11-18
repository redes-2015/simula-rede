"""Represents a computer (host) on the network simulation."""

import time
from queue import LifoQueue, Empty, Full

from ipDatagram import IPDatagram
from tcpSegment import TCPSegment

# -------------------------------------------------------------


class Host:

    def __init__(self, name):
        """Initializes a computer with the given hostname."""
        self.name = name

        # Addresses
        self.ipAddr = self.routerAddr = self.dnsAddr = None

        # link to a router
        self.link = None

        # Simulator and network itself queues
        self.simQueue = LifoQueue()
        self.netQueue = LifoQueue()

        # DNS table storing the corresponding IP for each host
        self.dnsTable = None

        # Usable ports in the host
        self.portCounter = 1025

    def setIp(self, ipAddr, routerAddr, dnsAddr):
        """Defines IP numbers for host, its router and DNS server."""
        self.ipAddr = ipAddr
        self.routerAddr = routerAddr
        self.dnsAddr = dnsAddr

    def getNetQueue(self):
        """Returns the host's network queue."""
        return self.netQueue

    def addSimQueue(self, msg):
        """Adds a message to the host's simulator queue."""
        self.simQueue.put(msg)

    def addLink(self, link):
        """Links the host to a router's buffer queue."""
        self.link = link

    def processCommand(self, command):
        """Processes a command received from the simulation."""
        packet = IPDatagram(self.ipAddr, command[1], TCPSegment(command[0], 5000, 6667))

        self.link.putTargetQueue(packet)
        print("DEBUG:", self.name, " Processing command", command)

    def processPacket(self, packet):
        """Processes a packet received from the network."""
        print("DEBUG:", self.name, "received packet from", packet.getOriginIP())
