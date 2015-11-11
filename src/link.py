"""???"""

class Link:

    def __init__(self, targetQueue, bandwidth, delay):
        self.targetQueue = targetQueue
        self.bandwidth = bandwidth
        self.delay = delay

    def getTargetQueue(self):
        return self.targetQueue

    def getBandwidth(self):
        return self.bandwidth

    def getDelay(self):
        return self.delay
