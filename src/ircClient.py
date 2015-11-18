"""Represents an IRC client on the network simulation."""

# -------------------------------------------------------------

class IrcClient:

    def __init__(self, clientIP, clientPort):
        """Initializes client's attributes."""
        self.clentIP = clientIP
        self.clientPort = clientPort
        self.serverPort = 6667  # Default port for IRC servers

        # Comandos parseados no cliente
        self.CONNECT = "CONNECT"

    def send(self, msgList):
        """Sends the specified message to an IRC server
           This method supposes that the message is correct!."""
        if msgList[0] == self.CONNECT:
            msg = ' '.join(msgList)
            transport = TCPSegment(msg, self.clientPort, self.serverPort)
            datagram = IPDatagram(self.clientIP, )
        else:
            pass  # TODO: Send message through socket
        # TODO: Receive response from server
