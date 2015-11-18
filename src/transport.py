"""Base class for transport layer protocols."""

# -------------------------------------------------------------


class Transport:

    def __init__(self, msg, originPort, destinationPort):
        """Initializes data common for all transport layer protocols."""
        self.msg = msg.encode()
        self.originPort = originPort
        self.destinationPort = destinationPort

    def getMessage(self):
        """Returns the application message stored by the protocol."""
        return self.msg.decode()

    def getOrigin(self):
        """Returns the origin port stored by the protocol."""
        return self.originPort

    def getDestination(self):
        """Returns the destination port stored by the protocol."""
        return self.destinationPort
