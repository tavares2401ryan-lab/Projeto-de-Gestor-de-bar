import uuid
import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

ARQUIVO = "atendentes.json"

atendentes = []


# =========================
# PERSISTÊNCIA
# =========================

def salvar_atendentes():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(atendentes, arquivo, indent=4, ensure_ascii=False)

    logging.info("Atendentes salvos")


def carregar_atendentes():
    global atendentes

    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
                atendentes = json.load(arquivo)

            logging.info("Atendentes carregados")

        except json.JSONDecodeError:
            logging.error("Erro JSON")
            atendentes = []

    else:
        atendentes = []


# =========================
# AUTENTICAÇÃO (SIMULADA)
# =========================

def autorizado(auth=True):
    return auth


def gerar_id():
    return str(uuid.uuid4())


def validar_nome(nome):
    return isinstance(nome, str) and nome.replace(" ", "").isalpha()


# =========================
# ATENDENTES - CRUD
# =========================

def criar_atendente(nome, tipo, data_nascimento, auth=True):
    carregar_atendentes()

    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    if not validar_nome(nome):
        logging.warning("Nome inválido")
        return {"status": 400, "erro": "Nome deve conter apenas letras"}

    atendente = {
        "id": gerar_id(),
        "nome": nome,
        "tipo": tipo,
        "data_nascimento": data_nascimento,
        "ativo": False
    }

    atendentes.append(atendente)

    salvar_atendentes()

    logging.info("Atendente criado")

    return {"status": 201, "data": atendente}


def listar_atendentes(auth=True):
    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    carregar_atendentes()

    return {"status": 200, "data": atendentes}


def atualizar_atendente(id, novo_nome=None, ativo=None, auth=True):
    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    carregar_atendentes()

    for atendente in atendentes:
        if atendente["id"] == id:

            if novo_nome:
                if not validar_nome(novo_nome):
                    logging.warning("Nome inválido")
                    return {"status": 400, "erro": "Nome inválido"}

                atendente["nome"] = novo_nome

            if ativo is not None:
                atendente["ativo"] = bool(ativo)

            salvar_atendentes()

            logging.info("Atendente atualizado")

            return {"status": 200, "data": atendente}

    logging.warning("Atendente não encontrado")

    return {"status": 404, "erro": "Not Found"}


def remover_atendente(id, auth=True):
    carregar_atendentes()

    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    for atendente in atendentes:
        if atendente["id"] == id:

            atendentes.remove(atendente)

            salvar_atendentes()

            logging.warning("Atendente removido")

            return {"status": 200, "mensagem": "Removido com sucesso"}

    logging.warning("Atendente não encontrado")

    return {"status": 404, "erro": "Not Found"}
