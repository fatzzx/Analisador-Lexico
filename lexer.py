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

    # Metodo para pular comentarios // e /* */
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
            # Se chegar ao final do arquivo sem fechar o comentario, ele eh valido
            return True
        return False  # aq ele é uma divisao normal

    # metodo para processar numeros reais ou inteiros
    def fazer_numero(self):
        num_str = ""
        tem_ponto = False
        qtd_char_lidos = 0  # Conta caracteres validos para a Tabela de Simbolos

        # O loop agora precisa checar se é um caractere válido de número, um delimitador, ou um inválido
        while self.char_atual is not None:
            char = self.char_atual

            # 1. Caracteres que fazem parte do padrao (digito, ponto, exponencial)
            if char.isdigit():
                if qtd_char_lidos < 32:
                    num_str += char
                qtd_char_lidos += 1
                self.prox()

            elif char == ".":
                prox_char = self.proximo_char()  # Armazena o proximo char

                # Le o ponto apenas se for a primeira vez, NAO for None e for seguido por digito
                if not tem_ponto and prox_char is not None and prox_char.isdigit():
                    if qtd_char_lidos < 32:
                        tem_ponto = True
                        num_str += "."
                    qtd_char_lidos += 1
                    self.prox()
                else:
                    break  # Ponto é um delimitador se ja tinha um, se nao ha proximo char ou se nao e seguido por digito

            # Tratamento da parte exponencial
            elif char.lower() == "e":
                prox_char = self.proximo_char()

                # Checa se o proximo é um digito ou um sinal (+/-) seguido de digito
                if prox_char is not None and (
                    prox_char.isdigit() or prox_char in ("+", "-")
                ):
                    tem_ponto = True  # Um numero com 'e' eh sempre real

                    # Se ja passou da parte de digitos/ponto, le o 'e' (ou 'E')
                    if qtd_char_lidos < 32:
                        num_str += char
                    qtd_char_lidos += 1
                    self.prox()

                    # le o sinal (se existir)
                    if self.char_atual in ("+", "-"):
                        if qtd_char_lidos < 32:
                            num_str += self.char_atual
                        qtd_char_lidos += 1
                        self.prox()

                    # le os digitos do expoente
                    while self.char_atual is not None and self.char_atual.isdigit():
                        if qtd_char_lidos < 32:
                            num_str += self.char_atual
                        qtd_char_lidos += 1
                        self.prox()

                    break  # Terminou de ler a parte exponencial
                else:
                    break  # 'e' nao eh seguido de um exponencial valido (pode ser um ID)

            # 2. Caracteres que são delimitadores (VALIDOS)
            elif (
                char in " \t\n"
                or char in simbolos_reservados
                or char == '"'
                or char == "/"
            ):
                break  # Delimitador encontrado, para de formar o atomo

            # 3. O que sobrar é um Caractere INVALDO (ex: '@', '$', '!')
            else:
                # FILTRA E CONTINUA (nao funciona como delimitador)
                self.prox()

        # O lexema final é o truncado a 35 (maximo de armazenamento)
        lexema_final = num_str[:35]

        if tem_ponto:
            return TokenClass("IDN05", lexema_final, self.linha)  # realConst
        else:
            return TokenClass("IDN04", lexema_final, self.linha)  # IntConst

    # metodo pra intentificador e palavras reservadas
    def fazer_identificador(self):
        id_str = ""
        qtd_char_lidos = 0  # Conta chars validos lidos antes do delimitador

        # Agora o loop verifica se é caractere de ID, delimitador ou inválido
        while self.char_atual is not None:
            char = self.char_atual

            # 1. Caracter do padrao (letra, digito, _)
            if char.isalnum() or char == "_":
                # Truncagem: coleta ate 32 chars, mas continua lendo
                if qtd_char_lidos < 32:
                    id_str += char

                qtd_char_lidos += 1
                self.prox()

            # 2. Caracteres que são delimitadores (VALIDOS)
            # Inclui: espacos em branco, quebra de linha, e todos os simbolos reservados, aspas, barra (pode ser divisao/comentario)
            elif (
                char in " \t\n"
                or char in simbolos_reservados
                or char == '"'
                or char == "/"
            ):
                break  # Encerra a formacao do atomo (delimitador encontrado)

            # 3. O que sobrar é um Caractere INVALDO (ex: '@', '$', '!')
            else:
                # Regra da especificacao: Caracteres invalidos devem ser FILTRADOS e
                # NAO DEVEM funcionar como delimitadores, permitindo que a formacao do atomo continue.
                self.prox()  # Filtra/ignora o caractere e continua no proximo loop

        # O lexema final para o token deve ser o truncado (max 35) e em caixa alta
        lexema_final = id_str[:35].upper()

        # Aq é pq eh case insensitive pra pravras reservadas
        id_lower = lexema_final.lower()

        # identifica se eh palabra reservada
        if id_lower in palavras_reservadas:
            codigo = palavras_reservadas[id_lower]
            # Usa o lexema em caixa alta para consistencia no relatorio
            return TokenClass(codigo, lexema_final, self.linha)

        # senao é um identificador normal
        codigo_idn = "IDN02"

        # aq joga na tabela de simbolos (passa o lexema truncado a 35 e a qtd de chars lidos)
        indice = self.tabela_simbolos.insert_symbol(
            lexema_final,
            codigo_idn,
            self.linha,
            qtd_char_lidos,  # Passa a qtd de chars lidos antes do delimitador
        )

        # O token armazena o lexema em caixa alta
        return TokenClass(codigo_idn, lexema_final, self.linha, indice_tab=indice)

    # processa strings
    def fazer_string(self):
        string_val = '"'
        self.prox()  # pula aspas iniciais
        qtd_char_lidos = 1  # Aspas iniciais contam

        while self.char_atual is not None and self.char_atual != '"':
            # trata quebra de linha dentro de strings
            if self.char_atual == "\n":
                self.linha += 1

            # O limite de 32 chars se aplica aqui tambem (incluindo aspas)
            if qtd_char_lidos < 32:
                string_val += self.char_atual

            qtd_char_lidos += 1
            self.prox()

        # Pula as aspas de fechamento (e adiciona se nao excedeu o limite)
        if self.char_atual == '"':
            if qtd_char_lidos < 32:
                string_val += '"'
            qtd_char_lidos += 1
            self.prox()  # pula as aspas de fechamento

        # Garante o truncamento final a 35 (que e o maximo de armazenamento)
        lexema_final = string_val[:35]

        return TokenClass("IDN06", lexema_final, self.linha)

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
        # tengo que ver se eh necessario mesmo
        tokens.append(TokenClass("EOF", "EOF", self.linha))
        return tokens
