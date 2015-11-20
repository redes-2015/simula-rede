"""Represents a sniffer that monitors a link between entities
   on the network."""

# -------------------------------------------------------------


class Sniffer:

    def __init__(self, nodeA, nodeB, fileDescriptor):
        """Initializes the sniffer."""
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.fileDescriptor = fileDescriptor

    def write(self, packet):
        """Writes information regarding a packet sent
           from nodeA to nodeB."""
        out = "{" + self.nodeA + " -> " + self.nodeB + "}"
        out += '\n' + packet.info() + '\n'
        print(out, end="")
        self.fileDescriptor.write(out)
        self.fileDescriptor.flush()
