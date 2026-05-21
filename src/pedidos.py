import uuid
import json
import os
import logging
from produtos import produtos

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

ARQUIVO = "pedidos.json"

pedidos = []


# =========================
# PERSISTÊNCIA
# =========================

def salvar_pedidos():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(pedidos, arquivo, indent=4, ensure_ascii=False)

    logging.info("Pedidos salvos")


def carregar_pedidos():
    global pedidos

    if os.path.exists(ARQUIVO):

        try:
            with open(ARQUIVO, "r", encoding="utf-8") as arquivo:

                conteudo = arquivo.read().strip()

                if not conteudo:
                    pedidos = []
                    return

                pedidos = json.loads(conteudo)

            logging.info("Pedidos carregados")

        except json.JSONDecodeError:
            logging.error("Erro JSON")
            pedidos = []

    else:
        pedidos = []


# =========================
# AUTENTICAÇÃO (SIMULADA)
# =========================

def autorizado(auth=True):
    return auth


def gerar_id():
    return str(uuid.uuid4())


# =========================
# CALCULAR TOTAL REAL
# =========================

def calcular_total(lista_produtos):
    total = 0

    for item in lista_produtos:

        produto_id = item["id"]
        quantidade = item["quantidade"]

        for p in produtos:

            if p["id"] == produto_id:
                total += p["preco"] * quantidade

    logging.info("Total calculado")

    return total


# =========================
# PEDIDOS - CRUD COMPLETO
# =========================

def criar_pedido(id_cliente, id_atendente, produtos_lista, auth=True):
    carregar_pedidos()

    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    pedido = {
        "id": gerar_id(),
        "cliente": id_cliente,
        "atendente": id_atendente,
        "produtos": produtos_lista,
        "valor_total": calcular_total(produtos_lista)
    }

    pedidos.append(pedido)

    salvar_pedidos()

    logging.info("Pedido criado")

    return {"status": 201, "data": pedido}


def listar_pedidos(auth=True):
    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    carregar_pedidos()

    return {"status": 200, "data": pedidos}


def obter_pedido(id, auth=True):
    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    carregar_pedidos()

    for pedido in pedidos:

        if pedido["id"] == id:
            return {"status": 200, "data": pedido}

    logging.warning("Pedido não encontrado")

    return {"status": 404, "erro": "Pedido não encontrado"}


def atualizar_pedido(id, novos_produtos=None, auth=True):
    carregar_pedidos()

    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    for pedido in pedidos:

        if pedido["id"] == id:

            if novos_produtos:
                pedido["produtos"] = novos_produtos
                pedido["valor_total"] = calcular_total(novos_produtos)

            salvar_pedidos()

            logging.info("Pedido atualizado")

            return {"status": 200, "data": pedido}

    logging.warning("Pedido não encontrado")

    return {"status": 404, "erro": "Pedido não encontrado"}


def remover_pedido(id, auth=True):
    carregar_pedidos()

    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    for pedido in pedidos:

        if pedido["id"] == id:

            pedidos.remove(pedido)

            salvar_pedidos()

            logging.warning("Pedido removido")

            return {"status": 200, "mensagem": "Pedido removido"}

    logging.warning("Pedido não encontrado")

    return {"status": 404, "erro": "Pedido não encontrado"}
