from database.connection import execute_query, fetch_all, fetch_one
from utils.helpers import validar_id, validar_quantidade_movimentacao


def _buscar_quantidade_atual(produto_id):
    row = fetch_one("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
    if not row:
        raise ValueError(f"Produto ID {produto_id} não encontrado.")
    return row["quantidade"]


def _registrar_movimentacao(produto_id, tipo, quantidade):
    execute_query(
        "INSERT INTO movimentacoes (produto_id, tipo, quantidade) VALUES (?, ?, ?)",
        (produto_id, tipo, quantidade)
    )


def entrada_estoque(produto_id, quantidade):
    produto_id = validar_id(produto_id)
    quantidade = validar_quantidade_movimentacao(quantidade)

    atual = _buscar_quantidade_atual(produto_id)
    nova  = atual + quantidade

    execute_query(
        "UPDATE produtos SET quantidade = ? WHERE id = ?",
        (nova, produto_id)
    )
    _registrar_movimentacao(produto_id, "entrada", quantidade)

    return {"mensagem": f"Entrada de {quantidade} unidade(s). Estoque atual: {nova}."}


def saida_estoque(produto_id, quantidade):
    produto_id = validar_id(produto_id)
    quantidade = validar_quantidade_movimentacao(quantidade)

    atual = _buscar_quantidade_atual(produto_id)
    if quantidade > atual:
        raise ValueError(
            f"Estoque insuficiente. Disponível: {atual}, solicitado: {quantidade}."
        )

    nova = atual - quantidade

    execute_query(
        "UPDATE produtos SET quantidade = ? WHERE id = ?",
        (nova, produto_id)
    )
    _registrar_movimentacao(produto_id, "saida", quantidade)

    return {"mensagem": f"Saída de {quantidade} unidade(s). Estoque atual: {nova}."}


def listar_movimentacoes(produto_id=None):
    if produto_id:
        produto_id = validar_id(produto_id)
        return fetch_all(
            """
            SELECT m.id, p.nome, m.tipo, m.quantidade, m.data_hora
            FROM movimentacoes m
            JOIN produtos p ON p.id = m.produto_id
            WHERE m.produto_id = ?
            ORDER BY m.data_hora DESC
            """,
            (produto_id,)
        )
    return fetch_all(
        """
        SELECT m.id, p.nome, m.tipo, m.quantidade, m.data_hora
        FROM movimentacoes m
        JOIN produtos p ON p.id = m.produto_id
        ORDER BY m.data_hora DESC
        """
    )


def listar_estoque_baixo(limite=5):
    return fetch_all(
        "SELECT * FROM produtos WHERE quantidade <= ? ORDER BY quantidade ASC",
        (limite,)
    )


def resumo_estoque():
    return fetch_one(
        """
        SELECT
            COUNT(*)                        AS total_produtos,
            SUM(quantidade)                 AS total_unidades,
            SUM(quantidade * preco)         AS valor_total,
            AVG(preco)                      AS preco_medio
        FROM produtos
        """
    )
    