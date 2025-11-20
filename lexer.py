from token_class import Token

from symbol_table import palavras_reservadas, simbolos_reservados, SymbolTable

class Lexer:
    def __init__(self, texto: str, tabela_simbolos: SymbolTable):
        self.texto = texto
        self.tabela_simbolos = tabela_simbolos
        self.pos = -1
        self.linha = 1 
        self.char_atual = None
        self.prox()

    def prox(self):
        self.pos += 1
        if self.pos < len(self.texto):
            self.char_atual = self.texto[self.pos]
        else:
            self.char_atual = None

    def proximo_char(self):
        prox_pos = self.pos + 1
        if prox_pos < len(self.texto):
            return self.texto[prox_pos]
        return None

    def pular_comentario(self):
        prox_char = self.proximo_char()
        if prox_char == '/':  
            self.prox() # consome /
            self.prox() # consome /
            while self.char_atual is not None and self.char_atual != '\n':
                self.prox()
            return True
        elif prox_char == '*': 
            self.prox() # consome /
            self.prox() # consome *
            while self.char_atual is not None:
                if self.char_atual == '\n':
                    self.linha += 1
                if self.char_atual == '*' and self.proximo_char() == '/':
                    self.prox() # consome *
                    self.prox() # consome /
                    return True
                self.prox()
            return True 
        return False

    def fazer_numero(self):
        num_str = ''
        tem_ponto = False
        while self.char_atual is not None and self.char_atual.isdigit():
            num_str += self.char_atual
            self.prox()
        if self.char_atual == '.':
            tem_ponto = True
            num_str += '.'
            self.prox()
            while self.char_atual is not None and self.char_atual.isdigit():
                num_str += self.char_atual
                self.prox()
        if tem_ponto:
            return Token('IDN05', num_str, self.linha) 
        else:
            return Token('IDN04', num_str, self.linha)

    def fazer_identificador(self):
        id_str = ''
        while self.char_atual is not None and (self.char_atual.isalnum() or self.char_atual == '_'):
            id_str += self.char_atual
            self.prox()

        # CORREÇÃO: Converter para minúsculo para buscar no dicionário de palavras reservadas
        id_lower = id_str.lower()

        if id_lower in palavras_reservadas:
            codigo = palavras_reservadas[id_lower]
            # Retorna o lexema original, mas com o código correto
            return Token(codigo, id_str, self.linha)
        
        # Se não é palavra reservada, é identificador (IDN02)
        codigo_idn = "IDN02" 
        # A tabela de símbolos cuida da truncagem e do maiúsculo internamente
        indice = self.tabela_simbolos.insert_symbol(id_str, codigo_idn, self.linha)
        
        return Token(codigo_idn, id_str, self.linha, indice_tab=indice)

    def fazer_string(self):
        string_val = '"'
        self.prox() 
        while self.char_atual is not None and self.char_atual != '"':
            if self.char_atual == '\n':
                self.linha += 1
            string_val += self.char_atual
            self.prox()
        if self.char_atual == '"':
            string_val += '"'
            self.prox() 
        return Token('IDN06', string_val, self.linha)

    def gerarTokens(self):
        tokens = []
        while self.char_atual is not None:
            if self.char_atual in ' \t':
                self.prox()
            elif self.char_atual == '\n':
                self.linha += 1
                self.prox()
            elif self.char_atual == '/':
                if self.pular_comentario():
                    continue 
                else:
                    tokens.append(Token(simbolos_reservados['/'], '/', self.linha))
                    self.prox()
            elif self.char_atual.isdigit():
                tokens.append(self.fazer_numero())
            elif self.char_atual.isalpha() or self.char_atual == '_':
                tokens.append(self.fazer_identificador())
            elif self.char_atual == '"':
                tokens.append(self.fazer_string())
            else:
                char_simples = self.char_atual
                char_composto = char_simples + (self.proximo_char() or '')

                if char_composto in simbolos_reservados:
                    tokens.append(Token(simbolos_reservados[char_composto], char_composto, self.linha))
                    self.prox()
                    self.prox()
                elif char_simples in simbolos_reservados:
                    tokens.append(Token(simbolos_reservados[char_simples], char_simples, self.linha))
                    self.prox()
                else:
                    self.prox()
        
        tokens.append(Token("EOF", "EOF", self.linha))
        return tokens