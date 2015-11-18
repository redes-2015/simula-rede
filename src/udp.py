"""Represents the UDP protocol on the simulated network."""

from transport import Transport

# -------------------------------------------------------------


class UDP(Transport):

    def __init__(self, msg, originPort, destinationPort):
        """Initializes data on UDP header."""
        super(msg, originPort, destinationPort)
        # TODO: Checksum

    def messageSize(self):
        """Returns size of application message. in bytes."""
        return sys.getsizeof(self.msg)

    def headerSize(self):
        "Returns size of UDP header, in bytes."""
        # TODO: Do checksum first, use 16 bits for each port
        pass
