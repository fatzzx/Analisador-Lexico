import sys

from lexer import Lexer
from symbol_table import SymbolTable


def main():
    if len(sys.argv) < 2:
        print("erro")
        return

    nome_base = sys.argv[1]
    nome_arquivo = f"{nome_base}.252"

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        print(f"--- comecando -> {nome_arquivo} ---\n")

        tabela = SymbolTable()
        lexer = Lexer(conteudo, tabela)

        tokens = lexer.gerarTokens()

        with open(f"{nome_arquivo}.LEX", "w", encoding="utf-8") as a:
            a.write("EQUIPE EQ06\n")
            a.write("Felipe Spinola Farias\n")
            a.write("Diogo Rossi\n")
            a.write("Nicollas Matsuo\n")
            a.write("Breno de Moura\n")
            for t in tokens:
                a.write(f"{t}\n")

    except FileNotFoundError:
        print(f"Erro: arq '{nome_arquivo}' nao encontrado.")


if __name__ == "__main__":
    main()
