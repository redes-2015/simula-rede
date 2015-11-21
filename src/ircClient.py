"""Represents an IRC client on the network simulation."""

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

        self.ackNumber = None
        self.seqNumber = None

        # Comandos parseados no cliente
        self.CONNECT = "CONNECT"

    def setClientPort(self, clientPort):
        """Sets the client's port number to the specified value."""
        self.clientPort = clientPort

    def send(self, msgList):
        """Sends the specified message to an IRC server
           This method supposes that the message is correct!."""
        msg = ' '.join(msgList)
        if msgList[0] == self.CONNECT:
            self.ackNumber = self.seqNumber = 1
            self.serverIp = msgList[1]

        segment = TcpSegment(msg, self.clientPort, self.serverPort)
        segment.setACK()
        segment.setAckNumber(self.ackNumber)
        segment.setSeqNumber(self.seqNumber)
        datagram = IpDatagram(segment, self.clientIp, self.serverIp)
        if self.serverIp is None:
            raise Exception("IRC client must CONNECT first!")

        return datagram

    def receive(self, packet):
        """Receives and parses a package from the IRC server."""
        msg = packet.getSegment().getMessage()

        # Update acknowledgement and sequence numbers
        self.ackNumber = packet.getSegment().getSeqNumber()
        self.seqNumber = packet.getSegment().getAckNumber()
        self.seqNumber += packet.getSegment().getMessageSize()

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

        return None

    def requireDns(self, msgList):
        """Checks if the client command is a CONNECT that requires
           the DNS server."""
        if msgList[0] == self.CONNECT and not \
           re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", msgList[1]):
                return msgList[1]
        return None

    def __tcpCloseConnection(self, serverPacket):
        """Close TCP connection by doing a handshake with
           the server."""

        # Sends a FIN/ACK message to close connection
        # TODO: Think of what to do here...
        segment = TcpSegment("", finalSegment.getOriginPort(), self.ircPort)
        segment.setFIN()
        segment.setACK()
        segment.setAckNumber(serverPacket.getSegment().getSeqNumber())
        segment.setSeqNumber(1)
        datagram = IpDatagram(segment, self.ipAddr, serverIp)
        self.link.putTargetQueue(datagram)
        packet = self.netQueue.get()
