from Clientes_do_Bar import criar_cliente, listar_clientes, atualizar_cliente, remover_cliente
from Atendente_do_Bar import criar_atendente, listar_atendentes, atualizar_atendente, remover_atendente
from produtos import criar_produto, listar_produtos, atualizar_produto, remover_produto
from pedidos import criar_pedido, listar_pedidos, atualizar_pedido, remover_pedido

from utils import input_seguro_float, validar_email, validar_nif


def mostrar_lista(lista):
    if not lista:
        print("Nenhum registo encontrado.")
        return

    for item in lista:
        print("-" * 40)
        for k, v in item.items():
            print(f"{k}: {v}")


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
            nome = input("Nome: ")
            telefone = input("Telefone: ")

            email = input("Email: ")
            if not validar_email(email):
                print("Email inválido!")
                continue

            nif = input("NIF: ")
            if not validar_nif(nif):
                print("NIF inválido!")
                continue

            res = criar_cliente(nome, telefone, email, nif)
            print(res)

        elif op == "2":
            res = listar_clientes()
            mostrar_lista(res["data"])

        elif op == "3":
            id = input("ID do cliente: ")
            nome = input("Novo nome (enter para ignorar): ")
            ativo = input("Ativo (True/False ou vazio): ")

            ativo = None if ativo == "" else ativo.lower() == "true"

            res = atualizar_cliente(id, novo_nome=nome or None, ativo=ativo)
            print(res)

        elif op == "4":
            id = input("ID do cliente: ")
            print(remover_cliente(id))

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
            nome = input("Nome: ")
            tipo = input("Tipo: ")
            data = input("Data nascimento: ")

            print(criar_atendente(nome, tipo, data))

        elif op == "2":
            res = listar_atendentes()
            mostrar_lista(res["data"])

        elif op == "3":
            id = input("ID do atendente: ")
            nome = input("Novo nome: ")
            ativo = input("Ativo (True/False ou vazio): ")

            ativo = None if ativo == "" else ativo.lower() == "true"

            print(atualizar_atendente(id, novo_nome=nome or None, ativo=ativo))

        elif op == "4":
            id = input("ID do atendente: ")
            print(remover_atendente(id))

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
            nome = input("Nome: ")
            preco = input_seguro_float("Preço: ")
            categoria = input("Categoria: ")

            print(criar_produto(nome, preco, categoria))

        elif op == "2":
            res = listar_produtos()
            mostrar_lista(res["data"])

        elif op == "3":
            id = input("ID do produto: ")
            preco = input_seguro_float("Novo preço: ")

            print(atualizar_produto(id, preco))

        elif op == "4":
            id = input("ID do produto: ")
            print(remover_produto(id))

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
            cliente = input("ID Cliente: ")
            atendente = input("ID Atendente: ")
            produtos = input("Produtos (vírgula): ").split(",")
            valor = input_seguro_float("Valor total: ")

            print(criar_pedido(cliente, atendente, produtos, valor))

        elif op == "2":
            res = listar_pedidos()
            mostrar_lista(res["data"])

        elif op == "3":
            id = input("ID do pedido: ")
            valor = input_seguro_float("Novo valor: ")

            print(atualizar_pedido(id, novo_valor=valor))

        elif op == "4":
            id = input("ID do pedido: ")
            print(remover_pedido(id))

        elif op == "0":
            break


# --------- INICIAR ----------
menu_principal()
        elif op == "0":
            break


# --------- INICIAR ----------
menu_principal()
