"""Representa um servidor IRC na simulação de rede."""

# Comandos válidos no servidor
CONNECT = "CONNECT"
USER = "USER"
QUIT = "QUIT"

# -------------------------------------------------------------


class IrcServidor:

    def __init__(self):
        """Inicializa o socket de escuta do servidor IRC."""
        # Porta padrão do IRC
        self.porta = 6667

        # Dicionário 'IP:Porta -> Username' dos clientes conectados
        self.conectados = {}

        # TODO: "Criar socket de escuta e dar bind"

    def executa(self):
        """Loop infinito do servidor IRC."""
        while True:
            # TODO: "Checar sockets para novas conexões ou mensagens"

    def parseMsg(self, endereco, msg):
        """Interpreta a mensagem enviada por um cliente."""
        enderecoStr = endereco[0] + ':' + endereco[1]

        msg = msg.rstrip('\r\n')
        msg = msg.rstrip(' ')
        separa = msg.split(' ')

        if separa[0] == CONNECT:
            resposta = "Conexão feita!\r\n"
            self.conectados[enderecoStr] = None

        elif separa[0] == USER:
            # Verifica se username já existe
            username = separa[1]
            if username in self.conectados.values():
                resposta = "Username '" + username + "' já existente!"
            else:
                self.conectados[enderecoStr] = username
                resposta = "Username '" + username + "' definido com sucesso!"

        elif separa[0] == QUIT:
            # O 'None' é o valor de retorno em caso da chave não existir
            self.conectados.pop(enderecoStr, None)

        return resposta
