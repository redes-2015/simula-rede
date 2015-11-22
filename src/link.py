"""Defines a link between two nodes (hosts or routers) on the network."""

import sys
import time

# -------------------------------------------------------------


class Link:

    def __init__(self, targetQueue, bandwidth, delay):
        """Initializes the link with the queue of the target node,
           as well connection data."""
        self.targetQueue = targetQueue
        self.bandwidth = bandwidth
        self.delay = delay/1000  # Divide by 1000 to get time in miliseconds
        self.sniffer = None

    def setSniffer(self, sniffer):
        """Sets a sniffer on the link."""
        self.sniffer = sniffer

    def putTargetQueue(self, packet):
        """Inserts the specified packet into the target queue."""
        # Delay time according to link and packet
        time.sleep(self.__waitTime(sys.getsizeof(packet)))

        if self.sniffer is not None:
            self.sniffer.write(packet)
        try:
            self.targetQueue.put_nowait(packet)
        except queue.Full:
            pass  # Discard packet if buffer is full

    def getBandwidth(self):
        """Returns the link's bandwidth."""
        return self.bandwidth

    def getDelay(self):
        """Returns the link's delay."""
        return self.delay

    def __waitTime(self, packetSize):
        """Calculates delay time for sending a packet with the
           specified time."""
        # Bandwidth: Converts Mb to bytes and applies it
        # to the packet size
        waitTime = 8*packetSize/(self.bandwidth*1000000)

        # Adds link delay
        waitTime += self.delay

        return waitTime
