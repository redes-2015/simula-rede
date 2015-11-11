"""Represents a router on the network simulation."""

import queue

# -------------------------------------------------------------


class Router:

    def __init__(self, name, numInterfaces):
        """Initializes the router with a name and number of interfaces."""
        self.name = name
        self.numInterfaces = numInterfaces

        # Initialize each port
        self.interfaces = {}
        self.portBuffer = {}
        for x in range(numInterfaces):
            self.addPort(x, None)

        # Initializes empty attributes
        self.timePerformance = None
        self.routes = {}
        self.links = {}

    def addPort(self, port, ip):
        """Adds a new port, with its respective IP, to the router."""
        self.interfaces[port] = ip
        self.portBuffer[port] = queue.LifoQueue()

    def addRoute(self, subnetwork, port):
        """Configures a new subnetwork to the router's specified port."""
        self.routes[subnetwork] = port

    def setBufferSize(self, port, bufferSize):
        """Sets the router's specified port to have a certain buffer size."""
        self.portBuffer[port].maxsize = bufferSize

    def setTimePerformance(self, timePerformance):
        """Sets the time to process a package."""
        self.timePerformance = timePerformance

    def getBufferQueue(self, port):
        print(self.portBuffer.keys())
        return self.portBuffer[port]

    def addBufferQueue(self, port, packet):
        self.portBuffer[port].put(packet)

    def addLink(self, port, link):
        self.links[port] = link

    def proc(self, port, packet):
        destination = packet.getDestination()
        subnetwork = __findSubnetwork(destination)
        # TODO: Send the packet to who is connected to self.routes[subnetwork]

    def runThread(self, port):
        """Router's infinite thread loop. Receives and sends packages
           to hosts/routers."""
        while True:
            packet = self.portBuffer[port].get()
            self.proc(port, packet)
            self.portBuffer[port].task_done()

    def __findSubnetwork(destination):
        finalDot = destination.rfind('.')
        return destination[0:finalDot] + ".0"
