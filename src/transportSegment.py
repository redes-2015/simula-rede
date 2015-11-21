"""Base class for transport layer protocols."""

import sys

# -------------------------------------------------------------


class TransportSegment:

    def __init__(self, msg, originPort, destinationPort):
        """Initializes data common for all transport layer protocols."""
        self.msg = msg
        self.originPort = originPort
        self.destinationPort = destinationPort

    def info(self):
        """Returns information that any transport layer protocol contains."""
        info = ("  To:   %5d" % self.destinationPort) + '\n'
        info += ("  From: %5d" % self.originPort) + '\n'
        return info

    def getMessage(self):
        """Returns the application message stored by the protocol."""
        return self.msg

    def getMessageSize(self):
        """Returns size of application message, in bytes."""
        return len(self.msg)

    def getOriginPort(self):
        """Returns the origin port stored by the protocol."""
        return self.originPort

    def getDestinationPort(self):
        """Returns the destination port stored by the protocol."""
        return self.destinationPort
