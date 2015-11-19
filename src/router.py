"""Represents a router on the network simulation."""

from queue import Queue, Empty
import threading

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

        # Lock that disallows simultaneous packet sending
        self.lock = threading.Lock()

    def addPort(self, port, ip):
        """Adds a new port, with its respective IP, to the router."""
        self.ports[port] = ip
        self.portBuffer[port] = Queue()

    def addRoute(self, subnetwork, port):
        """Configures a new subnetwork to the router's specified port."""
        self.routes[subnetwork] = port

    def updateRoute(self):
        """???"""
        for key in self.routes:
            try:
                int(self.routes[key])
            except ValueError:
                address = self.routes[key]
                subnetwork = self.__findSubnetwork(address)
                self.routes[key] = self.routes[subnetwork]

    def setBufferSize(self, port, bufferSize):
        """Sets the router's specified port to have a certain buffer size."""
        self.portBuffer[port].maxsize = bufferSize

    def setTimePerformance(self, timePerformance):
        """Sets the time to process a package."""
        self.timePerformance = timePerformance

    def getBufferQueue(self, port):
        """Returns the router's buffer queue for a given port."""
        return self.portBuffer[port]

    def addBufferQueue(self, port, packet):
        """Adds a packet to the buffer of a given port on the router."""
        self.portBuffer[port].put(packet)

    def addLink(self, port, link):
        """Links the router's port to a host's queue or
           another router's buffer."""
        self.links[port] = link

    def setSniffer(self, port, sniffer):
        """Sets a sniffer between the router's port and another entity
           on the network."""
        self.links[port].setSniffer(sniffer)

    def process(self, port, packet):
        """Processes a packet received from the network. This method is
           thread-safe, i.e., only one port can access it at a time."""
        self.lock.acquire()
        destination = packet.getDestinationIP();
        subnetwork = self.__findSubnetwork(destination)
        self.links[int(self.routes[subnetwork])].putTargetQueue(packet)
        self.lock.release()

    def runThread(self, port):
        """Router's infinite thread loop. Receives and sends packages
           to hosts/routers."""
        queue = self.portBuffer[port]
        while True:
            packet = queue.get()
            self.process(port, packet)
            queue.task_done()

    def __findSubnetwork(self, destination):
        """Returns the subnetwork (ends with ".0") of a given
           IP destination."""
        finalDot = destination.rfind('.')
        return destination[0:finalDot] + ".0"
