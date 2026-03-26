from Clientes_do_Bar import criar_cliente, listar_clientes, atualizar_cliente, remover_cliente
from Atendente_do_Bar import criar_atendente, listar_atendentes, atualizar_atendente, remover_atendente
from produtos import criar_produto, listar_produtos, atualizar_produto, remover_produto
from pedidos import criar_pedido, listar_pedidos, atualizar_pedido, remover_pedido

from utils import input_seguro_int, input_seguro_float, validar_email, validar_nif


def menu_principal():
    while True:
        print("\n=== SISTEMA DE BAR ===")
        print("1 - Clientes")
        print("2 - Atendentes")
        print("3 - Produtos")
        print("4 - Pedidos")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            menu_clientes()
        elif op == "2":
            menu_atendentes()
        elif op == "3":
            menu_produtos()
        elif op == "4":
            menu_pedidos()
        elif op == "0":
            print("A sair...")
            break
        else:
            print("Opção inválida!")


# ---------------- CLIENTES ----------------
def menu_clientes():
    while True:
        print("\n--- CLIENTES ---")
        print("1 - Criar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Remover")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            id = input_seguro_int("ID: ")
            nome = input("Nome: ")
            telefone = input("Telefone: ")

            email = input("Email: ")
            if not validar_email(email):
                continue

            nif = input("NIF: ")
            if not validar_nif(nif):
                continue

            criar_cliente(id, nome, telefone, email, nif)

        elif op == "2":
            print(listar_clientes())

        elif op == "3":
            id = input_seguro_int("ID: ")
            nome = input("Novo nome: ")
            atualizar_cliente(id, nome)

        elif op == "4":
            id = input_seguro_int("ID: ")
            remover_cliente(id)

        elif op == "0":
            break


# ---------------- ATENDENTES ----------------
def menu_atendentes():
    while True:
        print("\n--- ATENDENTES ---")
        print("1 - Criar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Remover")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            id = input_seguro_int("ID: ")
            nome = input("Nome: ")
            tipo = input("Tipo: ")
            data = input("Data nascimento: ")

            criar_atendente(id, nome, tipo, data)

        elif op == "2":
            print(listar_atendentes())

        elif op == "3":
            id = input_seguro_int("ID: ")
            nome = input("Novo nome: ")
            atualizar_atendente(id, nome)

        elif op == "4":
            id = input_seguro_int("ID: ")
            remover_atendente(id)

        elif op == "0":
            break


# ---------------- PRODUTOS ----------------
def menu_produtos():
    while True:
        print("\n--- PRODUTOS ---")
        print("1 - Criar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Remover")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            id = input_seguro_int("ID: ")
            nome = input("Nome: ")
            preco = input_seguro_float("Preço: ")
            categoria = input("Categoria: ")

            criar_produto(id, nome, preco, categoria)

        elif op == "2":
            print(listar_produtos())

        elif op == "3":
            id = input_seguro_int("ID: ")
            preco = input_seguro_float("Novo preço: ")
            atualizar_produto(id, preco)

        elif op == "4":
            id = input_seguro_int("ID: ")
            remover_produto(id)

        elif op == "0":
            break


# ---------------- PEDIDOS ----------------
def menu_pedidos():
    while True:
        print("\n--- PEDIDOS ---")
        print("1 - Criar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Remover")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            id = input_seguro_int("ID: ")
            cliente = input_seguro_int("ID Cliente: ")
            atendente = input_seguro_int("ID Atendente: ")
            produtos = input("Produtos (vírgula): ").split(",")
            valor = input_seguro_float("Valor total: ")

            criar_pedido(id, cliente, atendente, produtos, valor)

        elif op == "2":
            print(listar_pedidos())

        elif op == "3":
            id = input_seguro_int("ID: ")
            valor = input_seguro_float("Novo valor: ")
            atualizar_pedido(id, novo_valor=valor)

        elif op == "4":
            id = input_seguro_int("ID: ")
            remover_pedido(id)

        elif op == "0":
            break


# --------- INICIAR ----------
menu_principal()