"""Represents a packet sent or received by a host/router on the network."""

# -------------------------------------------------------------


class Packet:

    def __init__(self):
        """Initializes all layers in the packet with an empty value."""
        self.msg = None
        self.transport = None
        self.network = None

    def addMessage(self, msg):
        """Adds the specified msg to the packet (application layer)."""
        self.msg = msg

    def addTransport(self):
        """???"""
        pass  # TODO

    def addNetwork(self):
        pass  # TODO

    def getMessage(self):
        """Returns the msg stored in the packet (application layer)."""
        return self.msg

    def getTransport(self):
        pass  # TODO

    def getNetwork(self):
        pass  # TODO
