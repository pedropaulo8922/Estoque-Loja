from database.connection import get_connection, close_connection


SQL_CREATE_PRODUTOS = """
CREATE TABLE IF NOT EXISTS produtos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT    NOT NULL UNIQUE,
    preco     REAL    NOT NULL CHECK(preco >= 0),
    quantidade INTEGER NOT NULL DEFAULT 0 CHECK(quantidade >= 0),
    categoria TEXT    NOT NULL DEFAULT 'Geral'
);
"""

SQL_CREATE_MOVIMENTACOES = """
CREATE TABLE IF NOT EXISTS movimentacoes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id  INTEGER NOT NULL,
    tipo        TEXT    NOT NULL CHECK(tipo IN ('entrada', 'saida')),
    quantidade  INTEGER NOT NULL CHECK(quantidade > 0),
    data_hora   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);
"""


def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(SQL_CREATE_PRODUTOS)
        cursor.execute(SQL_CREATE_MOVIMENTACOES)
        conn.commit()
        print("[OK] Banco de dados inicializado.")
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Erro ao inicializar banco: {e}")
    finally:
        close_connection(conn)


def drop_all_tables():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS movimentacoes")
        cursor.execute("DROP TABLE IF EXISTS produtos")
        conn.commit()
        print("[OK] Tabelas removidas.")
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Erro ao remover tabelas: {e}")
    finally:
        close_connection(conn)


def reset_db():
    drop_all_tables()
    init_db()
    