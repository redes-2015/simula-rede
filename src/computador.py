"""Representação de um computador (host) na simulação de rede."""

# -------------------------------------------------------------

import time

class Computador:

    def __init__(self, nome):
        """Inicializa um computador com seu nome e endereço IP."""
        self.nome = nome
        self.ipComp = self.ipRoteador = self.ipDns = self.thread = None
        # TODO: Ver se vale a pena colocar aplicação dentro do computador
        # self.aplicacao = None

    def setIp(self, ipComp, ipRoteador, ipDns):
        """Define atributos da configuração de IP do computador."""
        self.ipComp = ipComp
        self.ipRoteador = ipRoteador
        self.ipDns = ipDns

    def funcThread(self):
        while(True):
            print("O computador", self.nome, "está rodando")
            time.sleep(5)
