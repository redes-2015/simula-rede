"""Represents an IRC server on the network simulation."""

# -------------------------------------------------------------


class IrcServer:

    def __init__(self):
        """Initializes the server's listening socket."""
        # IRC's default port
        self.port = 6667

        # Valid commands
        self.CONNECT = "CONNECT"
        self.USER = "USER"
        self.QUIT = "QUIT"

        # Dictionary 'IP:Port -> Username' for connected clients
        self.connections = {}

        # TODO: Create listening TCP socket and bind it

    def run(self):
        """IRC server's infinite loop, checks for incoming messages."""
        while True:
            pass  # TODO: Check sockets for new connections/messages

    def parseMessage(self, addr, msg):
        """Parses a message received by a client with the given address
           'addr' (which is a list [IP, Port])."""
        addrStr = addr[0] + ':' + addr[1]

        msg = msg.rstrip('\r\n')
        msg = msg.rstrip(' ')
        separate = msg.split(' ')

        if separate[0] == CONNECT:
            response = "Connection successful!\r\n"
            self.connections[addrStr] = None

        elif separate[0] == USER:
            # Supposes that a client won't try
            # to use an already defined username
            self.connections[addrStr] = username
            response = "Username '" + username + "' successfully defined!"

        elif separate[0] == QUIT:
            # 'None' is the returning value
            # in case 'addrStr' key doesn't exist
            self.connections.pop(addrStr, None)
            resposta = "You have left the server."

        return response
