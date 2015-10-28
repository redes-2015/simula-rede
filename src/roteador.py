"""Representação de um roteador na simulação de rede."""

# -------------------------------------------------------------


class Roteador:

    def __init__(self, nome, numInterfaces):
        """Inicializa o roteador com um nome e o número de interfaces."""
        self.nome = nome
        self.numInterfaces = numInterfaces

        # Inicializa atributos vazios
        self.tempoProc = None
        self.interfaces = {}
        self.rotas = {}
        self.tamBuffers = {}

    def adicionaPorta(self, porta, ip):
        """Adiciona uma nova porta, com seu respectivo ip, ao roteador."""
        self.interfaces[porta] = ip

    def adicionaRota(self, rede, porta):
        """Configura uma nova rota para a rede especificada numa dada
           porta do roteador."""
        self.rotas[rede] = porta

    def setTamanhoBuffer(self, porta, tamanho):
        """Define o tamanho do buffer para a porta indicada."""
        self.tamBuffers[porta] = tamanho

    def setTempoProcessa(self, tempoProc):
        """Define o tempo para processar um pacote."""
        self.tempoProc = tempoProc

    def executa(self):
        """Loop infinito do roteador. Recebe e trata pacotes."""
        while True:
            pass
