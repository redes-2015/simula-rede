"""Represents the IP protocol on the simulated network."""

from tcpSegment import TCPSegment
from udpSegment import UDPSegment

# Initial TTL values for different systems
UNIX_TTL = 64
WINDOWS_TTL = 128

# -------------------------------------------------------------


class IPDatagram:

    def __init__(self, originIP, destinationIP, transport):
        """Initializes datagram values."""
        self.originIP = originIP
        self.destinationIP = destinationIP
        self.transport = transport
        self.TTL = UNIX_TTL
        # TODO: Checksum

    def getOriginIP(self):
        """Returns the IP address of who sent the datagram."""
        return self.originIP

    def getDestinationIP(self):
        """Returns the IP address of who will receive the datagram."""
        return self.destinationIP

    def getTransportSegment(self):
        """Returns the transport and application layers part of the datagram."""
        return self.transport

    def getTransportNumber(self):
        """Returns a number identifying the type of transport layer."""
        if type(self.transport) is TCPSegment:
            return 6
        elif type(self.transport) is UDPSegment:
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
