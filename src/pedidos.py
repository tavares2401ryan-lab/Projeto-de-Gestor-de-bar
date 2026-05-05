import uuid
from produtos import produtos  # 🔥 usa a lista real de produtos

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

    return total


# =========================
# PEDIDOS - CRUD COMPLETO
# =========================

def criar_pedido(id_cliente, id_atendente, produtos_lista, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    pedido = {
        "id": gerar_id(),
        "cliente": id_cliente,
        "atendente": id_atendente,
        "produtos": produtos_lista,
        "valor_total": calcular_total(produtos_lista)
    }

    pedidos.append(pedido)
    return {"status": 201, "data": pedido}


def listar_pedidos(auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    return {"status": 200, "data": pedidos}


def obter_pedido(id, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for pedido in pedidos:
        if pedido["id"] == id:
            return {"status": 200, "data": pedido}

    return {"status": 404, "erro": "Pedido não encontrado"}


def atualizar_pedido(id, novos_produtos=None, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for pedido in pedidos:
        if pedido["id"] == id:

            if novos_produtos:
                pedido["produtos"] = novos_produtos
                pedido["valor_total"] = calcular_total(novos_produtos)

            return {"status": 200, "data": pedido}

    return {"status": 404, "erro": "Pedido não encontrado"}


def remover_pedido(id, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for pedido in pedidos:
        if pedido["id"] == id:
            pedidos.remove(pedido)
            return {"status": 200, "mensagem": "Pedido removido"}

    return {"status": 404, "erro": "Pedido não encontrado"}
