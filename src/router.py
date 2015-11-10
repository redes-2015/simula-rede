"""Represents a router on the network simulation."""

# -------------------------------------------------------------


class Router:

    def __init__(self, name, numInterfaces):
        """Initializes the router with a name and number of interfaces."""
        self.name = name
        self.numInterfaces = numInterfaces

        # Initializes empty attributes
        self.timePerformance = None
        self.interfaces = {}
        self.routes = {}
        self.bufferSizes = {}

    def addPort(self, port, ip):
        """Adds a new port, with its respective IP, to the router."""
        self.interfaces[port] = ip

    def addRoute(self, subnetwork, port):
        """Configures a new subnetwork to the router's specified port."""
        self.routes[subnetwork] = port

    def setBufferSize(self, port, bufferSize):
        """Sets the router's specified port to have a certain buffer size."""
        self.bufferSizes[port] = bufferSize

    def setTimePerformance(self, timePerformance):
        """Sets the time to process a package."""
        self.timePerformance = timePerformance

    def runThread(self):
        """Router's infinite thread loop. Receives and sends packages
           to hosts/routers."""
        while True:
            # TODO: Many things here...
            print()
