pedidos = []

def criar_pedido(id, id_cliente, id_atendente, produtos, valor_total):
    pedido = {
        "id": id,
        "cliente": id_cliente,
        "atendente": id_atendente,
        "produtos": produtos,
        "valor_total": valor_total
    }
    pedidos.append(pedido)

def listar_pedidos():
    return pedidos

def atualizar_pedido(id, novos_produtos=None, novo_valor=None):
    for pedido in pedidos:
        if pedido["id"] == id:
            if novos_produtos:
                pedido["produtos"] = novos_produtos
            if novo_valor:
                pedido["valor_total"] = novo_valor
            return True
    return False

def remover_pedido(id):
    for pedido in pedidos:
        if pedido["id"] == id:
            pedidos.remove(pedido)
            return True
    return False