"""Representa um cliente IRC na simulação de rede."""

# -------------------------------------------------------------


class IrcCliente:

    def __init__(self):
        """Inicializa o socket de escuta do servidor IRC."""
        self.socket = None
        self.ip = None
        self.port = None

        # Comandos parseados no cliente
        self.CONNECT = "CONNECT"

    def envia(self, msg):
        """Loop infinito do servidor IRC."""
        separa = msg.split(' ')
        if separa[0] == "CONNECT":
            pass  # TODO: Criar socket TCP e se conectar ao servidor IRC
        else:
            pass  # TODO: Enviar msg pelo socket
        # TODO: Receber resposta do servidor
