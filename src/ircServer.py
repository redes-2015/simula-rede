"""Represents an IRC server on the network simulation."""

from tcpSegment import TCPSegment
from ipDatagram import IPDatagram

# -------------------------------------------------------------


class IrcServer:

    def __init__(self, serverIP):
        """Initializes the server's listening socket."""
        self.port = 6667  # IRC's default port
        self.serverIP = serverIP

        # Valid commands
        self.CONNECT = "CONNECT"
        self.USER = "USER"
        self.QUIT = "QUIT"

        # Dictionary 'IP:Port -> Username' for connected clients
        self.connections = {}

        # TODO: Create listening TCP socket and bind it

    def receive(self, packet):
        """Receives a packet. Based on its message, returns a response packet."""
        originIP = packet.getOriginIP()
        msg = packet.getSegment().getMessage()

        # Creates a packet to be sent as a response
        serverMsg = self.__parseMessage(originIP, msg)
        respSegment = TCPSegment(serverMsg, self.port, packet.getSegment().getOrigin())
        respPacket = IPDatagram(self.serverIP, packet.getOriginIP(), respSegment)
        return respPacket


    def __parseMessage(self, addr, msg):
        """Parses a message received by a client with the given address
           'addr' (which is a list [IP, Port])."""
        addrStr = addr[0] + ':' + addr[1]

        msg = msg.rstrip('\r\n')
        msg = msg.rstrip(' ')
        separate = msg.split(' ')

        if separate[0] == self.CONNECT:
            response = "0 Connection successful! Welcome!\r\n"
            self.connections[addrStr] = None

        elif separate[0] == self.USER:
            # Supposes that a client won't try
            # to use an already defined username
            self.connections[addrStr] = username
            response = "1 Username '" + username + "' successfully defined!"

        elif separate[0] == self.QUIT:
            # 'None' is the returning value
            # in case 'addrStr' key doesn't exist
            self.connections.pop(addrStr, None)
            resposta = "2 You have left the server. Until next time!"

        return response
