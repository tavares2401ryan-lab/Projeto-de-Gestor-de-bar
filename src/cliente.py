import uuid

clientes = []

# =========================
# AUTENTICAÇÃO (SIMULADA)
# =========================
def autorizado(auth=True):
    return auth


# =========================
# VALIDAÇÕES
# =========================
def gerar_id():
    return str(uuid.uuid4())


def validar_nome(nome):
    return isinstance(nome, str) and nome.replace(" ", "").isalpha()


def validar_telefone(telefone):
    return isinstance(telefone, str) and telefone.isdigit() and len(telefone) >= 9


def validar_email(email):
    return isinstance(email, str) and "@" in email and "." in email


def validar_nif(nif):
    return isinstance(nif, str) and nif.isdigit() and len(nif) == 9


# =========================
# CLIENTES - CRUD COMPLETO
# =========================

def criar_cliente(nome, telefone, email, nif, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    if not validar_nome(nome):
        return {"status": 400, "erro": "Nome inválido"}

    if not validar_telefone(telefone):
        return {"status": 400, "erro": "Telefone inválido"}

    if not validar_email(email):
        return {"status": 400, "erro": "Email inválido"}

    if not validar_nif(nif):
        return {"status": 400, "erro": "NIF inválido"}

    # evitar duplicados
    for c in clientes:
        if c["email"] == email:
            return {"status": 409, "erro": "Email já cadastrado"}
        if c["nif"] == nif:
            return {"status": 409, "erro": "NIF já cadastrado"}

    cliente = {
        "id": gerar_id(),
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "nif": nif,
        "ativo": False  # começa inativo
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


def atualizar_cliente(id, novo_nome=None, novo_telefone=None, novo_email=None, novo_nif=None, ativo=None, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for cliente in clientes:
        if cliente["id"] == id:

            if novo_nome:
                if not validar_nome(novo_nome):
                    return {"status": 400, "erro": "Nome inválido"}
                cliente["nome"] = novo_nome

            if novo_telefone:
                if not validar_telefone(novo_telefone):
                    return {"status": 400, "erro": "Telefone inválido"}
                cliente["telefone"] = novo_telefone

            if novo_email:
                if not validar_email(novo_email):
                    return {"status": 400, "erro": "Email inválido"}
                cliente["email"] = novo_email

            if novo_nif:
                if not validar_nif(novo_nif):
                    return {"status": 400, "erro": "NIF inválido"}
                cliente["nif"] = novo_nif

            if ativo is not None:
                cliente["ativo"] = bool(ativo)

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
