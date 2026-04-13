atendentes = []

# Simulação simples de autenticação
def autorizado(auth=True):
    return auth  # em um sistema real isso seria um token/check

def criar_atendente(id, nome, tipo, data_nascimento, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    atendente = {
        "id": id,
        "nome": nome,
        "tipo": tipo,
        "data_nascimento": data_nascimento
    }
    atendentes.append(atendente)
    return {"status": 201, "data": atendente}


def listar_atendentes(auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    return {"status": 200, "data": atendentes}


def atualizar_atendente(id, novo_nome=None, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for atendente in atendentes:
        if atendente["id"] == id:
            if novo_nome:
                atendente["nome"] = novo_nome
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
