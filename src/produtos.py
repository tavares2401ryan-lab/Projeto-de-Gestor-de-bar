produtos = []

# =========================
# AUTENTICAÇÃO (SIMULADA)
# =========================

def autorizado(auth=True):
    return auth


# =========================
# PRODUTOS - CRUD COMPLETO
# =========================

def criar_produto(id, nome, preco, categoria, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    # evitar duplicados
    for p in produtos:
        if p["id"] == id:
            return {"status": 409, "erro": "Produto já existe"}

    produto = {
        "id": id,
        "nome": nome,
        "preco": preco,
        "categoria": categoria
    }

    produtos.append(produto)
    return {"status": 201, "data": produto}


def listar_produtos(auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    return {"status": 200, "data": produtos}


def obter_produto(id, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for produto in produtos:
        if produto["id"] == id:
            return {"status": 200, "data": produto}

    return {"status": 404, "erro": "Produto não encontrado"}


def atualizar_produto(id, novo_nome=None, novo_preco=None, nova_categoria=None, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for produto in produtos:
        if produto["id"] == id:

            if novo_nome:
                produto["nome"] = novo_nome
            if novo_preco:
                produto["preco"] = novo_preco
            if nova_categoria:
                produto["categoria"] = nova_categoria

            return {"status": 200, "data": produto}

    return {"status": 404, "erro": "Produto não encontrado"}


def remover_produto(id, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for produto in produtos:
        if produto["id"] == id:
            produtos.remove(produto)
            return {"status": 200, "mensagem": "Produto removido"}

    return {"status": 404, "erro": "Produto não encontrado"}
