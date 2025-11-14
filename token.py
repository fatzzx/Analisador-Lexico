from typing import Optional


class Token:
    def __init__(
        self, codigo: str, lexema: str, linha: int, indice_tab: Optional[int] = None
    ) -> None:
        self.codigo = codigo
        self.lexema = lexema
        self.linha = linha
        self.indice_tab = indice_tab

    def __repr__(self) -> str:
        return f"Token(codigo={self.codigo}, lexema={self.lexema}, linha={self.linha}, indice_tab={self.indice_tab})"

palavras_reservadas = {
    "integer": "PRS01",
    "real": "PRS02",
    "character": "PRS03",
    "string": "PRS04",
    "boolean": "PRS05",
    "void": "PRS06",
    "true": "PRS07",
    "false": "PRS08",
    "varType": "PRS09",
    "funcType": "PRS10",
    "paramType": "PRS11",
    "declarations": "PRS12",
    "endDeclarations": "PRS13",
    "program": "PRS14",
    "endProgram": "PRS15",
    "functions": "PRS16",
    "endFunctions": "PRS17",
    "endFunction": "PRS18",
    "return": "PRS19",
    "if": "PRS20",
    "else": "PRS21",
    "endIf": "PRS22",
    "while": "PRS23",
    "endWhile": "PRS24",
    "break": "PRS25",
    "print": "PRS26"
}
simbolos_reservados = {
    ";": "SRS01",
    ",": "SRS02",
    ":": "SRS03",
    ":=": "SRS04",
    "?": "SRS05",
    "(": "SRS06",
    ")": "SRS07",
    "[": "SRS08",
    "]": "SRS09",
    "{": "SRS10",
    "}": "SRS11",
    "+": "SRS12",
    "-": "SRS13",
    "*": "SRS14",
    "/": "SRS15",
    "%": "SRS16",
    "==": "SRS17",
    "!=": "SRS18",
    "#": "SRS18",
    "<": "SRS19",
    "<=": "SRS20",
    ">": "SRS21",
    ">=": "SRR22"
}