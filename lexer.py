from symbol_table import SymbolTable, palavras_reservadas, simbolos_reservados
from token_class import TokenClass


class Lexer:
    def __init__(self, texto: str, tabela_simbolos: SymbolTable):
        self.texto = texto
        self.tabela_simbolos = tabela_simbolos
        # pos atual do cursor
        self.pos = -1
        # contador de linas para mensagem de erro
        self.linha = 1
        self.char_atual = None
        self.prox()  # Joguei essa funcao aqui para já le o primeiro char quando iniciar

    # Esse metodo so avanca o cursor para o proximo char e verifica se é o ultimo
    def prox(self):
        self.pos += 1
        if self.pos < len(self.texto):
            self.char_atual = self.texto[self.pos]
        else:
            self.char_atual = None

    # esse metodo so ve o proximo char, para alguns casos expecificos como o de < <=
    def proximo_char(self):
        prox_pos = self.pos + 1
        if prox_pos < len(self.texto):
            return self.texto[prox_pos]
        return None

    # Metodo para pular comentarios // e /*   */
    def pular_comentario(self):
        prox_char = self.proximo_char()
        # aq verifica para o caso de //
        if prox_char == "/":
            self.prox()  # pula a primeira /
            self.prox()  # pula a segunda /
            # Pula tudo tudo ate o final da linha
            while self.char_atual is not None and self.char_atual != "\n":
                self.prox()
            return True
        # aq verifica para o caso de /* */
        elif prox_char == "*":
            self.prox()  # pula a primeira /
            self.prox()  # pula o *
            # pula ate encontrar o */
            while self.char_atual is not None:
                if self.char_atual == "\n":
                    self.linha += 1
                if self.char_atual == "*" and self.proximo_char() == "/":
                    self.prox()
                    self.prox()
                    return True
                self.prox()
            return True  # se chegar aq eh pq realmente era um comentario
        return False  # aq ele é uma divisao normal

    # metodo para processar numeros reais ou inteiros
    def fazer_numero(self):
        num_str = ""
        tem_ponto = False
        # le a parte inteira
        while self.char_atual is not None and self.char_atual.isdigit():
            num_str += self.char_atual
            self.prox()
        # aq ele ve se tem parte decimal
        if self.char_atual == ".":
            tem_ponto = True
            num_str += "."
            self.prox()
            # le a parte decimal
            while self.char_atual is not None and self.char_atual.isdigit():
                num_str += self.char_atual
                self.prox()
        if tem_ponto:
            return TokenClass("IDN05", num_str, self.linha)
        else:
            return TokenClass("IDN04", num_str, self.linha)

    # metodo pra intentificador e palavras reservadas
    def fazer_identificador(self):
        id_str = ""
        # vai juntandos os char de alfanumericos
        while self.char_atual is not None and (
            self.char_atual.isalnum() or self.char_atual == "_"
        ):
            id_str += self.char_atual
            self.prox()

        # Aq é pq eh case insensitive pra pravras reservadas
        id_lower = id_str.lower()

        # identifica se eh palabra reservada
        if id_lower in palavras_reservadas:
            codigo = palavras_reservadas[id_lower]
            return TokenClass(codigo, id_str, self.linha)

        # senao é um identificador normal
        codigo_idn = "IDN02"
        # aq joga na tabela de simbolos
        indice = self.tabela_simbolos.insert_symbol(id_str, codigo_idn, self.linha)

        return TokenClass(codigo_idn, id_str, self.linha, indice_tab=indice)

    # processa strings
    def fazer_string(self):
        string_val = '"'
        self.prox()  # pula aspas iniciais
        while self.char_atual is not None and self.char_atual != '"':
            # trata quebra de linha dentro de strings
            if self.char_atual == "\n":
                self.linha += 1
            string_val += self.char_atual
            self.prox()
        if self.char_atual == '"':
            string_val += '"'
            self.prox()  # pula as aspas de fechamento
        return TokenClass("IDN06", string_val, self.linha)

    # aq eh o principar q le char por char do arquivo e gera todos os tokens
    def gerarTokens(self):
        tokens = []
        # ignora espaco em branco e tabulacao
        while self.char_atual is not None:
            if self.char_atual in " \t":
                self.prox()
            # quebra de linha
            elif self.char_atual == "\n":
                self.linha += 1
                self.prox()
            # trara barra pode ser comentario ou divisao
            elif self.char_atual == "/":
                if self.pular_comentario():
                    continue  # sendo comentario volta pro inicio
                else:
                    # se n for comentario eh divisao
                    tokens.append(TokenClass(simbolos_reservados["/"], "/", self.linha))
                    self.prox()
            # trata os numeros
            elif self.char_atual.isdigit():
                tokens.append(self.fazer_numero())
            # trata identificadores e palabras reservadas
            elif self.char_atual.isalpha() or self.char_atual == "_":
                tokens.append(self.fazer_identificador())
            # strings
            elif self.char_atual == '"':
                tokens.append(self.fazer_string())
            # simbolos, operadores
            else:
                char_simples = self.char_atual
                # aq tenta formar simbolos compostos como <=
                char_composto = char_simples + (self.proximo_char() or "")

                # verifica se o simbolo composto existe
                if char_composto in simbolos_reservados:
                    tokens.append(
                        TokenClass(
                            simbolos_reservados[char_composto],
                            char_composto,
                            self.linha,
                        )
                    )
                    self.prox()  # come o 1 char
                    self.prox()  # come o 2 char
                # se n eh composo trata como simples
                elif char_simples in simbolos_reservados:
                    tokens.append(
                        TokenClass(
                            simbolos_reservados[char_simples], char_simples, self.linha
                        )
                    )
                    self.prox()
                # desconhecido aq
                else:
                    self.prox()
        # tenho que ver se eh necessario mesmo
        tokens.append(TokenClass("EOF", "EOF", self.linha))
        return tokens
