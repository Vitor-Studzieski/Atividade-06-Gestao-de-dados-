# Experimento de ETL - Integração CSV para SQL

Projeto didático do material de instalação e configuração Python. Ele extrai nomes da tabela `usuarios_temporarios`, separa o primeiro termo do restante do nome, padroniza os campos em maiúsculas e grava o resultado em `usuarios_final`.

## Ambiente

Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Windows, ative com `\.venv\Scripts\activate`.

## MySQL

1. Execute `sql/setup_mysql.sql` no MySQL Workbench para criar o banco `gestaodados`, as tabelas e os 50 registros de origem.
2. Copie `.env.example` para `.env` e preencha a senha do seu MySQL.
3. Rode o ETL:

```bash
python -m src.main
```

O PDF usa nomes diferentes para o banco em dois trechos. Este projeto padroniza o nome como `gestaodados`, igual ao primeiro comando de criação do próprio material.

Antes da carga, o ETL confere se as colunas de destino existem e se os valores cabem nos limites definidos no banco. Para reproduzir a falha de truncamento do material, execute no MySQL:

```sql
ALTER TABLE usuarios_final MODIFY primeiro_nome VARCHAR(5);
```

Depois rode o ETL: a validação deve interromper a carga e indicar o primeiro nome que excede o limite. Restaure a coluna com `ALTER TABLE usuarios_final MODIFY primeiro_nome VARCHAR(50);`.

## Demonstração sem MySQL

Para executar o fluxo completo com os mesmos 50 nomes em um banco SQLite temporário:

```bash
python -m src.main --demo
```

Esse modo é útil para conferir o ETL; o banco temporário existe apenas durante a execução.

Para nomes com partículas como “da” e “de”, a transformação também oferece a capitalização de nome próprio (`capitalizacao="nome_proprio"`). O padrão continua em maiúsculas, como na célula de transformação do PDF. A regra de divisão segue “primeiro termo versus restante”; reconhecer nomes compostos exige uma regra de negócio ou uma base de nomes.

Para registrar as versões exatas instaladas no ambiente, gere o arquivo congelado com `./.venv/bin/python -m pip freeze > requirements.txt`.

## Notebook

Abra `notebooks/exploracao.ipynb` no VS Code, selecione o kernel do ambiente `.venv` e execute as células. O notebook usa a conexão MySQL configurada em `.env`.
