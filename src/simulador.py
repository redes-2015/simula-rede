#!/usr/bin/env python3

from computador import Computador
from roteador import Roteador

"""Cria e executa a simulação a partir do arquivo"""
class Simulador:

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.dict_computador = {}
        self.dict_roteador = {}

    def criarComputador(self, nome):
        print ("Criando computador de nome " + nome)
        computador = Computador(nome)
        self.dict_computador[nome] = computador

    def criarRoteador(self, nome, numInterfaces):
        print ("Criando roteador de nome " + nome + " com " + numInterfaces + " interfaces.")
        roteador = Roteador(nome, numInterfaces)
        self.dict_roteador[nome] = roteador

    def configuraComputador(self, nome, enderecoIp, enderecoRoteador, enderecoDNS):
        print("Configurando computador de nome", nome + ":", enderecoIp, enderecoRoteador, enderecoDNS)
        self.dict_computador[nome].setIp(enderecoIp, enderecoRoteador, enderecoDNS)

    def configuraRoteador(self, nome, porta, enderecoIp):
        print("Configurando roteador de nome", nome + ":", porta, "->", enderecoIp)
        self.dict_roteador[nome].adicionaPorta(porta, enderecoIp)

    def criarDuplexLink(self, lado1, lado2, banda, atraso):
        print ("Criando duplex link entre " + lado1 + " e " + lado2 + ": " + banda + ", " + atraso)

    def criarRota(self, nome, subrede, rota):
        print ("Criando rota no roteador " + nome + " para a rede " + subrede + " : " + rota)
        self.dict_roteador[nome].adicionaRota(subrede, rota)

    def definePerformanceTempo(self, nome, tempo):
        print ("Performance do roteador " + nome + " com tempo: " + tempo)
        self.dict_roteador[nome].setTempoProcessa(tempo)

    def definePerformancePorta(self, nome, porta, tamanhoPorta):
        print ("Tamanho do buffer do roteador " + nome + " na porta " + porta)
        self.dict_roteador[nome].setTamanhoBuffer(porta, tamanhoPorta)

    def iniciaAplicacao(self, nomeComputador, nomeAplicacao, tipo):
        print ("Inicia aplicacao " + nomeAplicacao + " do tipo " + tipo + " em " + nomeComputador)

    def criarSniffer(self, nome, monitorando, saida):
        print ("Iniciando sniffer de " + nome + " em " + monitorando + ". Saída: " + saida)

    def simularComando(self, tempo, nomeAplicacao, comando):
        print ("Simulando " + nomeAplicacao + " no instante " + tempo + " com o comando: " + comando[0])

    def encerrar(self, tempo):
        print ("Encerrar a " + tempo)

    def processaEntrada(self):
        with open(self.nomeArquivo, 'r') as arquivo:
            while True:
                linha = arquivo.readline()

                # Verifica EOF
                if linha == "":
                    break

                # Limpa espaços e '\n' no final
                linha = linha.rstrip()

                # Ignora linhas vazias e comentários
                if linha == "" or linha[0] == '#':
                    continue

                # Verifica se a linha tem continuação
                while linha[-1] == '\\':
                    linha = linha[0:-1]
                    proximaLinha = arquivo.readline().rstrip()
                    linha = linha + proximaLinha

                msg = linha.split()

                # processa comandos 'set'
                if msg[0] == 'set':
                    if msg[1] == 'host':
                        nome = msg[2]
                        self.criarComputador(nome)

                    elif msg[1] == 'router':
                        nome = msg[2]
                        numInterfaces = msg[3]
                        self.criarRoteador(nome, numInterfaces)

                    elif msg[1] == 'duplex-link':
                        lado1 = msg[2]
                        lado2 = msg[3]
                        banda = msg[4]
                        atraso = msg[5]
                        self.criarDuplexLink(lado1, lado2, banda, atraso)

                    elif msg[1] == 'ip':
                        nome = msg[2]

                        try:
                            porta = int(msg[3])
                            for x in range(3, len(msg), 2):
                                self.configuraRoteador(nome, msg[x], msg[x+1])

                        except ValueError:
                            enderecoIp = msg[3]
                            enderecoRoteador = msg[4]
                            enderecoDNS = msg[5]
                            self.configuraComputador(nome, enderecoIp, enderecoRoteador, enderecoDNS)

                    elif msg[1] == 'route':
                        nomeRoteador = msg[2]

                        # Ler os argumentos, pulando 'set route nomeRoteador'
                        # cada rota é um par de argumentos, ler com step = 2
                        for x in range(3, len(msg), 2):
                            self.criarRota(nomeRoteador, msg[x], msg[x+1])

                    elif msg[1] == 'performance':
                        nome = msg[2]
                        tempo = msg[3]
                        self.definePerformanceTempo(nome, tempo)
                        for x in range(4, len(msg),2):
                            porta = msg[x]
                            tamanhoPorta = msg[x+1]
                            self.definePerformancePorta(nome, porta, tamanhoPorta)

                    elif msg[1] == 'ircc' or msg[1] == 'ircs' or msg[1] == 'dnss':
                        nomeComputador = msg[2]
                        nomeAplicacao = msg[3]
                        tipoAplicacao = msg[1]
                        self.iniciaAplicacao(nomeComputador, nomeAplicacao, tipoAplicacao)

                    elif msg[1] == 'sniffer':
                        nome = msg[2]
                        monitorando = msg[3]
                        saida = msg[4]
                        self.criarSniffer(nome, monitorando, saida)

                elif msg[0] == 'simulate':
                    tempo = msg[1]
                    nomeAplicacao = msg[2]
                    comando = msg[3:]

                    # Tira o " do início da primeira string
                    comando[0] = comando[0][1:]

                    # Tira o " do final da última string
                    comando[-1] = comando[-1][0:-1]

                    self.simularComando(tempo, nomeAplicacao, comando)

                elif msg[0] == 'finish':
                    tempo = msg[1]
                    self.encerrar(tempo)

                else:
                    print (linha)

    def inicia(self):
        self.processaEntrada()
        # proximos passos...


def main():
    sim = Simulador('entrada.txt')
    sim.inicia()

if __name__ == "__main__":
    main()

