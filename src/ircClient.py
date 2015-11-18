"""Represents an IRC client on the network simulation."""

# -------------------------------------------------------------


class IrcClient:

    def __init__(self):
        """Initializes client's attributes."""
        self.socket = None
        self.ip = None
        self.port = None

        # Comandos parseados no cliente
        self.CONNECT = "CONNECT"

    def send(self, msg):
        """Sends the specified message to an IRC server
           This method supposes that the message is correct!."""
        separate = msg.split(' ')
        if separate[0] == self.CONNECT:
            pass  # TODO: Create TCP socket and connect to IRC server
        else:
            pass  # TODO: Send message through socket
        # TODO: Receive response from server
