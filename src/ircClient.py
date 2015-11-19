"""Represents an IRC client on the network simulation."""

from tcpSegment import TCPSegment
from ipDatagram import IPDatagram

# -------------------------------------------------------------


class IrcClient:

    def __init__(self, clientIP):
        """Initializes client's attributes."""
        self.clientIP = clientIP
        self.clientPort = 1025
        self.serverPort = 6667  # Default port for IRC servers
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

        transport = TCPSegment(msg, self.clientPort, self.serverPort)
        datagram = IPDatagram(self.clientIP, self.serverIP, transport)
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

    def __updateClientPort(self):
        """Updates used client ports."""
        self.clientPort += 1
        if self.clientPort > 65530:
            self.clientPort = 1025
