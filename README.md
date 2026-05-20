#  Sistema de Estoque — Loja

Sistema CRUD de estoque via terminal, construído em Python puro com SQLite3.

##  Como executar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/estoque-loja.git
cd estoque-loja

# Execute diretamente (sem dependências externas)
python main.py
```


##  Estrutura do projeto
```
estoque-loja/
├── database/
│   ├── connection.py       # Conexão e queries SQLite
│   ├── schema.py           # Criação das tabelas
│   └── estoque.db          # Gerado automaticamente
├── services/
│   ├── produto_service.py  # CRUD de produtos
│   └── estoque_service.py  # Movimentações de estoque
├── ui/
│   └── menu.py             # Interface CLI
├── utils/
│   └── helpers.py          # Validações e formatações
├── main.py                 # Ponto de entrada
└── requirements.txt        # Sem dependências externas
```


## Funcionalidades

### Produtos
- Cadastrar produto (nome, preço, quantidade, categoria)
- Listar todos os produtos
- Buscar por ID ou nome
- Atualizar nome, preço e categoria
- Remover produto

### Estoque
- Entrada de unidades
- Saída de unidades (com validação de saldo)
- Histórico de movimentações (geral ou por produto)
- Alerta de estoque baixo (limite configurável)
- Resumo financeiro do estoque


## Banco de dados

### Tabela `produtos`
| Campo      | Tipo    | Descrição              |
|------------|---------|------------------------|
| id         | INTEGER | PK autoincrement       |
| nome       | TEXT    | Único, obrigatório     |
| preco      | REAL    | >= 0                   |
| quantidade | INTEGER | >= 0, padrão 0         |
| categoria  | TEXT    | Padrão "Geral"         |

### Tabela `movimentacoes`
| Campo      | Tipo    | Descrição                   |
|------------|---------|-----------------------------|
| id         | INTEGER | PK autoincrement            |
| produto_id | INTEGER | FK → produtos               |
| tipo       | TEXT    | "entrada" ou "saida"        |
| quantidade | INTEGER | > 0                         |
| data_hora  | TEXT    | datetime local automático   |


## Arquitetura

- **Procedural** — sem classes ou OOP
- **Modular** — cada camada com responsabilidade única
- **SQL parametrizado** — sem risco de SQL injection
- **Tratamento de erros** — try/except em todas operações críticas

##  Contribuindo

```bash
# Crie sua branch
git checkout -b feature/nome-da-feature

# Commit
git commit -m "feat: descrição clara da mudança"

# Push
git push origin feature/nome-da-feature
```
