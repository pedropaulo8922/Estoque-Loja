import sys
from database.schema import init_db
from ui.menu import menu_principal


def main():
    try:
        init_db()
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n  Programa encerrado pelo usuário.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Erro crítico: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()