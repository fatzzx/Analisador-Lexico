palavras_reservadas = {
    "integer": "PRS01",
    "real": "PRS02",
    "character": "PRS03",
    "string": "PRS04",
    "boolean": "PRS05",
    "void": "PRS06",
    "true": "PRS07",
    "false": "PRS08",
    "vartype": "PRS09",
    "functype": "PRS10",
    "paramtype": "PRS11",
    "declarations": "PRS12",
    "enddeclarations": "PRS13",
    "program": "PRS14",
    "endprogram": "PRS15",
    "functions": "PRS16",
    "endfunctions": "PRS17",
    "endfunction": "PRS18",
    "return": "PRS19",
    "if": "PRS20",
    "else": "PRS21",
    "endif": "PRS22",
    "while": "PRS23",
    "endwhile": "PRS24",
    "break": "PRS25",
    "print": "PRS26",
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
    ">=": "SRS22",
}


class SymbolTable:
    def __init__(self):
        self._table = {}
        self._next_index = 1

    def insert_symbol(self, lexema: str, codigo_atomo: str, linha: int) -> int:
        lexema_upper = lexema.upper()

        lexema_truncado = lexema_upper[:35]

        if lexema_truncado in self._table:
            if linha not in self._table[lexema_truncado]["linhas"]:
                self._table[lexema_truncado]["linhas"].append(linha)
            return self._table[lexema_truncado]["indice"]

        entry = {
            "indice": self._next_index,
            "codigo": codigo_atomo,
            "lexema": lexema_truncado,
            "linhas": [linha],
        }
        self._table[lexema_truncado] = entry
        self._next_index += 1
        return entry["indice"]
