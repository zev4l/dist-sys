"""
Aplicações distribuídas - Projeto 2 - color_utils.py
Grupo: 77
Números de aluno: 55373, 55371
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


def color(content, command = None):
    """
    Processa um pedido/resposta atribuindo as cores respetivas aos substrings 
    LOCKED, UNLOCKED, DISABLED, UNKNOWN RESOURCE, NOK e OK ou aos objetos nativos
    True, False, None e Ellipsis.
    Requires: content é uma lista. command é PRINT ou STATUS
    """

    elem = 0

    while elem < len(content):



        if str(content[elem]) in ('NOK', 'UNKNOWN RESOURCE', 'False', 'None'):
            content[elem] = colorWrite(str(content[elem]), 'red')
        elif str(content[elem]) in ('OK', 'True'):
            content[elem] = colorWrite(str(content[elem]), 'green')

        if command in ("PRINT", "STATUS"):
            # Uso de Regular Expressions para alterar ocorrências de 
            # palavras para sua versão colorida.
            content[elem] = re.sub(r"\bLOCKED\b", colorWrite("LOCKED", "red"), str(content[elem]))
            content[elem] = re.sub(r"\bUNLOCKED\b", colorWrite("UNLOCKED", "green"), str(content[elem]))
            content[elem] = re.sub(r"\bEllipsis\b", colorWrite("Ellipsis", "bk_red"), str(content[elem]))
            content[elem] = re.sub(r"\bDISABLED\b", colorWrite("DISABLED", "bk_red"), str(content[elem]))
        
        elem += 1

    return content