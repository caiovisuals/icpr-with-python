# RECIBO DE PAGAMENTO PARA PRESTADOR DE SERVIÇOS AUTÔNOMO COM PYTHON - ᴘᴛ

Sistema de geração e gerenciamento de **Recibo de Pagamento Autônomo (RPA)**
para uma empresa que contrata prestadores de serviço sem vínculo empregatício.

## Estado atual

O que já existe é o **domínio puro** (tipos de valor, arredondamento
parametrizável, máquina de estados, invariantes) e o **schema do banco**: 14
tabelas com constraints e índices, aplicadas por migration reversível. A camada
web e a geração de PDF ainda não existem.

**Escopo ampliado:** o sistema atenderá também funcionários CLT, com cálculo de
folha e emissão de holerite — **sem** férias, 13º, rescisão e eSocial. A ordem
definida é **RPA primeiro, até produção; CLT depois**, como módulo aditivo.

## Aviso sobre regras tributárias

Este projeto **não contém nenhuma regra tributária presumida**. Não há alíquota,
faixa, teto nem dedução no código-fonte, e não haverá: os valores vivem em
tabelas parametrizadas por vigência, preenchidas a partir de fonte oficial e
homologadas por profissional de contabilidade.

Enquanto ele não for preenchido e homologado, o sistema opera em **modo
simulação**: parâmetros podem ser carregados como provisórios e o cálculo roda,
mas o documento sai com marca d'água e **não pode virar recibo definitivo**.

## Como rodar

```bash
pip install -e ".[dev]"

ruff check . && ruff format --check .   # lint e formatação
mypy                                    # tipos, modo estrito
pytest --cov=app --cov-report=term-missing
```

Os quatro precisam passar antes de qualquer coisa ser considerada pronta.

Os testes de integração exigem **PostgreSQL de verdade** — SQLite não tem
constraint de exclusão, índice parcial nem gatilho, que é justamente o que eles
verificam. Sem `DATABASE_URL` eles são pulados, com aviso; no CI a variável
`RPA_REQUIRE_DB=1` transforma isso em falha, para que uma suíte inteira nunca
desapareça atrás de um build verde.

```bash
cp .env.example .env              # preencha POSTGRES_PASSWORD
docker compose up -d db           # sobe o banco
export DATABASE_URL="postgresql+psycopg://rpa:SENHA@localhost:5432/icpr"
alembic upgrade head              # aplica o schema
pytest
```

O domínio **não tem dependência de runtime** — por construção. Isso é verificado
por `tests/architecture/test_domain_purity.py`, que falha se alguém importar
framework, ORM, I/O ou ler o relógio dentro de `app/domain/`.

## Documentação

- [`AGENTS.md`](AGENTS.md) — regras de trabalho no repositório

# INDEPENDENT CONTRACTOR PAYMENT RECEIPT WITH PYTHON - ᴇɴ

by caiothevisual<br/>
#caiobavisuals #icpr-with-python #python #payment #receipt