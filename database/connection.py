import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "estoque.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def close_connection(conn):
    if conn:
        conn.close()


def execute_query(query, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Erro ao executar query: {e}")
    finally:
        close_connection(conn)


def fetch_all(query, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise RuntimeError(f"Erro ao buscar dados: {e}")
    finally:
        close_connection(conn)


def fetch_one(query, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        raise RuntimeError(f"Erro ao buscar registro: {e}")
    finally:
        close_connection(conn)