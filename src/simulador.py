

"""Cria e executa a simulação a partir do arquivo"""
class Simulador:

    def __init__(self, entrada):
        self.entrada = entrada

    def criarComputador(nome):
        print ("TODO: criando computador de nome " + nome)

    def criarRoteador (nome, numInterfaces):
        print ("TODO: criando roteador de nome " + nome + " com " + numInterfaces + " interfaces.")

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
                        self.criarComputador (nome)

                    elif msg[1] == 'router':
                        nome = msg[2]
                        numInterfaces = msg[3]
                        self.criarRoteador (numInterfaces)

                    else:
                        print(linha)

                # processa comando simulate

                # processa comando finish
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

