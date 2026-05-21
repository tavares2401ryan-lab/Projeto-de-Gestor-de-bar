import uuid
import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

ARQUIVO = "clientes.json"

clientes = []


# =========================
# PERSISTÊNCIA
# =========================

def salvar_clientes():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(clientes, arquivo, indent=4, ensure_ascii=False)

    logging.info("Clientes salvos")


def carregar_clientes():
    global clientes

    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
                clientes = json.load(arquivo)

            logging.info("Clientes carregados")

        except json.JSONDecodeError:
            logging.error("Erro JSON")
            clientes = []

    else:
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
    carregar_clientes()

    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    if not validar_nome(nome):
        logging.warning("Nome inválido")
        return {"status": 400, "erro": "Nome inválido"}

    if not validar_telefone(telefone):
        logging.warning("Telefone inválido")
        return {"status": 400, "erro": "Telefone inválido"}

    if not validar_email(email):
        logging.warning("Email inválido")
        return {"status": 400, "erro": "Email inválido"}

    if not validar_nif(nif):
        logging.warning("NIF inválido")
        return {"status": 400, "erro": "NIF inválido"}

    for c in clientes:

        if c["email"] == email:
            logging.warning("Email duplicado")
            return {"status": 409, "erro": "Email já cadastrado"}

        if c["nif"] == nif:
            logging.warning("NIF duplicado")
            return {"status": 409, "erro": "NIF já cadastrado"}

    cliente = {
        "id": gerar_id(),
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "nif": nif,
        "ativo": False
    }

    clientes.append(cliente)

    salvar_clientes()

    logging.info("Cliente criado")

    return {"status": 201, "data": cliente}


def listar_clientes(auth=True):
    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    carregar_clientes()

    return {"status": 200, "data": clientes}


def obter_cliente(id, auth=True):
    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    carregar_clientes()

    for cliente in clientes:
        if cliente["id"] == id:
            return {"status": 200, "data": cliente}

    logging.warning("Cliente não encontrado")

    return {"status": 404, "erro": "Cliente não encontrado"}


def atualizar_cliente(
    id,
    novo_nome=None,
    novo_telefone=None,
    novo_email=None,
    novo_nif=None,
    ativo=None,
    auth=True
):
    carregar_clientes()

    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    for cliente in clientes:

        if cliente["id"] == id:

            if novo_nome:

                if not validar_nome(novo_nome):
                    logging.warning("Nome inválido")
                    return {"status": 400, "erro": "Nome inválido"}

                cliente["nome"] = novo_nome

            if novo_telefone:

                if not validar_telefone(novo_telefone):
                    logging.warning("Telefone inválido")
                    return {"status": 400, "erro": "Telefone inválido"}

                cliente["telefone"] = novo_telefone

            if novo_email:

                if not validar_email(novo_email):
                    logging.warning("Email inválido")
                    return {"status": 400, "erro": "Email inválido"}

                cliente["email"] = novo_email

            if novo_nif:

                if not validar_nif(novo_nif):
                    logging.warning("NIF inválido")
                    return {"status": 400, "erro": "NIF inválido"}

                cliente["nif"] = novo_nif

            if ativo is not None:
                cliente["ativo"] = bool(ativo)

            salvar_clientes()

            logging.info("Cliente atualizado")

            return {"status": 200, "data": cliente}

    logging.warning("Cliente não encontrado")

    return {"status": 404, "erro": "Cliente não encontrado"}


def remover_cliente(id, auth=True):
    carregar_clientes()

    if not autorizado(auth):
        logging.error("Sem autorização")
        return {"status": 401, "erro": "Unauthorized"}

    for cliente in clientes:

        if cliente["id"] == id:

            clientes.remove(cliente)

            salvar_clientes()

            logging.warning("Cliente removido")

            return {"status": 200, "mensagem": "Cliente removido"}

    logging.warning("Cliente não encontrado")

    return {"status": 404, "erro": "Cliente não encontrado"}
