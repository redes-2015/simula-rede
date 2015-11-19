"""Represents a DNS server on the network simulation."""

from udpSegment import UDPSegment
from ipDatagram import IPDatagram

# -------------------------------------------------------------


class DnsServer:

    def __init__(self, serverIP):
        """Initializes the DNS server with the host's IP."""
        self.port = 53  # Default DNS port
        self.serverIP = serverIP
        self.dnsTable = None

    def setDnsTable(self, dnsTable):
        """Defines the DNS table for a DNS server application."""
        self.dnsTable = dnsTable

    def receive(self, packet):
        """Receives a packet asking for the IP of a name address.
           Returns a packet with the desired IP."""
        name = packet.getSegment().getMessage()
        ip = self.dnsTable[name]

        segment = UDPSegment(name + ',' + ip, self.port, packet.getSegment().getOrigin())
        datagram = IPDatagram(self.serverIP, packet.getOriginIP(), segment)
        return datagram
