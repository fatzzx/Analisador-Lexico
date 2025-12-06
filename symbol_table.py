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

    # Atualizado para receber a qtd de chars lida pelo lexer (antes da truncagem)
    # e para garantir que o lexema seja truncado a 35 (maximo para a tabela)
    def insert_symbol(
        self,
        lexema_original: str,  # o lexema que pode ter vindo maior que 35
        codigo_atomo: str,
        linha: int,
        qtd_char_antes_trunc: int,  # qtd de chars validos lidos antes do delimitador
    ) -> int:
        # Usa o lexema em caixa alta para a chave e para o armazenamento
        lexema_upper = lexema_original.upper()

        # O lexema na tabela e o truncado a 35 [cite: 279]
        lexema_truncado = lexema_upper[:35]

        # A qtd de chars depois da truncagem e o tamanho do lexema truncado
        qtd_char_depois_trunc = len(lexema_truncado)

        if lexema_truncado in self._table:
            # Controla para armazenar as 5 primeiras linhas (podem ser repetidas)
            if len(self._table[lexema_truncado]["linhas"]) < 5:
                self._table[lexema_truncado]["linhas"].append(linha)
            return self._table[lexema_truncado]["indice"]

        # Se for nova entrada
        entry = {
            "indice": self._next_index,
            "codigo": codigo_atomo,
            "lexema": lexema_truncado,
            # TipoSimb (default vazio, sera preenchido na analise sintatica) [cite: 281]
            "tipo_simb": "",
            # Qtd de chars (antes/depois da truncagem) [cite: 284, 287]
            "qtd_char_antes_trunc": qtd_char_antes_trunc,
            "qtd_char_depois_trunc": qtd_char_depois_trunc,
            # Linhas (apenas a primeira, max 5)
            "linhas": [linha],
        }
        self._table[lexema_truncado] = entry
        self._next_index += 1
        return entry["indice"]

    # Metodo para gerar o conteudo do arquivo .TAB
    def gerar_relatorio_tab(self, nome_arquivo_entrada: str, info_equipe: dict) -> str:
        # Monta o cabecalho
        relatorio = f"Codigo da Equipe: {info_equipe['codigo']}\n"
        relatorio += "Componentes:\n"
        for comp in info_equipe["componentes"]:
            relatorio += f" {comp['nome']}; {comp['email']}; ({comp['telefone']})\n"

        relatorio += f"\nRELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: {nome_arquivo_entrada}\n"

        # Monta os detalhes de cada simbolo
        # Ordena pela indice para seguir a ordem de insercao
        for key in sorted(self._table.keys(), key=lambda k: self._table[k]["indice"]):
            entry = self._table[key]

            # Formata a lista de linhas para o estilo (1, 2, 3) do exemplo
            linhas_str = ", ".join(map(str, entry["linhas"]))

            # Formato de entrada da tabela
            relatorio += (
                f"Entrada: {entry['indice']}, "
                f"Codigo: {entry['codigo']}, "
                f"Lexeme: {entry['lexema']},\n"
                f" QtdCharAntesTrunc: {entry['qtd_char_antes_trunc']}, "
                f"QtdCharDepoisTrunc: {entry['qtd_char_depois_trunc']},\n"
                f" TipoSimb: {entry['tipo_simb']}, Linhas: ({linhas_str}).\n"
            )

        return relatorio
