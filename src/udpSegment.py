"""Represents the UDP protocol on the simulated network."""

from transportSegment import TransportSegment

# -------------------------------------------------------------


class UDPSegment(TransportSegment):

    def __init__(self, msg, originPort, destinationPort):
        """Initializes data on UDP header."""
        super(msg, originPort, destinationPort)
        # TODO: Checksum

    def messageSize(self):
        """Returns size of application message, in bytes."""
        return sys.getsizeof(self.msg)

    def headerSize(self):
        "Returns size of UDP header, in bytes."""
        # TODO: Do checksum first, use 16 bits for each port
        pass
