pedidos = []

# =========================
# AUTENTICAÇÃO (SIMULADA)
# =========================

def autorizado(auth=True):
    return auth


# =========================
# PEDIDOS - CRUD COMPLETO
# =========================

def criar_pedido(id, id_cliente, id_atendente, produtos, valor_total, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    # evitar ID duplicado
    for p in pedidos:
        if p["id"] == id:
            return {"status": 409, "erro": "Pedido já existe"}

    pedido = {
        "id": id,
        "cliente": id_cliente,
        "atendente": id_atendente,
        "produtos": produtos,
        "valor_total": valor_total
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


def atualizar_pedido(id, novos_produtos=None, novo_valor=None, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for pedido in pedidos:
        if pedido["id"] == id:

            if novos_produtos:
                pedido["produtos"] = novos_produtos

            if novo_valor:
                pedido["valor_total"] = novo_valor

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
