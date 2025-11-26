from typing import Optional


class TokenClass:
    def __init__(
        self, codigo: str, lexema: str, linha: int, indice_tab: Optional[int] = None
    ) -> None:
        self.codigo = codigo
        self.lexema = lexema
        self.linha = linha
        self.indice_tab = indice_tab

    def __repr__(self) -> str:
        return f"Token(codigo='{self.codigo}', lexema='{self.lexema}', linha={self.linha}, indice_tab={self.indice_tab})"
