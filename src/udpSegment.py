"""Represents the UDP protocol on the simulated network."""

from transportSegment import TransportSegment

# -------------------------------------------------------------


class UdpSegment(TransportSegment):

    def __init__(self, msg, originPort, destinationPort):
        """Initializes data on UDP header."""
        super().__init__(msg, originPort, destinationPort)

    def info(self):
        """Shows information regarding the UDP protocol about the segment."""
        info = ">>>> UDP" + '\n'
        info += super().info()
        info += "  Size: %d" % self.size() + '\n'

        info += ">>>> DNS" + '\n'
        info += "  Message: \"" + self.msg + "\""

        return info

    def size(self):
        """Returns the UDP header size summed with the message size."""
        # UDP header always has a size of 8 bytes:
        # - 4 bytes, 2 for each port
        # - 2 bytes for Checksum
        # - 2 bytes for (UDP header + messages) length
        return 8 + self.getMessageSize()
