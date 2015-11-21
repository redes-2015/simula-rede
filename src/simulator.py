"""Creates and executes a network simulation based on a file."""

import sys
import queue
import threading
import time

from host import Host
from router import Router
from link import Link
from sniffer import Sniffer

# -------------------------------------------------------------


class Simulator:

    def __init__(self, filename):
        """Initializes the simulator's attributes."""
        self.filename = filename

        self.hosts = {}     # Host name        -> Host object
        self.routers = {}   # Router name      -> Router object
        self.apps = {}      # Application name -> Host name
        self.dnsTable = {}  # Host name        -> Host IP

        self.currentTime = 0    # Time when last simulate command was executed
        self.snifferFiles = []  # List of sniffer file objects

        self.startTime = time.time()

    def start(self):
        """Starts the simulation."""
        # Process file
        self.__parseFile()

    def __createHost(self, name):
        """Creates a host with the given name."""
        # print("Host: %s" % name)
        host = Host(name)
        self.hosts[name] = host

    def __createRouter(self, name, numPorts):
        """Creates a router with the given name and number of ports.
           Also runs a thread for each router port."""
        # print("Router: %s [%d interfaces]" % (name, numInterfaces))
        router = Router(name, numPorts)
        self.routers[name] = router
        for port in range(numPorts):
            router.thread = threading.Thread(name=name + "." + str(port),
                                             target=router.runThread,
                                             args=(port,),
                                             daemon=True)
            router.thread.start()

    def __configHost(self, name, ipAddr, routerAddr, dnsAddr):
        """Configures the host's and its default router's IP.
           Also sets the DNS server's IP."""
        # print("{IP} Host %s: %s, [Router] %s, [DNS] %s" %
        #      (name, ipAddr, routerAddr, dnsAddr))
        self.hosts[name].setIp(ipAddr, routerAddr, dnsAddr)

    def __configRouter(self, name, port, ipAddr):
        """Configures the IP address of one of the router's ports."""
        # print("{IP} Router %s.%d: %s" % (name, port, ipAddr))
        self.routers[name].addPort(port, ipAddr)

    def __createDuplexLink(self, side1, side2, bandwidth, delay):
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

    def __createRoute(self, name, subnetwork, route):
        """Creates a specified route from a router to a subnetwork."""
        # print("{Route} %s -> %s:%s" % (name, subnetwork, route))
        self.routers[name].addRoute(subnetwork, route)

    def __defineTimePerformance(self, name, timeProcess):
        """Sets time to process a package for a given router."""
        # print("{Time} %s: %g us" % (name, timeProcess))
        self.routers[name].setTimePerformance(timeProcess)

    def __definePortPerformance(self, name, port, bufferSize):
        """Defines buffer size for a specified router's port."""
        # print("{Buffer} %s.%d: %g" % (name, port, bufferSize))
        self.routers[name].setBufferSize(port, bufferSize)

    def __startApplication(self, hostname, appName, appType):
        """Defines an application level protocol on the given host."""
        # print("{Application} %s: %s [%s]" % (hostname, appName, appType))
        self.apps[appName] = hostname
        host = self.hosts[hostname]
        host.addApplication(appName, appType)
        if appType == "dnss":
            host.setDnsTable(self.dnsTable)

        # Start host thread
        host.thread = threading.Thread(name=hostname,
                                       target=host.runThread,
                                       daemon=True)
        host.thread.start()

    def __createSniffer(self, name, target, outputFile):
        """Creates a sniffer between 'name' and 'target'. Information its
           shown in standard output and specified 'outputFile.'"""
        # print("{Sniffer} %s <-> %s [Output '%s']" %
        #      (name, target, outputFile))
        f = open(outputFile, 'w')
        self.snifferFiles.append(f)

        # 'pair' receives one of the two lists
        for pair in [[name, target], [target, name]]:
            # Here, 'pair' is a list with two values
            sniffer = Sniffer(pair[0], pair[1], f, self.startTime)
            checkRouter = self.__isRouter(pair[0])
            if checkRouter is not None:
                router = self.routers[checkRouter[0]]
                router.setSniffer(int(checkRouter[1]), sniffer)
            else:
                host = self.hosts[pair[0]]
                host.setSniffer(sniffer)

    def __simulateCommand(self, cmdTime, appName, command):
        """Runs 'appName' with the given command at the specified time."""
        # print("{Simulate} [t = %g] %s %s" % (cmdTime, appName, command))
        delta = cmdTime - self.currentTime
        time.sleep(delta)
        self.currentTime = cmdTime
        host = self.apps[appName]
        self.hosts[host].addSimQueue(command)

    def __finish(self, endTime):
        """Ends the simulation at the specified time."""
        # print("**FINISH [t = %g]**" % endTime)
        delta = endTime - self.currentTime
        time.sleep(delta)
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

                # Cleans whitespaces and '\n' at the end
                line = line.rstrip()

                # Ignores empty lines and comments
                if line == "" or line[0] == '#':
                    continue

                # Checks if line continues (ends with '\')
                while line[-1] == '\\':
                    line = line[0:-1]
                    nextLine = simulFile.readline().rstrip()
                    line = line + nextLine

                parts = line.split()
                self.__parseLine(parts)

    def __parseLine(self, parts):
        # Parse 'set' commands
        if parts[0] == "set":
            if parts[1] == "host":
                name = parts[2]
                self.__createHost(name)

            elif parts[1] == "router":
                name = parts[2]
                numInterfaces = int(parts[3])
                self.__createRouter(name, numInterfaces)

            elif parts[1] == "duplex-link":
                side1 = parts[2]
                side2 = parts[3]

                # Removes 'Mbps' and 'ms' at end of string before
                # converting to float
                bandwidth = float(parts[4][:-4])
                delay = float(parts[5][:-2])

                self.__createDuplexLink(side1, side2, bandwidth, delay)

            elif parts[1] == "ip":
                name = parts[2]

                try:
                    port = int(parts[3])
                    # Port conversion successful;
                    # 'name' is a router
                    for x in range(3, len(parts), 2):
                        self.__configRouter(name, int(parts[x]),
                                            parts[x+1])

                except ValueError:
                    # Port conversion raised exception;
                    # 'name' is a host
                    ipAddr = parts[3]
                    routerAddr = parts[4]
                    dnsAddr = parts[5]
                    self.__configHost(name, ipAddr, routerAddr, dnsAddr)
                    self.dnsTable[name] = ipAddr

            elif parts[1] == "route":
                routerName = parts[2]

                # Reads two arguments (subnetwork, route) at a time
                for x in range(3, len(parts), 2):
                    self.__createRoute(routerName, parts[x], parts[x+1])
                self.routers[routerName].updateRoute()

            elif parts[1] == "performance":
                name = parts[2]

                # Removes "us" at end of string before
                # converting to float
                timeProcess = float(parts[3][:-2])

                self.__defineTimePerformance(name, timeProcess)
                for x in range(4, len(parts), 2):
                    port = int(parts[x])
                    bufferSize = float(parts[x+1])
                    self.__definePortPerformance(name, port, bufferSize)

            elif parts[1] in ["ircc", "ircs", "dnss"]:
                hostname = parts[2]
                appName = parts[3]
                appType = parts[1]
                self.__startApplication(hostname, appName, appType)

            elif parts[1] == "sniffer":
                name = parts[2]
                target = parts[3]
                outputFile = parts[4]

                # Removes "" quotes from beginning and end
                outputFile = outputFile[1:-1]
                self.__createSniffer(name, target, outputFile)

        elif parts[0] == "simulate":
            cmdTime = float(parts[1])
            appName = parts[2]
            command = parts[3:]

            # Removes a " from the beginning of first string
            command[0] = command[0][1:]

            # Removes a " from the end of final string
            command[-1] = command[-1][0:-1]

            self.__simulateCommand(cmdTime, appName, command)

        elif parts[0] == "finish":
            endTime = float(parts[1])
            self.__finish(endTime)

        else:
            print("ERROR: Invalid line!\n'%s'" % line)

    def __isRouter(self, entity):
        """Returns a tuple (name, port) if the entity is a
           router, or None otherwise."""
        separate = entity.split('.')
        if len(separate) > 1:
            return (separate[0], separate[1])
        else:
            return None
