"""Represents the TCP protocol on the simulated network."""

from transportSegment import TransportSegment

# -------------------------------------------------------------


class TcpSegment(TransportSegment):

    def __init__(self, msg, originPort, destinationPort):
        """Initializes data on TCP header."""
        super().__init__(msg, originPort, destinationPort)
        self.SYN = self.ACK = self.FIN = False
        self.ackNumber = self.seqNumber = 0

    def info(self):
        """Returns information regarding the TCP protocol about
           the segment."""
        info = ">>>> TCP" + '\n'
        info += super().info()
        info += ("  Seq Number: %3d" % self.getSeqNumber()) + '\n'

        if self.ACK is True:
            info += ("  Ack Number: %3d" % self.getAckNumber()) + '\n'
        info += "  "

        if self.ACK is True:
            info += "[ACK] "
        if self.FIN is True:
            info += "[FIN] "
        if self.SYN is True:
            info += "[SYN]"

        info += '\n' + ">>>> IRC" + '\n'
        info += "  Message: \"" + self.msg + "\""

        return info

    def setSeqNumber(self, seqNumber):
        """Sets the TCP protocol's Sequence Number."""
        self.seqNumber = seqNumber

    def getSeqNumber(self):
        """Returns the Sequence Number."""
        return self.seqNumber

    def setAckNumber(self, ackNumber):
        """Sets the TCP protocol's Acknowledgement Number."""
        self.ackNumber = ackNumber

    def getAckNumber(self):
        """Returns the Acknowledgement Number."""
        return self.ackNumber

    def setSYN(self):
        """Sets the SYN bit, establishing a connection."""
        self.SYN = True

    def getSYN(self):
        """Returns the SYN bit."""
        return self.SYN

    def setACK(self):
        """Sets the ACK bit, related to checking data received."""
        self.ACK = True

    def getACK(self):
        """Returns the ACK bit."""
        return self.ACK

    def setFIN(self):
        """Sets the FIN bit, informing that the TCP connection
           can be closed."""
        self.FIN = True

    def getFIN(self):
        """Returns the FIN bit."""
        return self.FIN
