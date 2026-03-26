clientes = []

def criar_cliente(id, nome, telefone, email, nif):
    cliente = {
        "id": id,
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "nif": nif
    }
    clientes.append(cliente)

def listar_clientes():
    return clientes

def atualizar_cliente(id, novo_nome=None, novo_telefone=None):
    for cliente in clientes:
        if cliente["id"] == id:
            if novo_nome:
                cliente["nome"] = novo_nome
            if novo_telefone:
                cliente["telefone"] = novo_telefone
            return True
    return False

def remover_cliente(id):
    for cliente in clientes:
        if cliente["id"] == id:
            clientes.remove(cliente)
            return True
    return False