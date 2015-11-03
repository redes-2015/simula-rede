"""Representação de um computador (host) na simulação de rede."""

# -------------------------------------------------------------


class Computador:

    def __init__(self, nome):
        """Inicializa um computador com seu nome e endereço IP."""
        self.nome = nome
        self.ipComp = self.ipRoteador = self.ipDns = None
        # TODO: Ver se vale a pena colocar aplicação dentro do computador
        # self.aplicacao = None

    def setIp(self, ipComp, ipRoteador, ipDns):
        """Define atributos da configuração de IP do computador."""
        self.ipComp = ipComp
        self.ipRoteador = ipRoteador
        self.ipDns = ipDns
