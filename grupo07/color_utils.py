import re

def colorWrite(text, color):
    """
    Devolve o texto recebido na cor especificada.
    Requires: text é um string e color é 'green' ou 'red'.
    Ensures: text rodeado pelos códigos de cor referentes à 
    cor especificada.
    """

    RED_START = '\033[91m'
    GREEN_START = '\033[92m'
    COLOR_END = '\033[0m'
    BK_RED = '\u001b[41m'


    if color == "green":
        return GREEN_START + str(text) + COLOR_END
    
    if color == "red":
        return RED_START + str(text) + COLOR_END
    
    if color == "bk_red":
        return BK_RED + str(text) + COLOR_END


def color(content, command = None):
    if content in ('NOK', 'UNKNOWN RESOURCE'):
        content = colorWrite(content, 'red')
    elif content == 'OK':
        content = colorWrite(content, 'green')

    if command == "PRINT":
        content = re.sub(r"\bLOCKED\b", colorWrite("LOCKED", "red"), content)
        content = re.sub(r"\bUNLOCKED\b", colorWrite("UNLOCKED", "green"), content)
        content = re.sub(r"\bDISABLED\b", colorWrite("DISABLED", "bk_red"), content)

    return content