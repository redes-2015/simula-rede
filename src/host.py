"""Represents a computer (host) on the network simulation."""

import queue

from dnsServer import DnsServer
from ircClient import IrcClient
from ircServer import IrcServer
from udpSegment import UdpSegment
from ipDatagram import IpDatagram

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
        self.simQueue = queue.Queue()
        self.netQueue = queue.Queue()

        # Default port for DNS server
        self.dnsPort = 53

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
            self.application = DnsServer(self.ipAddr)
            self.simQueue = None

    def setDnsTable(self, dnsTable):
        """Defines the DNS table for a DNS server application."""
        try:
            self.application.setDnsTable(dnsTable)
        except NameError:
            print(self.name, "isn't a DNS server!")

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
        name = self.application.requireDns(command)
        if name is not None:
            segment = UdpSegment(name, 2000, self.dnsPort)
            datagram = IpDatagram(segment, self.ipAddr, self.dnsAddr)
            self.link.putTargetQueue(datagram)
            packet = self.netQueue.get()

            # TODO: Make the below line more comfortable
            command[1] = packet.getSegment().getMessage().split(',')[1]
            self.netQueue.task_done()

        packet = self.application.send(command)
        self.link.putTargetQueue(packet)

    def processPacket(self, packet):
        """Processes a packet received from the network."""
        respPacket = self.application.receive(packet)
        if respPacket is not None:
            self.link.putTargetQueue(respPacket)

    def runThread(self):
        """Host's infinite thread loop. Receives and sends messages
           to other hosts."""
        while True:
            if self.simQueue is not None:
                # Read and process a direct simulator command
                command = self.simQueue.get()
                self.processCommand(command)
                self.simQueue.task_done()

            # Read and process network command
            packet = self.netQueue.get()
            self.processPacket(packet)
            self.netQueue.task_done()
