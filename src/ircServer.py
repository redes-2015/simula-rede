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
        originIp = packet.getOriginIp()
        msg = packet.getSegment().getMessage()
        segment = packet.getSegment()

        # Creates a packet to be sent as a response
        serverMsg = self.__parseMessage(originIp, msg)
        respSegment = TcpSegment(serverMsg, self.serverPort,
                                 packet.getSegment().getOriginPort())

        if segment.getSYN() is False and segment.getFIN() is False \
            and segment.getMessage() == "":
                return None
        if segment.getSYN() is True:
            # Establish connection with client
            clientIp = packet.getOriginIp()
            clientPort = segment.getOriginPort()
            respSegment.setSYN()
            respSegment.setACK()
            respSegment.setAckNumber(1)
        else:
            ackNumber = segment.getAckNumber()
            seqNumber = segment.getSeqNumber()
            respSegment.setACK()
            respSegment.setAckNumber(seqNumber)
            respSegment.setSeqNumber(ackNumber + segment.getMessageSize())

        respPacket = IpDatagram(respSegment, self.serverIp, packet.getOriginIp())
        return respPacket

    def __parseMessage(self, addr, msg):
        """Parses a message received by a client with the given address
           'addr' (which is a list [IP, Port])."""
        addrStr = addr[0] + ':' + addr[1]

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
