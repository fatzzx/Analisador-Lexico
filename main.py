import sys

from token_class import Token
from symbol_table import SymbolTable
from lexer import Lexer

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <nome_do_arquivo_sem_extensao>")
        return

    nome_base = sys.argv[1]
    nome_arquivo = f"{nome_base}.252"

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        print(f"--- Iniciando Análise de {nome_arquivo} ---\n")

        tabela = SymbolTable()
        lexer = Lexer(conteudo, tabela)
        
        tokens = lexer.gerarTokens()

        for t in tokens:
            print(t)

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")

if __name__ == "__main__":
    main()