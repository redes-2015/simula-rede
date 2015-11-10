"""Creates and executes a network simulation based on a file."""

from host import Host
from router import Router
from threading import Thread

# -------------------------------------------------------------


class Simulator:

    def __init__(self, filename):
        """Initializes the simulator's attributes."""
        self.filename = filename
        self.hosts = {}
        self.routers = {}

    def start(self):
        """Starts the simulation."""
        # Process file
        self.__parseFile()
        print("<-- End of File -->")

        # Begin simulation
        for pc in self.hosts:
            self.hosts[pc].thread = Thread(target=self.hosts[pc].runThread)
            self.hosts[pc].thread.start()
        # TODO: Simulate routers

    def createHost(self, name):
        """Creates a host with the given name."""
        print("Host: %s" % name)
        host = Host(name)
        self.hosts[name] = host

    def createRouter(self, name, numInterfaces):
        """Creates a router with the given name and number of interfaces."""
        print("Router: %s [%d interfaces]" % (name, numInterfaces))
        router = Router(name, numInterfaces)
        self.routers[name] = router

    def configHost(self, name, ipAddr, routerAddr, dnsAddr):
        """Configures the host's and its default router's IP.
           Also sets the DNS server's IP."""
        print("{IP} Host %s: %s, [Router] %s, [DNS] %s" %
              (name, ipAddr, routerAddr, dnsAddr))
        self.hosts[name].setIp(ipAddr, routerAddr, dnsAddr)

    def configRouter(self, name, port, ipAddr):
        """Configures the IP address of one of the router's ports."""
        print("{IP} Router %s.%d: %s" % (name, port, ipAddr))
        self.routers[name].addPort(port, ipAddr)

    def createDuplexLink(self, side1, side2, bandwidth, delay):
        """Creates a link between hosts/routers (sides 1 and 2).
           Also configures the link's bandwidth (in Mbps) and
           delay (in ms)."""
        print("{Link} %s <=> %s [%g Mbps, %g ms]" %
              (side1, side2, bandwidth, delay))

    def createRoute(self, name, subnetwork, route):
        """Creates a specified route from a router to a subnetwork."""
        print("{Route} %s -> %s:%s" % (name, subnetwork, route))
        self.routers[name].addRoute(subnetwork, route)

    def defineTimePerformance(self, name, time):
        """Sets time to process a package for a given router."""
        print("{Time} %s: %g us" % (name, time))
        self.routers[name].setTimePerformance(time)

    def definePortPerformance(self, name, port, bufferSize):
        """Defines buffer size for a specified router's port."""
        print("{Buffer} %s.%d: %g" % (name, port, bufferSize))
        self.routers[name].setBufferSize(port, bufferSize)

    def startApplication(self, hostname, appName, appType):
        """Defines an application level protocol on the given host."""
        print("{Application} %s: %s [%s]" % (hostname, appName, appType))

    def createSniffer(self, name, target, outputFile):
        """Creates a sniffer between 'name' and 'target'. Information its
           shown in standard output and specified 'outputFile.'"""
        # Sniffer name? Shouldn't it be link? (TODO: Check this)
        print("{Sniffer} %s <-> %s [Output '%s']" % (name, target, outputFile))

    def simulateCommand(self, time, appName, command):
        """Runs 'appName' with the given command at the specified time."""
        print("{Simulate} %s %s [t = %g]" % (appName, command, time))

    def finish(self, time):
        """Ends the simulation at the specified time."""
        print("**FINISH [t = %g]**" % time)

    def __parseFile(self):
        with open(self.filename, 'r') as simulFile:
            while True:
                line = simulFile.readline()

                # Checks for EOF
                if line == "":
                    break

                # Cleans whitespaces and "\n" at the end
                line = line.rstrip()

                # Ignores empty lines and comments
                if line == "" or line[0] == '#':
                    continue

                # Checks if line continues (ends with '\')
                while line[-1] == '\\':
                    line = line[0:-1]
                    nextLine = simulFile.readline().rstrip()
                    line = line + nextLine

                msg = line.split()

                # Parse 'set' commands
                if msg[0] == 'set':
                    if msg[1] == 'host':
                        name = msg[2]
                        self.createHost(name)

                    elif msg[1] == 'router':
                        name = msg[2]
                        numInterfaces = int(msg[3])
                        self.createRouter(name, numInterfaces)

                    elif msg[1] == 'duplex-link':
                        side1 = msg[2]
                        side2 = msg[3]

                        # Removes 'Mbps' and 'ms' at end of string before
                        # converting to float
                        bandwidth = float(msg[4][:-4])
                        delay = float(msg[5][:-2])

                        self.createDuplexLink(side1, side2, bandwidth, delay)

                    elif msg[1] == 'ip':
                        name = msg[2]

                        try:
                            port = int(msg[3])
                            for x in range(3, len(msg), 2):
                                self.configRouter(name, int(msg[x]), msg[x+1])

                        except ValueError:
                            ipAddr = msg[3]
                            routerAddr = msg[4]
                            dnsAddr = msg[5]
                            self.configHost(name, ipAddr, routerAddr, dnsAddr)

                    elif msg[1] == 'route':
                        routerName = msg[2]

                        # Reads two arguments (subnetwork, route) at a time
                        for x in range(3, len(msg), 2):
                            self.createRoute(routerName, msg[x], msg[x+1])

                    elif msg[1] == 'performance':
                        name = msg[2]

                        # Removes "us" at end of string before
                        # converting to float
                        time = float(msg[3][:-2])

                        self.defineTimePerformance(name, time)
                        for x in range(4, len(msg), 2):
                            port = int(msg[x])
                            bufferSize = float(msg[x+1])
                            self.definePortPerformance(name, port, bufferSize)

                    elif msg[1] in ['ircc', 'ircs', 'dnss']:
                        hostname = msg[2]
                        appName = msg[3]
                        appType = msg[1]
                        self.startApplication(hostname, appName, appType)

                    elif msg[1] == 'sniffer':
                        name = msg[2]
                        target = msg[3]
                        outputFile = msg[4]
                        self.createSniffer(name, target, outputFile)

                elif msg[0] == 'simulate':
                    time = float(msg[1])
                    appName = msg[2]
                    command = msg[3:]

                    # Removes a " from the beginning of first string
                    command[0] = command[0][1:]

                    # Removes a " from the end of final string
                    command[-1] = command[-1][0:-1]

                    self.simulateCommand(time, appName, command)

                elif msg[0] == 'finish':
                    time = float(msg[1])
                    self.finish(time)

                else:
                    print(line)
