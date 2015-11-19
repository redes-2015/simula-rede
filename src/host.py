"""Represents a computer (host) on the network simulation."""

import time
from queue import LifoQueue, Empty, Full

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

        # Simulator and network itself queues
        self.simQueue = LifoQueue()
        self.netQueue = LifoQueue()

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
        elif appType == 'ircs':
            self.application = IrcServer(self.ipAddr)
        elif appType == 'dnss':
            pass
            # TODO: self.application = DnsServer()
        print(self.name, self.dnsTable)

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
        packet = self.application.send(command)
        self.link.putTargetQueue(packet)
        print("DEBUG:", self.name, " Processing command", command)

    def processPacket(self, packet):
        """Processes a packet received from the network."""
        respPacket = self.application.receive(packet)
        if respPacket is not None:
            self.link.putTargetQueue(respPacket)
        print("DEBUG:", self.name, "received packet from", packet.getOriginIP())

    def runThread(self):
        """Host's infinite thread loop. Receives and sends messages
           to other hosts."""
        while(True):
            try:
                command = self.simQueue.get_nowait()
                self.processCommand(command)
                self.simQueue.task_done()
            except Empty:
                pass

            try:
                packet = self.netQueue.get_nowait()
                self.processPacket(packet)
                self.netQueue.task_done()
            except Empty:
                pass

    def getAddressInfo(self, name):
        """???"""
        packet = IPDatagram(self.ipAddr, self.dnsAddr, UDPSegment(name, self.portCounter, 53))
        self.portCounter += 1
        if self.portCounter >= 60000:
            self.portCounter = 1025
        return packet

    def ircc_process(self, msgList):
        """Sends the specified message to an IRC server
           This method supposes that the message is correct!."""
        if msgList[0] == self.CONNECT:
            msg = ' '.join(msgList)
            transport = TCPSegment(msg, self.portCounter, 6667)
            transport.setSYN()
            datagram = IPDatagram(self.ipAddr, msgList[1], transport)
        else:
            pass  # TODO: Send message through socket
        # TODO: Receive response from server

    def ircs_process(self, packet):
        """Parses a message received by a client with the given address
           'addr' (which is a list [IP, Port])."""
        msg = packet.getTransportSegment().getMessage()
        separate = msg.split(' ')

        if separate[0] == CONNECT:
            response = "Connection successful!"
            self.connections[addrStr] = None

        elif separate[0] == USER:
            # Supposes that a client won't try
            # to use an already defined username
            self.connections[addrStr] = username
            response = "Username '" + username + "' successfully defined!"

        elif separate[0] == QUIT:
            # 'None' is the returning value
            # in case 'addrStr' key doesn't exist
            self.connections.pop(addrStr, None)
            response = "You have left the server."

        return response

    def dnss_process(self):
        """???"""
