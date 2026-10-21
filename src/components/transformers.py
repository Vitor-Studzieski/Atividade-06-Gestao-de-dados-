import pandas as pd

PARTICULAS = {"da", "das", "de", "do", "dos", "e"}


def _formatar_palavras(
    palavras: list[str], capitalizacao: str, *, capitalizar_primeira: bool = False
) -> str:
    if capitalizacao == "maiusculas":
        return " ".join(palavra.upper() for palavra in palavras)
    if capitalizacao == "nome_proprio":
        return " ".join(
            palavra.lower()
            if (indice > 0 or not capitalizar_primeira) and palavra.lower() in PARTICULAS
            else palavra.capitalize()
            for indice, palavra in enumerate(palavras)
        )
    raise ValueError("capitalizacao deve ser 'maiusculas' ou 'nome_proprio'.")


def processar_usuarios_etl(
    df: pd.DataFrame, *, capitalizacao: str = "maiusculas"
) -> pd.DataFrame:
    """Separa primeiro termo e restante do nome, com capitalização escolhida."""
    if "nome_completo" not in df.columns:
        raise ValueError("O DataFrame precisa ter a coluna 'nome_completo'.")

    partes = (
        df["nome_completo"]
        .fillna("")
        .astype(str)
        .str.split()
    )
    resultado = pd.DataFrame(index=df.index)
    resultado["primeiro_nome"] = partes.map(
        lambda nome: _formatar_palavras(
            nome[:1], capitalizacao, capitalizar_primeira=True
        ) if nome else ""
    )
    resultado["sobrenome"] = partes.map(
        lambda nome: _formatar_palavras(nome[1:], capitalizacao)
        if len(nome) > 1 else "NÃO INFORMADO"
    )
    return resultado
