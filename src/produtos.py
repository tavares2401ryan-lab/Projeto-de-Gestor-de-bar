import uuid

# lista inicial (exemplo de bar)
produtos = [
    {"id": str(uuid.uuid4()), "nome": "Cerveja", "preco": 2.5, "categoria": "Bebida"},
    {"id": str(uuid.uuid4()), "nome": "Vinho", "preco": 4.0, "categoria": "Bebida"},
    {"id": str(uuid.uuid4()), "nome": "Whisky", "preco": 6.5, "categoria": "Bebida"},
    {"id": str(uuid.uuid4()), "nome": "Água", "preco": 1.0, "categoria": "Bebida"},
    {"id": str(uuid.uuid4()), "nome": "Batata Frita", "preco": 3.0, "categoria": "Comida"},
]


# =========================
# AUTENTICAÇÃO (SIMULADA)
# =========================
def autorizado(auth=True):
    return auth


def gerar_id():
    return str(uuid.uuid4())


def validar_nome(nome):
    return isinstance(nome, str) and len(nome.strip()) > 0


def validar_preco(preco):
    return isinstance(preco, (int, float)) and preco >= 0


# =========================
# PRODUTOS - CRUD COMPLETO
# =========================

def criar_produto(nome, preco, categoria, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    if not validar_nome(nome):
        return {"status": 400, "erro": "Nome inválido"}

    if not validar_preco(preco):
        return {"status": 400, "erro": "Preço inválido"}

    produto = {
        "id": gerar_id(),
        "nome": nome,
        "preco": preco,
        "categoria": categoria,
        "ativo": True
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


def atualizar_produto(id, novo_nome=None, novo_preco=None, nova_categoria=None, ativo=None, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for produto in produtos:
        if produto["id"] == id:

            if novo_nome:
                if not validar_nome(novo_nome):
                    return {"status": 400, "erro": "Nome inválido"}
                produto["nome"] = novo_nome

            if novo_preco is not None:  # 🔥 corrige bug do 0
                if not validar_preco(novo_preco):
                    return {"status": 400, "erro": "Preço inválido"}
                produto["preco"] = novo_preco

            if nova_categoria:
                produto["categoria"] = nova_categoria

            if ativo is not None:
                produto["ativo"] = bool(ativo)

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
    
