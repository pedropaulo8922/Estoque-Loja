def validar_string(valor, campo="Campo"):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} não pode ser vazio.")
    return valor.strip()


def validar_preco(valor):
    try:
        preco = float(valor)
    except (TypeError, ValueError):
        raise ValueError("Preço deve ser um número válido.")
    if preco < 0:
        raise ValueError("Preço não pode ser negativo.")
    return round(preco, 2)


def validar_quantidade(valor):
    try:
        qtd = int(valor)
    except (TypeError, ValueError):
        raise ValueError("Quantidade deve ser um número inteiro.")
    if qtd < 0:
        raise ValueError("Quantidade não pode ser negativa.")
    return qtd


def validar_quantidade_movimentacao(valor):
    qtd = validar_quantidade(valor)
    if qtd == 0:
        raise ValueError("Quantidade da movimentação deve ser maior que zero.")
    return qtd


def validar_id(valor):
    try:
        id_ = int(valor)
    except (TypeError, ValueError):
        raise ValueError("ID deve ser um número inteiro válido.")
    if id_ <= 0:
        raise ValueError("ID deve ser maior que zero.")
    return id_


def formatar_preco(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_linha(produto):
    return (
        f"[{produto['id']:>4}] "
        f"{produto['nome']:<30} "
        f"Cat: {produto['categoria']:<15} "
        f"Qtd: {produto['quantidade']:>6} "
        f"Preço: {formatar_preco(produto['preco'])}"
    )


def formatar_tabela(produtos):
    if not produtos:
        print("\n  Nenhum produto encontrado.\n")
        return
    separador = "-" * 85
    print(f"\n{separador}")
    print(f"{'ID':>6}  {'Nome':<30} {'Categoria':<15} {'Qtd':>6}  {'Preço':>12}")
    print(separador)
    for p in produtos:
        print(formatar_linha(p))
    print(f"{separador}\n")


def confirmar_acao(mensagem="Confirma? (s/n): "):
    resposta = input(mensagem).strip().lower()
    return resposta == "s"


def input_obrigatorio(prompt):
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("  Campo obrigatório. Tente novamente.")


def pausar():
    input("\nPressione ENTER para continuar...")