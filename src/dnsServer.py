"""Represents a DNS server on the network simulation."""

from udpSegment import UdpSegment
from ipDatagram import IpDatagram

# -------------------------------------------------------------


class DnsServer:

    def __init__(self, serverIp):
        """Initializes the DNS server with the host's IP."""
        self.port = 53  # Default DNS port
        self.serverIp = serverIp
        self.dnsTable = None

    def setDnsTable(self, dnsTable):
        """Defines the DNS table for a DNS server application."""
        self.dnsTable = dnsTable

    def receive(self, packet):
        """Receives a packet asking for the IP of a name address.
           Returns a packet with the desired IP."""
        if self.dnsTable is None:
            raise Exception("DNS table not defined in the server!")

        name = packet.getSegment().getMessage()
        ip = self.dnsTable[name]

        segment = UdpSegment(name + ',' + ip, self.port,
                             packet.getSegment().getOriginPort())
        datagram = IpDatagram(segment, self.serverIp, packet.getOriginIp())
        return datagram
