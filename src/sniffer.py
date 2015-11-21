"""Represents a sniffer that monitors a link between entities
   on the network."""

import time

# -------------------------------------------------------------


class Sniffer:

    def __init__(self, nodeA, nodeB, fileDescriptor, startTime):
        """Initializes the sniffer."""
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.fileDescriptor = fileDescriptor
        self.startTime = startTime

    def write(self, packet):
        """Writes information regarding a packet sent
           from nodeA to nodeB."""
        out = "{" + packet.getId() + "}\n"
        out += ("t = %.04fs" % (time.time() - self.startTime)) + '\n'
        out += self.nodeA + " -> " + self.nodeB + '\n'
        out += packet.info() + '\n'
        print(out, end="")
        self.fileDescriptor.write(out)
        self.fileDescriptor.flush()
