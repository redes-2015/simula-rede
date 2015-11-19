"""Creates and executes a network simulation based on a file."""

import sys
from threading import Thread
from queue import Queue
from time import sleep

from host import Host
from router import Router
from link import Link
from sniffer import Sniffer

# -------------------------------------------------------------


class Simulator:

    def __init__(self, filename):
        """Initializes the simulator's attributes."""
        self.filename = filename
        self.hosts = {}
        self.routers = {}
        self.apps = {}
        self.currentTime = 0

        self.snifferFiles = []
        self.dnsTable = {}

    def start(self):
        """Starts the simulation."""
        # Process file
        self.__parseFile()
        print("<-- End of File -->")

    def createHost(self, name):
        """Creates a host with the given name."""
        # print("Host: %s" % name)
        host = Host(name)
        self.hosts[name] = host

    def createRouter(self, name, numInterfaces):
        """Creates a router with the given name and number of interfaces."""
        # print("Router: %s [%d interfaces]" % (name, numInterfaces))
        router = Router(name, numInterfaces)
        self.routers[name] = router
        for x in range(numInterfaces):
            router.thread = Thread(name=name + "." + str(x),
                                   target=router.runThread,
                                   args=(x,),
                                   daemon=True)
            router.thread.start()

    def configHost(self, name, ipAddr, routerAddr, dnsAddr):
        """Configures the host's and its default router's IP.
           Also sets the DNS server's IP."""
        # print("{IP} Host %s: %s, [Router] %s, [DNS] %s" %
        #      (name, ipAddr, routerAddr, dnsAddr))
        self.hosts[name].setIp(ipAddr, routerAddr, dnsAddr)

    def configRouter(self, name, port, ipAddr):
        """Configures the IP address of one of the router's ports."""
        # print("{IP} Router %s.%d: %s" % (name, port, ipAddr))
        self.routers[name].addPort(port, ipAddr)

    def createDuplexLink(self, side1, side2, bandwidth, delay):
        """Creates a link between hosts/routers (sides 1 and 2).
           Also configures the link's bandwidth (in Mbps) and
           delay (in ms)."""
        # print("{Link} %s <=> %s [%g Mbps, %g ms]" %
        #      (side1, side2, bandwidth, delay))

        if '.' in side1 and '.' in side2:
            port1 = int(side1.split('.')[1])
            port2 = int(side2.split('.')[1])
            queue1 = self.routers[side1.split('.')[0]].getBufferQueue(port1)
            queue2 = self.routers[side2.split('.')[0]].getBufferQueue(port2)
            self.routers[side1.split('.')[0]].addLink(
                port1, Link(queue2, bandwidth, delay))
            self.routers[side2.split('.')[0]].addLink(
                port2, Link(queue1, bandwidth, delay))

        else:
            if not '.' in side1:
                aux = side1
                side1 = side2
                side2 = aux
            # 1 is router, 2 is host
            port1 = int(side1.split('.')[1])
            queue1 = self.routers[side1.split('.')[0]].getBufferQueue(port1)
            queue2 = self.hosts[side2].getNetQueue()
            self.routers[side1.split('.')[0]].addLink(
                port1, Link(queue2, bandwidth, delay))
            self.hosts[side2].addLink(Link(queue1, bandwidth, delay))

    def createRoute(self, name, subnetwork, route):
        """Creates a specified route from a router to a subnetwork."""
        # print("{Route} %s -> %s:%s" % (name, subnetwork, route))
        self.routers[name].addRoute(subnetwork, route)

    def defineTimePerformance(self, name, time):
        """Sets time to process a package for a given router."""
        # print("{Time} %s: %g us" % (name, time))
        self.routers[name].setTimePerformance(time)

    def definePortPerformance(self, name, port, bufferSize):
        """Defines buffer size for a specified router's port."""
        # print("{Buffer} %s.%d: %g" % (name, port, bufferSize))
        self.routers[name].setBufferSize(port, bufferSize)

    def startApplication(self, hostname, appName, appType):
        """Defines an application level protocol on the given host."""
        # print("{Application} %s: %s [%s]" % (hostname, appName, appType))
        self.apps[appName] = hostname
        host = self.hosts[hostname]
        host.addApplication(appName, appType)
        # Start host thread
        host.thread = Thread(name=hostname,
                             target=host.runThread,
                             daemon=True)
        host.thread.start()

    def createSniffer(self, name, target, outputFile):
        """Creates a sniffer between 'name' and 'target'. Information its
           shown in standard output and specified 'outputFile.'"""
        # print("{Sniffer} %s <-> %s [Output '%s']" % (name, target, outputFile))
        f = open(outputFile, 'w')
        self.snifferFiles.append(f)

        # Pair receives one of the two lists
        for pair in [[name, target], [target, name]]:
            # Here, pair is a list with two values
            sniffer = Sniffer(pair[0], pair[1], f)
            checkRouter = self.__isRouter(pair[0])
            if checkRouter is not None:
                router = self.routers[checkRouter[0]]
                router.setSniffer(int(checkRouter[1]), sniffer)
            else:
                host = self.hosts[pair[0]]
                host.setSniffer(sniffer)


    def simulateCommand(self, newTime, appName, command):
        """Runs 'appName' with the given command at the specified time."""
        # print("{Simulate} [t = %g] %s %s" % (newTime, appName, command))
        delta = newTime - self.currentTime
        # delta = delta/100.0
        sleep(delta)
        self.currentTime = newTime
        host = self.apps[appName]
        self.hosts[host].addSimQueue(command)

    def finish(self, time):
        """Ends the simulation at the specified time."""
        sleep(4)  # TODO: Check how to control time
        print("**FINISH [t = %g]**" % time)
        for f in self.snifferFiles:
            f.close()
        sys.exit(0)

    def __parseFile(self):
        """Parses the file containing simulation info, setting
           up objects during the process."""
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
                            # Is a router
                            for x in range(3, len(msg), 2):
                                self.configRouter(name, int(msg[x]), msg[x+1])

                        except ValueError:
                            # Is a host
                            ipAddr = msg[3]
                            routerAddr = msg[4]
                            dnsAddr = msg[5]
                            self.configHost(name, ipAddr, routerAddr, dnsAddr)
                            self.dnsTable[name] = ipAddr
                            # TODO: Check what happens if DNS server isn't the last entry
                            if dnsAddr == "1.1.1.1":
                                self.hosts[name].dnsTable = self.dnsTable  # TODO: Create a setter

                    elif msg[1] == 'route':
                        routerName = msg[2]

                        # Reads two arguments (subnetwork, route) at a time
                        for x in range(3, len(msg), 2):
                            self.createRoute(routerName, msg[x], msg[x+1])
                        self.routers[routerName].updateRoute()

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
                        self.createSniffer(name, target, outputFile[1:-1])

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

    def __isRouter(self, entity):
        """Returns a tuple (name, port) if the entity is a
           router, or None otherwise."""
        separate = entity.split('.')
        if len(separate) > 1:
            return (separate[0], separate[1])
        else:
            return None
