from typing import Optional


class TokenClass:
    def __init__(
        self, codigo: str, lexema: str, linha: int, indice_tab: Optional[int] = None
    ) -> None:
        self.codigo = codigo
        self.lexema = lexema
        self.linha = linha
        self.indice_tab = indice_tab

    def to_lex_report_line(self) -> str:
        indice_tab_str = str(self.indice_tab) if self.indice_tab is not None else ""

        lexema_relatorio = (
            self.lexema.upper()
            if self.codigo.startswith(("IDN", "PRS"))
            else self.lexema
        )

        return (
            f"Lexeme: {lexema_relatorio}, \n"
            f"Código: {self.codigo}, ÍndiceTabSimb: {indice_tab_str},\n"
            f"Linha: {self.linha}."
        )

    def __repr__(self) -> str:
        return f"Token(codigo='{self.codigo}', lexema='{self.lexema}', linha={self.linha}, indice_tab={self.indice_tab})"
