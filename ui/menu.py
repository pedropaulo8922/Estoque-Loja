from services import produto_service as ps
from services import estoque_service as es
from utils.helpers import (
    formatar_tabela, formatar_preco, input_obrigatorio, confirmar_acao, pausar
)


# ── Helpers de UI ─────────────────────────────────────────────────────────────

def _cabecalho(titulo):
    print(f"\n{'═' * 50}")
    print(f"  {titulo}")
    print(f"{'═' * 50}")


def _sucesso(msg):
    print(f"\n  ✔  {msg}")


def _erro(msg):
    print(f"\n  ✘  Erro: {msg}")


def _exibir_movimentacoes(movs):
    if not movs:
        print("\n  Nenhuma movimentação encontrada.\n")
        return
    separador = "-" * 70
    print(f"\n{separador}")
    print(f"{'ID':>5}  {'Produto':<25} {'Tipo':<8} {'Qtd':>6}  {'Data/Hora'}")
    print(separador)
    for m in movs:
        print(
            f"{m['id']:>5}  {m['nome']:<25} {m['tipo']:<8} "
            f"{m['quantidade']:>6}  {m['data_hora']}"
        )
    print(f"{separador}\n")


# ── Menus de Produto ──────────────────────────────────────────────────────────

def tela_cadastrar_produto():
    _cabecalho("CADASTRAR PRODUTO")
    try:
        nome      = input_obrigatorio("  Nome      : ")
        preco     = input_obrigatorio("  Preço     : ")
        quantidade = input("  Quantidade (padrão 0): ").strip() or "0"
        categoria = input("  Categoria  (padrão Geral): ").strip() or "Geral"

        resultado = ps.criar_produto(nome, preco, quantidade, categoria)
        _sucesso(resultado["mensagem"])
    except ValueError as e:
        _erro(e)
    pausar()


def tela_listar_produtos():
    _cabecalho("LISTA DE PRODUTOS")
    produtos = ps.listar_produtos()
    formatar_tabela(produtos)
    pausar()


def tela_buscar_produto():
    _cabecalho("BUSCAR PRODUTO")
    print("  [1] Buscar por ID")
    print("  [2] Buscar por Nome")
    opcao = input("\n  Opção: ").strip()

    try:
        if opcao == "1":
            pid = input_obrigatorio("  ID: ")
            produto = ps.buscar_por_id(pid)
            formatar_tabela([produto])
        elif opcao == "2":
            nome = input_obrigatorio("  Nome: ")
            produtos = ps.buscar_por_nome(nome)
            formatar_tabela(produtos)
        else:
            _erro("Opção inválida.")
    except ValueError as e:
        _erro(e)
    pausar()


def tela_atualizar_produto():
    _cabecalho("ATUALIZAR PRODUTO")
    try:
        pid = input_obrigatorio("  ID do produto: ")
        produto = ps.buscar_por_id(pid)
        formatar_tabela([produto])

        print("  (deixe em branco para manter o valor atual)")
        nome      = input(f"  Nome      [{produto['nome']}]: ").strip() or None
        preco     = input(f"  Preço     [{produto['preco']}]: ").strip() or None
        categoria = input(f"  Categoria [{produto['categoria']}]: ").strip() or None

        resultado = ps.atualizar_produto(pid, nome, preco, categoria)
        _sucesso(resultado["mensagem"])
    except ValueError as e:
        _erro(e)
    pausar()


def tela_remover_produto():
    _cabecalho("REMOVER PRODUTO")
    try:
        pid = input_obrigatorio("  ID do produto: ")
        produto = ps.buscar_por_id(pid)
        formatar_tabela([produto])

        if confirmar_acao("  Confirma remoção? (s/n): "):
            resultado = ps.remover_produto(pid)
            _sucesso(resultado["mensagem"])
        else:
            print("\n  Operação cancelada.")
    except ValueError as e:
        _erro(e)
    pausar()


# ── Menus de Estoque ──────────────────────────────────────────────────────────

def tela_entrada_estoque():
    _cabecalho("ENTRADA DE ESTOQUE")
    try:
        pid = input_obrigatorio("  ID do produto: ")
        qtd = input_obrigatorio("  Quantidade   : ")
        resultado = es.entrada_estoque(pid, qtd)
        _sucesso(resultado["mensagem"])
    except ValueError as e:
        _erro(e)
    pausar()


