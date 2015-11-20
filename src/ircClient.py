"""Represents an IRC client on the network simulation."""

import random
import re

from tcpSegment import TcpSegment
from ipDatagram import IpDatagram

# -------------------------------------------------------------


class IrcClient:

    def __init__(self, clientIp):
        """Initializes client's attributes."""
        self.clientIp = clientIp
        self.serverIp = None

        self.clientPort = None
        self.serverPort = 6667  # Default port for IRC servers

        # Comandos parseados no cliente
        self.CONNECT = "CONNECT"

    def send(self, msgList):
        """Sends the specified message to an IRC server
           This method supposes that the message is correct!."""
        msg = ' '.join(msgList)
        if msgList[0] == self.CONNECT:
            self.clientPort = random.randint(1025, 65530)
            self.serverIp = msgList[1]
             # TODO: Check TCP handshake

        segment = TcpSegment(msg, self.clientPort, self.serverPort)
        datagram = IpDatagram(segment, self.clientIp, self.serverIp)
        return datagram

    def receive(self, packet):
        """Receives and parses a package from the IRC server."""
        msg = packet.getSegment().getMessage()

        # Received CONNECT confirmation
        if msg[0] == '0':
            self.serverIp = packet.getOriginIp()
        # Received USER confirmation
        elif msg[0] == '1':
            pass
        # Received QUIT confirmation
        elif msg[0] == '2':
            self.clientPort = None
            self.serverIp = None
            # End of connection handshake

        return None

    def requireDns(self, msgList):
        """Checks if the client command is a CONNECT that requires
           the DNS server."""
        if msgList[0] == self.CONNECT and not \
           re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", msgList[1]):
                return msgList[1]
        return None
