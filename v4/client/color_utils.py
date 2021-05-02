"""
Aplicações distribuídas - Projeto 4 - color_utils.py
Grupo: 77
Alunos: José Almeida - 55373, Augusto Gouveia - 55371
"""

import re

def colorWrite(text, color):
    """
    Devolve o texto recebido na cor especificada.
    Requires: text é um string e color é 'green', 'red' ou 'bk_red'.
    Ensures: text rodeado pelos códigos de cor referentes à
    cor especificada.
    """

    RED_START = '\033[91m'
    GREEN_START = '\033[92m'
    BLUE_START = '\u001b[34m'
    COLOR_END = '\033[0m'
    BK_RED = '\u001b[41m'


    if color == "green":
        return GREEN_START + str(text) + COLOR_END

    if color == "red":
        return RED_START + str(text) + COLOR_END

    if color == "blue":
        return BLUE_START + str(text) + COLOR_END

    if color == "bk_red":
        return BK_RED + str(text) + COLOR_END
