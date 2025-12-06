import sys

from lexer import Lexer
from symbol_table import SymbolTable

# Informacoes da equipe para o relatorio
INFO_EQUIPE = {
    "codigo": "EQ06",
    "componentes": [
        {
            "nome": "Diogo Rossi Sampaio",
            "email": "diogo.sampaio@aln.senaicimatec.edu.br",
            "telefone": "71) 98321-3232",
        },
        {
            "nome": "Felipe Spinola Farias",
            "email": "felipe.farias@aln.senaicimatec.edu.br",
            "telefone": "71) 99987-9701",
        },
        {
            "nome": "Breno de Moura Batista",
            "email": "breno.batista@ba.estudante.senai.br",
            "telefone": "71) 99998-0446",
        },
        {
            "nome": "Nicollas Matsuo Mendes dos Santos",
            "email": "nicollas.santos@aln.senaicimatec.edu.br",
            "telefone": "11) 98931-3719",
        },
    ],
}


def main():
    if len(sys.argv) < 2:
        print(
            "Erro: Falta o nome base do arquivo a ser analisado. Ex: python main.py MeuTeste"
        )
        return

    nome_base = sys.argv[1]
    nome_arquivo_entrada = f"{nome_base}.252"
    nome_arquivo_lex = f"{nome_base}.LEX"
    nome_arquivo_tab = f"{nome_base}.TAB"

    try:
        with open(nome_arquivo_entrada, "r", encoding="utf-8") as f:
            conteudo = f.read()

        print(f"--- comecando analise lexica de -> {nome_arquivo_entrada} ---\n")

        tabela = SymbolTable()
        lexer = Lexer(conteudo, tabela)

        tokens = lexer.gerarTokens()

        # 1. Geracao do arquivo .LEX
        with open(nome_arquivo_lex, "w", encoding="utf-8") as a:
            # Cabecalho completo
            a.write(f"Código da Equipe: {INFO_EQUIPE['codigo']}\n")
            a.write("Componentes:\n")
            for comp in INFO_EQUIPE["componentes"]:
                a.write(f" {comp['nome']}; {comp['email']}; ({comp['telefone']})\n")

            # Titulo e nome do arquivo analisado
            a.write(
                f"\nRELATÓRIO DA ANÁLISE LÉXICA. Texto fonte analisado: {nome_arquivo_entrada}\n"
            )

            # Tokens formatados para o relatorio
            for t in tokens:
                a.write(f"{t.to_lex_report_line()}\n")  # Usa a funcao de formatacao

        print(f"--- relatorio .LEX gerado: {nome_arquivo_lex} ---\n")

        # 2. Geracao do arquivo .TAB
        with open(nome_arquivo_tab, "w", encoding="utf-8") as a:
            relatorio_tab = tabela.gerar_relatorio_tab(
                nome_arquivo_entrada, INFO_EQUIPE
            )
            a.write(relatorio_tab)

        print(f"--- relatorio .TAB gerado: {nome_arquivo_tab} ---\n")

    except FileNotFoundError:
        print(f"Erro: arquivo '{nome_arquivo_entrada}' nao encontrado.")


if __name__ == "__main__":
    main()
