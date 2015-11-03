

"""Cria e executa a simulação a partir do arquivo"""
class Simulador:

    def __init__(self, entrada):
        self.entrada = entrada

    def criarComputador(self, nome):
        print ("Criando computador de nome " + nome)

    def criarRoteador (self, nome, numInterfaces):
        print ("Criando roteador de nome " + nome + " com " + numInterfaces + " interfaces.")

    def criarDuplexLink (self, lado1, lado2, banda, atraso):
        print ("Criando duplex link entre " + lado1 + " e " + lado2 + ": " + banda + ", " + atraso)

    def criarRota(self, nome, subrede, rota):
        print ("Criando rota no roteador " + nome + " para a rede " + subrede + " : " + rota)

    def definePerformance(self, nome, tempo, porta, tamanhoPorta):
        print ("Performance do roteador " + nome)

    def iniciaAplicacao(self, nomeComputador, nomeAplicacao, tipo):
        print ("Inicia aplicacao " + nomeAplicacao + " do tipo " + tipo + " em " + nomeComputador)

    def criarSniffer(self, nome, monitorando, saida):
        print ("Iniciando sniffer de " + nome + " em " + monitorando + ". Saída: " + saida)

    def simularComando(self, tempo, nomeAplicacao, comando):
        print ("Simulando " + nomeAplicacao + " no instante " + tempo + " com o comando: " + comando)

    def encerrar(self, tempo):
        print ("Encerrar a " + tempo)

    def processaEntrada(self):
        for linha in self.entrada:
            # ignorar comentários
            if linha[0] == '#':
                continue

            msg = linha.split()

            try:
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
                        #TODO : distinguir 'set ip' de computadores e roteadores
                        # pelo numero de argumentos. abaixo funciona para computadores
                        nome = msg[2]
                        enderecoIp = msg[3]
                        enderecoRoteador = msg[4]
                        enderecoDNS = msg[5]
                        self.configuraComputador (nome, enderecoIp, enderecoRoteador, enderecoDNS)

                    elif msg[1] == 'route':
                        nomeRoteador = msg[2]

                        # ler os argumentos, pulando 'set route nomeRoteador'
                        # cada rota é um par de argumentos, ler com step = 2
                        for x in range(3, len(msg), 2):
                            self.criarRota (nomeRoteador, msg[x], msg[x+1])

                    elif msg[1] == 'performance':
                        nome = msg[2]
                        tempo = msg[3]
                        for x in range(4, len(msg),2):
                            porta = msg[x]
                            tamanhoPorta = msg[x+1]
                            self.definePerformance(nome, tempo, porta, tamanhoPorta)

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
                    comando = msg[3]
                    self.simularComando(tempo, nomeAplicacao, comando)

                elif msg[0] == 'finish':
                    tempo = msg[1]
                    self.encerrar(tempo)

                else:
                    print (linha)
            except:
                pass

        self.entrada.close()

    def inicia(self):
        self.processaEntrada()
        # proximos passos...


def main():
    arquivo = open('entrada.txt', 'r')
    sim = Simulador(arquivo)
    sim.inicia()

if __name__ == "__main__":
    main()

