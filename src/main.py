import argparse

import pandas as pd
from sqlalchemy import create_engine, inspect, text

from src.components.transformers import processar_usuarios_etl
from src.database.connection import get_engine


NOMES_DEMO = [
    "Ewerton Silva", "Ana Paula Oliveira", "João Pedro Santos", "Maria Eduarda Costa",
    "Carlos Henrique Ferreira", "Beatriz Souza", "Lucas Gabriel Rodrigues", "Fernanda Lima",
    "Ricardo Alves", "Juliana Pereira", "Gabriel Nascimento", "Mariana Guimarães",
    "Thiago Mendes", "Camila Rocha", "Bruno Cardoso", "Larissa Freitas",
    "Marcelo Vieira", "Amanda Machado", "Felipe Castro", "Letícia Barbosa",
    "Diego Ribeiro", "Patrícia Gomes", "Rodrigo Carvalho", "Tatiana Martins",
    "Gustavo Araújo", "Priscila Melo", "André Luiz Moreira", "Vanessa Caldeira",
    "Marcos Vinícius Cunha", "Renata Lopes", "Alexandre Ramos", "Simone Teixeira",
    "Daniel Cavalcanti", "Aline Borges", "Eduardo Farias", "Cláudia Neves",
    "Leonardo Pires", "Suelen Viana", "Vitor Hugo Amaral", "Gisele Monteiro",
    "Caio Augusto Aguiar", "Bianca Peixoto", "Samuel Telles", "Karina Rezende",
    "Henrique Silveira", "Débora Porto", "Otávio Mesquita", "Lorena Caldas",
    "Hugo Magalhães", "Cintia Veras",
]


def criar_engine_demo():
    """Prepara um banco SQLite em memória com os 50 nomes do material."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    with engine.begin() as conexao:
        conexao.execute(
            text(
                "CREATE TABLE usuarios_temporarios "
                "(id INTEGER PRIMARY KEY, nome_completo VARCHAR(100))"
            )
        )
        conexao.execute(
            text(
                "CREATE TABLE usuarios_final "
                "(id INTEGER PRIMARY KEY, primeiro_nome VARCHAR(50), sobrenome VARCHAR(100))"
            )
        )
        conexao.execute(
            text("INSERT INTO usuarios_temporarios (nome_completo) VALUES (:nome)"),
            [{"nome": nome} for nome in NOMES_DEMO],
        )
    return engine


def validar_esquema(df: pd.DataFrame, engine, tabela: str = "usuarios_final") -> None:
    """Impede a carga quando faltam colunas ou algum texto excede o tamanho do banco."""
    colunas = {
        coluna["name"]: getattr(coluna["type"], "length", None)
        for coluna in inspect(engine).get_columns(tabela)
    }
    faltantes = [nome for nome in df.columns if nome not in colunas]
    if faltantes:
        raise ValueError(
            f"A tabela '{tabela}' não possui as colunas esperadas: {', '.join(faltantes)}."
        )

    for nome, limite in colunas.items():
        if nome not in df.columns or limite is None:
            continue
        comprimentos = df[nome].dropna().astype(str).str.len()
        excedentes = comprimentos[comprimentos > limite]
        if not excedentes.empty:
            indice = excedentes.index[0]
            valor = str(df.loc[indice, nome])
            raise ValueError(
                f"Validação de esquema: '{tabela}.{nome}' permite {limite} caracteres, "
                f"mas o valor {valor!r} tem {len(valor)}. Carga cancelada."
            )


def executar_etl(engine) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Extrai, transforma e carrega os usuários no banco informado."""
    with engine.connect() as conexao:
        conexao.execute(text("SELECT 1"))
    print("Conexão estabelecida!")

    df_bruto = pd.read_sql(text("SELECT * FROM usuarios_temporarios"), engine)
    print(f"{len(df_bruto)} registros extraídos.")

    df_transformado = processar_usuarios_etl(df_bruto)
    print("Dados transformados e padronizados:")
    print(df_transformado.head().to_string(index=False))

    validar_esquema(df_transformado, engine)
    print("Validação de esquema aprovada.")
    df_transformado.to_sql(
        "usuarios_final", con=engine, if_exists="append", index=False
    )
    print("Carga finalizada com sucesso na tabela 'usuarios_final'!")
    return df_bruto, df_transformado


def main():
    parser = argparse.ArgumentParser(description="ETL de usuários do projeto Gestão de Dados")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="executa com SQLite em memória e os 50 nomes do PDF, sem MySQL",
    )
    args = parser.parse_args()

    engine = criar_engine_demo() if args.demo else get_engine()
    try:
        executar_etl(engine)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
