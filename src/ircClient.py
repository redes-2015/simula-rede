"""Represents an IRC client on the network simulation."""

import re

from tcpSegment import TCPSegment
from ipDatagram import IPDatagram

# -------------------------------------------------------------


class IrcClient:

    def __init__(self, clientIP):
        """Initializes client's attributes."""
        self.clientIP = clientIP
        self.clientPort = 1025
        self.ircPort = 6667  # Default port for IRC servers
        self.dnsPort = 53    # Default port for DNS servers
        self.serverIP = None

        # Comandos parseados no cliente
        self.CONNECT = "CONNECT"

    def send(self, msgList):
        """Sends the specified message to an IRC server
           This method supposes that the message is correct!."""
        msg = ' '.join(msgList)
        if msgList[0] == self.CONNECT:
            self.__updateClientPort()
            self.serverIP = msgList[1]
             # TODO: Check TCP handshake

        segment = TCPSegment(msg, self.clientPort, self.ircPort)
        datagram = IPDatagram(self.clientIP, self.serverIP, segment)
        return datagram

    def receive(self, packet):
        """Receives and parses a package from the IRC server."""
        msg = packet.getSegment().getMessage()

        # Received CONNECT confirmation
        if msg[0] == '0':
            self.serverIP = packet.getOriginIP()
        # Received USER confirmation
        elif msg[0] == '1':
            pass
        # Received QUIT confirmation
        elif msg[0] == '2':
            self.serverIP = None

        return None

    def requireDns(self, msgList):
        """Checks if the client command is a CONNECT that requires
           the DNS server."""
        if msgList[0] == self.CONNECT and not \
           re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", msgList[1]):
                return msgList[1]
        return None

    def __updateClientPort(self):
        """Updates used client ports."""
        self.clientPort += 1
        if self.clientPort > 65530:
            self.clientPort = 1025
