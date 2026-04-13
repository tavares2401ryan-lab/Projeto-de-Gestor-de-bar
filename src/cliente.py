clientes = []

# =========================
# AUTENTICAÇÃO (SIMULADA)
# =========================
def autorizado(auth=True):
    return auth


# =========================
# CLIENTES - CRUD COMPLETO
# =========================

def criar_cliente(id, nome, telefone, email, nif, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    # evitar IDs duplicados
    for c in clientes:
        if c["id"] == id:
            return {"status": 409, "erro": "Cliente já existe"}

    cliente = {
        "id": id,
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "nif": nif
    }

    clientes.append(cliente)
    return {"status": 201, "data": cliente}


def listar_clientes(auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    return {"status": 200, "data": clientes}


def obter_cliente(id, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for cliente in clientes:
        if cliente["id"] == id:
            return {"status": 200, "data": cliente}

    return {"status": 404, "erro": "Cliente não encontrado"}


def atualizar_cliente(id, novo_nome=None, novo_telefone=None, novo_email=None, novo_nif=None, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for cliente in clientes:
        if cliente["id"] == id:

            if novo_nome:
                cliente["nome"] = novo_nome
            if novo_telefone:
                cliente["telefone"] = novo_telefone
            if novo_email:
                cliente["email"] = novo_email
            if novo_nif:
                cliente["nif"] = novo_nif

            return {"status": 200, "data": cliente}

    return {"status": 404, "erro": "Cliente não encontrado"}


def remover_cliente(id, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for cliente in clientes:
        if cliente["id"] == id:
            clientes.remove(cliente)
            return {"status": 200, "mensagem": "Cliente removido"}

    return {"status": 404, "erro": "Cliente não encontrado"}
