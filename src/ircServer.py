"""Represents an IRC server on the network simulation."""

from tcpSegment import TcpSegment
from ipDatagram import IpDatagram

# -------------------------------------------------------------


class IrcServer:

    def __init__(self, serverIp):
        """Initializes the server's listening socket."""
        self.serverIp = serverIp
        self.serverPort = 6667    # IRC's default port

        # Valid commands
        self.CONNECT = "CONNECT"
        self.USER = "USER"
        self.QUIT = "QUIT"

        # 'IP:Port -> Username' for connected clients
        self.connections = {}

    def receive(self, packet):
        """Receives a packet. Based on its message, returns
           a response packet."""
        # Reads basic data from received packet
        clientIp = packet.getOriginIp()
        segment = packet.getSegment()
        clientPort = segment.getOriginPort()
        msg = packet.getSegment().getMessage()

        # Adjusts ack and seq numbers
        ackNumber = segment.getSeqNumber() + segment.getMessageSize()
        seqNumber = segment.getAckNumber()

        # Received a SYN packet; establish connection with client
        if segment.getSYN() is True:
            clientIp = packet.getOriginIp()
            synSegment = TcpSegment("", self.serverPort, clientPort)
            synSegment.setSYN()
            synSegment.setACK()
            synSegment.setAckNumber(1)
            synSegment.setSeqNumber(seqNumber)
            return IpDatagram(synSegment, self.serverIp, clientIp)

        # Received a FIN packet; close connection with client
        elif segment.getFIN() is True:
            clientIp = packet.getOriginIp()
            finSegment = TcpSegment("", self.serverPort, clientPort)
            finSegment.setFIN()
            finSegment.setACK()
            finSegment.setAckNumber(ackNumber + 1)
            finSegment.setSeqNumber(seqNumber)
            return IpDatagram(finSegment, self.serverIp, clientIp)

        # Received an ACK packet; do nothing
        elif msg == "":
            return None

        # Packet contains a message from the client;
        # send an ACK packet and a message packet

        # ACK packet
        ackSegment = TcpSegment("", self.serverPort, clientPort)
        ackSegment.setACK()
        ackSegment.setAckNumber(ackNumber)
        ackSegment.setSeqNumber(seqNumber)

        ackPacket = IpDatagram(ackSegment, self.serverIp, clientIp)

        # Response packet (contains a non-empty message)
        respMessage = self.__parseMessage([clientIp, clientPort], msg)

        respSegment = TcpSegment(respMessage, self.serverPort, clientPort)
        respSegment.setACK()
        respSegment.setAckNumber(ackNumber)
        respSegment.setSeqNumber(seqNumber)

        respPacket = IpDatagram(respSegment, self.serverIp, clientIp)

        return [ackPacket, respPacket]

    def __parseMessage(self, addr, msg):
        """Parses a message received by a client with the given address
           'addr' (which is a list [IP, Port])."""
        addrStr = addr[0] + ':' + str(addr[1])

        msg = msg.rstrip('\r\n')
        msg = msg.rstrip(' ')
        separate = msg.split(' ')
        response = ""

        if separate[0] == self.CONNECT:
            response = "0 Connection successful! Welcome!"
            self.connections[addrStr] = None

        elif separate[0] == self.USER:
            username = separate[1]
            # Supposes that a client won't try
            # to use an already defined username
            self.connections[addrStr] = username
            response = "1 Username '" + username + "' successfully defined!"

        elif separate[0] == self.QUIT:
            # 'None' is the returning value
            # in case 'addrStr' key doesn't exist
            self.connections.pop(addrStr, None)
            response = "2 You have left the server. Until next time!"

        return response
