"""Represents a computer (host) on the network simulation."""

import time
from queue import Queue, Empty, Full

from ircClient import IrcClient
from ircServer import IrcServer
from ipDatagram import IPDatagram
from tcpSegment import TCPSegment

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

        # Network queue that receives commands from linked entities
        self.simQueue = Queue()
        self.netQueue = Queue()

        # DNS table storing the corresponding IP for each host
        self.dnsTable = None

        # Usable ports in the host
        self.portCounter = 1025

        # 'IP:Port -> Username' for IRC server
        self.ircs_connections = {}

    def setIp(self, ipAddr, routerAddr, dnsAddr):
        """Defines IP numbers for host, its router and DNS server."""
        self.ipAddr = ipAddr
        self.routerAddr = routerAddr
        self.dnsAddr = dnsAddr

    def addApplication(self, appName, appType):
        """Creates an application 'appName' of the specified type."""
        if appType == 'ircc':
            self.application = IrcClient(self.ipAddr)
            # Only the IRC client can be controlled
            # directly by simulation commands
        elif appType == 'ircs':
            self.application = IrcServer(self.ipAddr)
            self.simQueue = None
        elif appType == 'dnss':
            # TODO: self.application = DnsServer()
            self.simQueue = None
           
        # print(self.name, self.dnsTable)

    def getNetQueue(self):
        """Returns the host's network queue."""
        return self.netQueue

    def addSimQueue(self, msg):
        """Adds a message to the host's simulator queue."""
        self.simQueue.put(msg)

    def addLink(self, link):
        """Links the host to a router's buffer queue."""
        self.link = link

    def setSniffer(self, sniffer):
        """Sets a sniffer between the host and the router
           which it is linked to."""
        self.link.setSniffer(sniffer)

    def processCommand(self, command):
        """Processes a command received from the simulation."""
        # print(self.name + ": Processing command", command)
        packet = self.application.send(command)
        # packet()
        self.link.putTargetQueue(packet)
        # print("Packet sent to router!")

    def processPacket(self, packet):
        """Processes a packet received from the network."""
        respPacket = self.application.receive(packet)
        # print(self.name + " received a packet!")
        # packet()
        if respPacket is not None:
            # respPacket()
            self.link.putTargetQueue(respPacket)
            # print("DEBUG:", self.name, "received packet from", packet.getOriginIP())

    def runThread(self):
        """Host's infinite thread loop. Receives and sends messages
           to other hosts."""
        while(True):
            try:
                command = self.simQueue.get()
                self.processCommand(command)
                self.simQueue.task_done()
            except AttributeError:
                pass

            packet = self.netQueue.get()
            self.processPacket(packet)
            self.netQueue.task_done()

    def getAddressInfo(self, name):
        """???"""
        packet = IPDatagram(self.ipAddr, self.dnsAddr, UDPSegment(name, self.portCounter, 53))
        self.portCounter += 1
        if self.portCounter >= 60000:
            self.portCounter = 1025
        return packet
