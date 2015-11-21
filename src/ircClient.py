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

        self.mustClose = False

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

        if self.serverIp is None:
            raise Exception("IRC client must CONNECT first!")

        segment = TcpSegment(msg, self.clientPort, self.serverPort)
        segment.setACK()
        segment.setAckNumber(self.ackNumber)
        segment.setSeqNumber(self.seqNumber)
        datagram = IpDatagram(segment, self.clientIp, self.serverIp)        

        return datagram

    def receive(self, packet):
        """Receives and parses a packet from the IRC server."""
        segment = packet.getSegment()
        msg = segment.getMessage()

        # Packet contains a message from the server;
        # first, read message contained in the packet

        # Received CONNECT confirmation
        if msg[0] == '0':
            self.serverIp = packet.getOriginIp()
        # Received USER confirmation
        elif msg[0] == '1':
            pass
        # Received QUIT confirmation
        elif msg[0] == '2':
            self.mustClose = True

        # Then, create and send an ACK packet
        ackSegment = TcpSegment("", self.clientPort, self.serverPort)

        # Adjusts ack and seq numbers
        self.ackNumber = segment.getSeqNumber() + segment.getMessageSize()
        self.seqNumber = segment.getAckNumber()

        ackSegment.setACK()
        ackSegment.setAckNumber(self.ackNumber)
        ackSegment.setSeqNumber(self.seqNumber)

        ackPacket = IpDatagram(ackSegment, self.clientIp, self.serverIp)

        if self.mustClose:
            self.mustClose = False
            finSegment = TcpSegment("", self.clientPort, self.serverPort)
            finSegment.setFIN()
            finSegment.setAckNumber(self.ackNumber)
            finSegment.setSeqNumber(self.seqNumber)
            finPacket = IpDatagram(finSegment, self.clientIp, self.serverIp)
            self.clientPort = None
            self.serverIp = None
            return [ackPacket, finPacket]

        return ackPacket

    def requireDns(self, msgList):
        """Checks if the client command is a CONNECT that requires
           the DNS server."""
        if msgList[0] == self.CONNECT and not \
           re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", msgList[1]):
                return msgList[1]
        return None
