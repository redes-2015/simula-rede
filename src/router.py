"""Represents a router on the network simulation."""

import queue

# -------------------------------------------------------------


class Router:

    def __init__(self, name, numPorts):
        """Initializes the router with a name and number of ports."""
        self.name = name
        self.numPorts = numPorts

        self.ports = {}       # port number -> IP
        self.portBuffer = {}  # port number -> the port's buffer queue
        for x in range(numPorts):
            self.addPort(x, None)

        # Initializes empty attributes
        self.timePerformance = None
        self.routes = {}  # subnetwork -> port
        self.links = {}   # port number -> queue of an other host or router port

    def addPort(self, port, ip):
        """Adds a new port, with its respective IP, to the router."""
        self.ports[port] = ip
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
        """Returns the router's buffer queue for a given port."""
        print(self.portBuffer.keys())
        return self.portBuffer[port]

    def addBufferQueue(self, port, packet):
        """Adds a packet to the buffer of a given port on the router."""
        self.portBuffer[port].put(packet)

    def addLink(self, port, link):
        """Links the router's port to a host's queue or
           another router's buffer."""
        self.links[port] = link

    def process(self, port, packet):
        """Processes a packet received from the network."""
        destination = packet.getDestination()
        subnetwork = __findSubnetwork(destination)
        # TODO: Send the packet to who is connected to self.routes[subnetwork]

    def runThread(self, port):
        """Router's infinite thread loop. Receives and sends packages
           to hosts/routers."""
        while True:
            packet = self.portBuffer[port].get()
            self.process(port, packet)
            self.portBuffer[port].task_done()

    def __findSubnetwork(destination):
        """Returns the subnetwork (ends with ".0") of a given
           IP destination."""
        finalDot = destination.rfind('.')
        return destination[0:finalDot] + ".0"
