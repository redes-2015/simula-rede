"""Represents the IP protocol on the simulated network."""

from tcpSegment import TcpSegment
from udpSegment import UdpSegment

# Initial TTL values for different systems
UNIX_TTL = 64
WINDOWS_TTL = 128

# -------------------------------------------------------------


class IpDatagram:

    def __init__(self, segment, originIp, destinationIp):
        """Initializes datagram values."""
        self.segment = segment
        self.originIp = originIp
        self.destinationIp = destinationIp
        self.TTL = UNIX_TTL
        # TODO: Checksum

    def info(self):
        """Shows information regarding the IP datagram. Used for testing!"""
        info = "To:: " + self.destinationIp + ':'
        info += str(self.segment.getDestinationPort()) + '\n'

        info += "From:: " + self.originIp + ':'
        info += str(self.segment.getOriginPort()) + '\n'

        # Gets transport layer's object name, and prints its first 3 characters
        info += "Transport layer: " + str(self.getTransportType()) + '\n'

        info += "TTL: " + str(self.TTL) + '\n'
        info += "Message: " + self.segment.getMessage() + '\n'
        return info

    def getOriginIp(self):
        """Returns the IP address of who sent the datagram."""
        return self.originIp

    def getDestinationIp(self):
        """Returns the IP address of who will receive the datagram."""
        return self.destinationIp

    def getSegment(self):
        """Returns the transport and application layers part
           of the datagram."""
        return self.segment

    def getTransportType(self):
        """Returns a number identifying the type of transport layer."""
        if type(self.segment) is TcpSegment:
            return 6
        elif type(self.segment) is UdpSegment:
            return 17
        else:
            raise Exception("Unexpected type of transport protocol!")

    def headerSize(self):
        "Returns size of UDP header, in bytes."""
        # TODO: Do checksum first, use 16 bits for each port
        pass

    def upperLayersSize(self):
        """Returns size of the upper layers, in bytes."""
        return sys.getsizeof(self.segment)

    def getTTL(self):
        """Returns the datagram's TTL (Time to Live) value."""
        return self.TTL

    def reduceTTL(self):
        """Reduces the TTL count by 1. Returns True if it reached 0,
           or False otherwise."""
        self.TTL -= 1
        return self.TTL <= 0
