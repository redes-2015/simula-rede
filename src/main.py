#!/usr/bin/env python3

"""Módulo principal.
   Verificação dos argumentos por linha de comando."""

from simulador import Simulador
import sys

# -------------------------------------------------------------

try:
    simulador = Simulador(sys.argv[1])
    simulador.inicia()
except IndexError:
    print("Arquivo de simulação não especificado!")
except FileNotFoundError:
    print("Arquivo de simulação '%s' não encontrado!" % sys.argv[1])
