import uuid

atendentes = []

# Simulação simples de autenticação
def autorizado(auth=True):
    return auth


def gerar_id():
    return str(uuid.uuid4())  # ID único aleatório


def validar_nome(nome):
    return isinstance(nome, str) and nome.replace(" ", "").isalpha()


def criar_atendente(nome, tipo, data_nascimento, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    if not validar_nome(nome):
        return {"status": 400, "erro": "Nome deve conter apenas letras"}

    atendente = {
        "id": gerar_id(),
        "nome": nome,
        "tipo": tipo,
        "data_nascimento": data_nascimento,
        "ativo": False  # começa como falso
    }

    atendentes.append(atendente)
    return {"status": 201, "data": atendente}


def listar_atendentes(auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    return {"status": 200, "data": atendentes}


def atualizar_atendente(id, novo_nome=None, ativo=None, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for atendente in atendentes:
        if atendente["id"] == id:
            if novo_nome:
                if not validar_nome(novo_nome):
                    return {"status": 400, "erro": "Nome inválido"}
                atendente["nome"] = novo_nome

            if ativo is not None:
                atendente["ativo"] = bool(ativo)

            return {"status": 200, "data": atendente}

    return {"status": 404, "erro": "Not Found"}


def remover_atendente(id, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for atendente in atendentes:
        if atendente["id"] == id:
            atendentes.remove(atendente)
            return {"status": 200, "mensagem": "Removido com sucesso"}

    return {"status": 404, "erro": "Not Found"}
