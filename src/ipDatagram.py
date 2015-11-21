"""Represents the IP protocol on the simulated network."""

import sys

from tcpSegment import TcpSegment
from udpSegment import UdpSegment

# Initial TTL values for different systems
UNIX_TTL = 64
WINDOWS_TTL = 128

TCP_ID = 6
UDP_ID = 17

# -------------------------------------------------------------


class IpDatagram:

    def __init__(self, segment, originIp, destinationIp):
        """Initializes datagram values."""
        self.segment = segment
        self.originIp = originIp
        self.destinationIp = destinationIp
        self.TTL = UNIX_TTL

    def info(self):
        """Returns information regarding the IP protocol about
           the datagram."""
        info = ">>>> IP" + '\n'
        info += "  To:   " + self.destinationIp + '\n'
        info += "  From: " + self.originIp + '\n'
        info += "  Transport Protocol: " + str(self.getTransportType()) + '\n'

        # TODO: Check why getsizeof(self) returns 0 :P
        segmentSize = sys.getsizeof(self.segment)
        headerSize = sys.getsizeof(self) - segmentSize
        info += ("  Size: %3d" % headerSize) + " (IP Header)\n"
        info += ("        %3d" % segmentSize) + " (Above)\n"
        info += "  TTL: " + str(self.TTL) + '\n'

        info += self.segment.info()

        return info + '\n'

    def setId(self, identifier):
        """Sets the packet's unique ID as the specified value."""
        self.identifier = identifier

    def getId(self):
        """Returns the packet's unique ID."""
        return self.identifier

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
            return TCP_ID
        elif type(self.segment) is UdpSegment:
            return UDP_ID
        else:
            raise Exception("Unexpected type of transport protocol!")

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
