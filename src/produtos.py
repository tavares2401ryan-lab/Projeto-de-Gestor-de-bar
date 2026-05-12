import uuid
import json
import os

ARQUIVO = "produtos.json"


# =========================
# PERSISTÊNCIA JSON
# =========================

def salvar_produtos():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, indent=4, ensure_ascii=False)


def carregar_produtos():
    global produtos

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            produtos = json.load(arquivo)
    else:
        produtos = []


# carrega ao iniciar
carregar_produtos()


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

    salvar_produtos()  # 🔥 salva no JSON

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

            if novo_preco is not None:
                if not validar_preco(novo_preco):
                    return {"status": 400, "erro": "Preço inválido"}
                produto["preco"] = novo_preco

            if nova_categoria:
                produto["categoria"] = nova_categoria

            if ativo is not None:
                produto["ativo"] = bool(ativo)

            salvar_produtos()  # 🔥 salva alteração

            return {"status": 200, "data": produto}

    return {"status": 404, "erro": "Produto não encontrado"}


def remover_produto(id, auth=True):
    if not autorizado(auth):
        return {"status": 401, "erro": "Unauthorized"}

    for produto in produtos:
        if produto["id"] == id:
            produtos.remove(produto)

            salvar_produtos()  # 🔥 salva remoção

            return {"status": 200, "mensagem": "Produto removido"}

    return {"status": 404, "erro": "Produto não encontrado"}
