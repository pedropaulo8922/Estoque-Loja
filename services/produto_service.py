from database.connection import execute_query, fetch_all, fetch_one
from utils.helpers import validar_string, validar_preco, validar_quantidade, validar_id


def criar_produto(nome, preco, quantidade, categoria="Geral"):
    nome      = validar_string(nome, "Nome")
    categoria = validar_string(categoria, "Categoria")
    preco     = validar_preco(preco)
    quantidade = validar_quantidade(quantidade)

    execute_query(
        "INSERT INTO produtos (nome, preco, quantidade, categoria) VALUES (?, ?, ?, ?)",
        (nome, preco, quantidade, categoria)
    )
    return {"mensagem": f"Produto '{nome}' cadastrado com sucesso."}


def listar_produtos():
    return fetch_all("SELECT * FROM produtos ORDER BY nome ASC")


def buscar_por_id(produto_id):
    produto_id = validar_id(produto_id)
    produto = fetch_one("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    if not produto:
        raise ValueError(f"Produto com ID {produto_id} não encontrado.")
    return produto


def buscar_por_nome(nome):
    nome = validar_string(nome, "Nome")
    return fetch_all(
        "SELECT * FROM produtos WHERE nome LIKE ?",
        (f"%{nome}%",)
    )


def atualizar_produto(produto_id, nome=None, preco=None, categoria=None):
    produto_id = validar_id(produto_id)
    produto    = buscar_por_id(produto_id)

    novo_nome      = validar_string(nome, "Nome")           if nome      else produto["nome"]
    novo_preco     = validar_preco(preco)                   if preco     else produto["preco"]
    nova_categoria = validar_string(categoria, "Categoria") if categoria else produto["categoria"]

    execute_query(
        "UPDATE produtos SET nome = ?, preco = ?, categoria = ? WHERE id = ?",
        (novo_nome, novo_preco, nova_categoria, produto_id)
    )
    return {"mensagem": f"Produto ID {produto_id} atualizado com sucesso."}


def remover_produto(produto_id):
    produto_id = validar_id(produto_id)
    buscar_por_id(produto_id)

    execute_query("DELETE FROM produtos WHERE id = ?", (produto_id,))
    return {"mensagem": f"Produto ID {produto_id} removido com sucesso."}


def produto_existe(produto_id):
    try:
        buscar_por_id(produto_id)
        return True
    except ValueError:
        return False
    