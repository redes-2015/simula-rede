"""Represents the TCP protocol on the simulated network."""

from transportSegment import TransportSegment

# -------------------------------------------------------------


class TCPSegment(TransportSegment):

    def __init__(self, msg, originPort, destinationPort):
        """Initializes data on TCP header."""
        super().__init__(msg, originPort, destinationPort);
        self.SYN = self.ACK = self.FIN = False
        self.ackNumber = 0

    def getSequenceNumber(self):
        "Returns the Unicode number of the application message's first byte."""
        # TODO: Not sure about len(msg) below
        if len(msg) == 0:
            return 0
        return ord(msg[0])

    def setAckNumber(self, ackNumber):
        """???"""
        self.ackNumber = ackNumber

    def setSYN(self):
        """Sets the SYN bit, establishing a connection."""
        self.SYN = True

    def setACK(self):
        """Sets the ACK bit, related to checking data received."""
        self.ACK = True

    def setFIN(self):
        """Sets the FIN bit, informing that the TCP connection can be closed."""
        self.FIN = True
