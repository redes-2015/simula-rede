"""Represents a computer (host) on the network simulation."""

import queue
import random

from dnsServer import DnsServer
from ircClient import IrcClient
from ircServer import IrcServer
from tcpSegment import TcpSegment
from udpSegment import UdpSegment
from ipDatagram import IpDatagram

# -------------------------------------------------------------


class Host:

    def __init__(self, name):
        """Initializes a computer with the given hostname."""
        self.name = name
        self.idCounter = 1

        # Addresses
        self.ipAddr = self.routerAddr = self.dnsAddr = None

        # Application running on host and link to a router
        self.application = None
        self.link = None

        # Network queue that receives commands from linked entities
        self.simQueue = queue.Queue()
        self.netQueue = queue.Queue()

        # Default port for DNS and IRC servers
        self.dnsPort = 53
        self.ircPort = 6667

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
            # Connect to DNS server to ask for IP
            command[1] = self.__dnsConnect(name)
        if command[0] == "CONNECT":
            self.__tcpEstablishConnection(command[1])

        packet = self.application.send(command)
        packet.setId(self.__nextPacketId())
        self.link.putTargetQueue(packet)

        # IRC Client must wait for ACK packet
        packet = self.netQueue.get()
        if packet.getSegment().getMessage() != "":
            raise Exception("Must get an ACK packet!")
        self.netQueue.task_done()

    def processPacket(self, packet):
        """Processes a packet received from the network."""
        respPacket = self.application.receive(packet)
        if type(respPacket) is list:
            for p in respPacket:
                p.setId(self.__nextPacketId())
                self.link.putTargetQueue(p)
                if p.getSegment().getFIN() is True:
                    self.__tcpCloseConnection(p)
        elif respPacket is not None:
            respPacket.setId(self.__nextPacketId())
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

    def __nextPacketId(self):
        """Returns a unique ID to be given to a packet."""
        packetId = self.name + " #" + str(self.idCounter)
        self.idCounter += 1
        return packetId

    def __tcpEstablishConnection(self, serverIp):
        """Establishes a TCP connection by doing a handshake with
           the server."""
        clientPort = random.randint(1025, 65530)

        # Sends a SYN message to establish connection
        segment = TcpSegment("", clientPort, self.ircPort)
        segment.setSYN()
        datagram = IpDatagram(segment, self.ipAddr, serverIp)
        datagram.setId(self.__nextPacketId())
        self.link.putTargetQueue(datagram)
        packet = self.netQueue.get()

        # Receives packet containing server's SYN
        segment = TcpSegment("", clientPort, self.ircPort)
        segment.setAckNumber(packet.getSegment().getAckNumber())
        segment.setACK()
        segment.setSeqNumber(1)
        segment.setSeqNumber(1)
        datagram = IpDatagram(segment, self.ipAddr, packet.getOriginIp())
        self.netQueue.task_done()
        datagram.setId(self.__nextPacketId())
        self.link.putTargetQueue(datagram)

        # Defines the randomized client port number
        self.application.setClientPort(clientPort)

    def __tcpCloseConnection(self, finalPacket):
        """Close TCP connection by doing a handshake with
           the server."""
        serverIp = finalPacket.getDestinationIp()
        clientPort = finalPacket.getSegment().getOriginPort()

        # Sends a FIN/ACK message to close connection
        packet = self.netQueue.get()

        # Receives packet containing server's SYN
        segment = TcpSegment("", clientPort, self.ircPort)
        segment.setAckNumber(packet.getSegment().getAckNumber())
        segment.setACK()
        segment.setSeqNumber(packet.getSegment().getAckNumber())
        segment.setAckNumber(packet.getSegment().getSeqNumber() + 1)

        datagram = IpDatagram(segment, self.ipAddr, packet.getOriginIp())
        self.netQueue.task_done()

        datagram.setId(self.__nextPacketId())
        self.link.putTargetQueue(datagram)

    def __dnsConnect(self, name):
        """Connects to the DNS server to obtain the given name's
           corresponding IP."""
        segment = UdpSegment(name, 2000, self.dnsPort)
        datagram = IpDatagram(segment, self.ipAddr, self.dnsAddr)
        datagram.setId(self.__nextPacketId())
        self.link.putTargetQueue(datagram)
        packet = self.netQueue.get()

        ip = packet.getSegment().getMessage().split(',')[1]
        self.netQueue.task_done()
        return ip