def tela_saida_estoque():
    _cabecalho("SAÍDA DE ESTOQUE")
    try:
        pid = input_obrigatorio("  ID do produto: ")
        qtd = input_obrigatorio("  Quantidade   : ")
        resultado = es.saida_estoque(pid, qtd)
        _sucesso(resultado["mensagem"])
    except ValueError as e:
        _erro(e)
    pausar()


def tela_movimentacoes():
    _cabecalho("HISTÓRICO DE MOVIMENTAÇÕES")
    print("  [1] Todas as movimentações")
    print("  [2] Por produto")
    opcao = input("\n  Opção: ").strip()

    try:
        if opcao == "1":
            movs = es.listar_movimentacoes()
        elif opcao == "2":
            pid = input_obrigatorio("  ID do produto: ")
            movs = es.listar_movimentacoes(pid)
        else:
            _erro("Opção inválida.")
            pausar()
            return
        _exibir_movimentacoes(movs)
    except ValueError as e:
        _erro(e)
    pausar()


def tela_estoque_baixo():
    _cabecalho("ALERTAS — ESTOQUE BAIXO")
    try:
        limite = input("  Limite mínimo (padrão 5): ").strip() or "5"
        produtos = es.listar_estoque_baixo(int(limite))
        formatar_tabela(produtos)
    except ValueError as e:
        _erro(e)
    pausar()


def tela_resumo():
    _cabecalho("RESUMO DO ESTOQUE")
    try:
        r = es.resumo_estoque()
        if not r:
            print("\n  Sem dados.\n")
        else:
            print(f"\n  Total de produtos  : {r['total_produtos']}")
            print(f"  Total de unidades  : {r['total_unidades'] or 0}")
            print(f"  Valor em estoque   : {formatar_preco(r['valor_total'] or 0)}")
            print(f"  Preço médio        : {formatar_preco(r['preco_medio'] or 0)}\n")
    except Exception as e:
        _erro(e)
    pausar()


# ── Menu Principal ────────────────────────────────────────────────────────────

def menu_produtos():
    opcoes = {
        "1": tela_cadastrar_produto,
        "2": tela_listar_produtos,
        "3": tela_buscar_produto,
        "4": tela_atualizar_produto,
        "5": tela_remover_produto,
    }
    while True:
        _cabecalho("PRODUTOS")
        print("  [1] Cadastrar produto")
        print("  [2] Listar produtos")
        print("  [3] Buscar produto")
        print("  [4] Atualizar produto")
        print("  [5] Remover produto")
        print("  [0] Voltar")
        opcao = input("\n  Opção: ").strip()
        if opcao == "0":
            break
        acao = opcoes.get(opcao)
        if acao:
            acao()
        else:
            _erro("Opção inválida.")
            pausar()


def menu_estoque():
    opcoes = {
        "1": tela_entrada_estoque,
        "2": tela_saida_estoque,
        "3": tela_movimentacoes,
        "4": tela_estoque_baixo,
        "5": tela_resumo,
    }
    while True:
        _cabecalho("ESTOQUE")
        print("  [1] Entrada de estoque")
        print("  [2] Saída de estoque")
        print("  [3] Histórico de movimentações")
        print("  [4] Alertas de estoque baixo")
        print("  [5] Resumo do estoque")
        print("  [0] Voltar")
        opcao = input("\n  Opção: ").strip()
        if opcao == "0":
            break
        acao = opcoes.get(opcao)
        if acao:
            acao()
        else:
            _erro("Opção inválida.")
            pausar()


def menu_principal():
    while True:
        _cabecalho("SISTEMA DE ESTOQUE — LOJA")
        print("  [1] Produtos")
        print("  [2] Estoque")
        print("  [0] Sair")
        opcao = input("\n  Opção: ").strip()
        if opcao == "1":
            menu_produtos()
        elif opcao == "2":
            menu_estoque()
        elif opcao == "0":
            print("\n  Até logo!\n")
            break
        else:
            _erro("Opção inválida.")
            pausar()