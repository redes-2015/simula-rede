"""Defines a link between two nodes (hosts or routers) on the network."""

# -------------------------------------------------------------


class Link:

    def __init__(self, targetQueue, bandwidth, delay):
        """Initializes the link with the queue of the target node,
           as well connection data."""
        self.targetQueue = targetQueue
        self.bandwidth = bandwidth
        self.delay = delay
        self.sniffer = None

    def setSniffer(self, sniffer):
        """Sets a sniffer on the link."""
        self.sniffer = sniffer

    def putTargetQueue(self, packet):
        """Inserts the specified packet into the target queue."""
        if self.sniffer is not None:
            self.sniffer.write(packet)
        self.targetQueue.put_nowait(packet)

    def getBandwidth(self):
        """Returns the link's bandwidth."""
        return self.bandwidth

    def getDelay(self):
        """Returns the link's delay."""
        return self.delay
