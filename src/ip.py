"""Represents the IP protocol on the simulated network."""

from tcp import TCP
from udp import UDP

# Initial TTL values for different systems
UNIX_TTL = 64
WINDOWS_TTL = 128

# -------------------------------------------------------------


class IP:

    def __init__(self, originIp, destinationIp, transport):
        """Initializes datagram values."""
        self.originIp = originIp
        self.destinationIp = destinationIp
        self.transport = transport
        self.TTL = UNIX_TTL
        # TODO: Checksum

    def getOriginIP(self):
        """Returns the IP address of who sent the datagram."""
        return self.originIp

    def getDestinationIP(self):
        """Returns the IP address of who will receive the datagram."""
        return self.destinationIp

    def getTransportNumber(self):
        """Returns a number identifying the type of transport layer."""
        if type(self.transport) is TCP:
            return 6
        elif type(self.transport) is UDP:
            return 17
        else:
            raise Exception("Unexpected type of transport protocol!")

    def headerSize(self):
        "Returns size of UDP header, in bytes."""
        # TODO: Do checksum first, use 16 bits for each port
        pass

    def upperLayersSize(self):
        """Returns size of the upper layers, in bytes."""
        return sys.getsizeof(self.transport)

    def getTTL(self):
        """Returns the datagram's TTL (Time to Live) value."""
        return self.TTL

    def reduceTTL(self):
        """Reduces the TTL count by 1. Returns True if it reached 0,
           or False otherwise."""
        self.TTL -= 1
        return self.TTL <= 0
