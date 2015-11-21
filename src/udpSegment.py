"""Represents the UDP protocol on the simulated network."""

import sys
from transportSegment import TransportSegment

# -------------------------------------------------------------


class UdpSegment(TransportSegment):

    def __init__(self, msg, originPort, destinationPort):
        """Initializes data on UDP header."""
        super().__init__(msg, originPort, destinationPort)
        # TODO: Checksum

    def info(self):
        """Shows information regarding the UDP protocol about the segment."""
        info = ">>>> UDP" + '\n'
        info += super().info()

        msgSize = sys.getsizeof(self.msg)
        headerSize = sys.getsizeof(self) - msgSize
        info += ("  Size: %3d" % headerSize) + " (UDP Header)\n"
        info += ("        %3d" % msgSize) + " (Above)\n"

        info += ">>>> DNS" + '\n'
        info += "  Message: \"" + self.msg.decode() + "\""

        return info

    def headerSize(self):
        "Returns size of UDP header, in bytes."""
        # TODO: Do checksum first, use 16 bits for each port
        pass
