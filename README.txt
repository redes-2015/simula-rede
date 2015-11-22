<------ MAC0448 - Prof Daniel Batista ------>
<-- Programação para Rede de Computadores -->

Integrantes:
    - (5173890) Evandro F. Giovanini
    - (8536065) Leonardo Pereira Macedo

+---------------------------+
| EP 3 - Simulador de Redes |
+---------------------------+

LINGUAGEM ESCOLHIDA
===================

A linguagem Python foi escolhida para fazer este EP.
A versão utilizada foi Python 3.4.3.

ARQUIVOS E DIRETÓRIOS
=====================

Este EP consiste em:
  - LEIAME: Este arquivo explicatório.
  - src/: Código fonte do EP, onde o simulador de redes está implementado.
  - executa.sh: Bash script usado para executar o simulador de redes.
  - slides.pdf: Slides para a apresentação, conforme solicitado no enunciado.

Além disso, há um diretório 'data/' dentro do 'src/' contendo arquivos de
entrada, incluindo os que foram usados como testes para os slides.

USO
===

Para executar o simulador, basta digitar no root do projeto:

$ ./executa.sh <arquivo de entrada>

O simulador será rodado usando o arquivo dado como argumento.
Este arquivo deve estar de acordo com as especificações do enunciado do EP.

Para maiores informações sobre o script que executa o simulador,
digite no root do projeto:

$ ./executa.sh -h

FUNCIONAMENTO
=============

O simulador agirá de acordo com as instruções contidas no arquivo de entrada.
Não é possível controlá-lo diretamente durante a simulação.

A saída do programa é definida pelos sniffers configurados no arquivo de
entrada: todos os pacotes que passem por onde um sniffer está monitorando
terão seus dados impressos na saída padrão e num arquivo ligado ao sniffer.

Abaixo estão exemplos de saída para os dois tipos de pacotes que podem
ser capturados, juntamente com informações sobre o que cada linha da saída
representa na simulação.

1) Pacote com protocolos IP, TCP e IRC.

{h2 #1}                    ID único do pacote
t = 0.5610s                Instante em que o pacote foi visto
r1.0 -> r0.2               Onde o pacote foi capturado (local do sniffer)
>>>> IP                    Informações sobre o protocolo IP
  To:   10.0.0.1           IP de destino
  From: 192.168.2.2        IP de origem
  Transport Protocol: 6    Código da camada de transporte
  Size: 44                 Tamanho: cabeçalho IP + camadas superiores
  TTL: 63                  Valor do "Time to Live"
>>>> TCP                   Informações sobre o protocolo TCP
  To:   14902              Porta de destino
  From:  6667              Porta de origem
  Seq Number:   0          Número de sequência
  Ack Number:   1          Número de reconhecimento
  [ACK] [SYN]              Indica bits ligados: ACK, FIN, SYN
>>>> IRC                   Informação sobre o protocolo IRC
  Message: ""              Pergunta/resposta (entre aspas)

2) Pacote com protocolos IP, UDP e DNS.

{h0 #1}                    Daqui até o final de IP, o tipo
t = 0.5501s                de informação é igual ao exemplo 1
r0.2 -> r1.0
>>>> IP
  To:   192.168.1.1
  From: 10.0.0.1
  Transport Protocol: 17
  Size: 30
  TTL: 63
>>>> UDP                   Informações sobre o protocolo UDP
  To:      53              Porta de destino
  From:  2000              Porta de origem
  Size: 10                 Tamanho: cabeçalho UDP + camada superior
>>>> DNS                   Informação sobre o protocolo DNS
  Message: "h2"            Pergunta/resposta (entre aspas)

OBSERVAÇÕES
===========

O simulador supõe que o arquivo de entrada possui os comandos na
mesma ordem que foram dados no exemplo do enunciado do EP 3, e que
não haverá erros em relação a nome de hosts e roteadores, definição
de rotas, mudanças nas unidades de medida de tempo e envio, etc.

Supõe-se, também, que os comandos do cliente IRC estejam corretos,
ou seja, o cliente não tentará definir um nickname inválido ou
usar um QUIT antes de um CONNECT, por exemplo.

Ao executar o comando "finish", a simulação imediatamente termina,
independente de dados estarem circulando ou não pelos hosts e
roteadores.
