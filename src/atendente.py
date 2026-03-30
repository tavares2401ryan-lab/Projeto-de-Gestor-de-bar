atendentes = []

def criar_atendente(id, nome, tipo, data_nascimento):
    atendente = {
        "id": id,
        "nome": nome,
        "tipo": tipo,
        "data_nascimento": data_nascimento
    }
    atendentes.append(atendente)

def listar_atendentes():
    return atendentes

def atualizar_atendente(id, novo_nome=None):
    for atendente in atendentes:
        if atendente["id"] == id:
            if novo_nome:
                atendente["nome"] = novo_nome
            return True
    return False

def remover_atendente(id):
    for atendente in atendentes:
        if atendente["id"] == id:
            atendentes.remove(atendente)
            return True
    return False