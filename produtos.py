produtos = []

def criar_produto(id, nome, preco, categoria):
    produto = {
        "id": id,
        "nome": nome,
        "preco": preco,
        "categoria": categoria
    }
    produtos.append(produto)

def listar_produtos():
    return produtos

def atualizar_produto(id, novo_preco=None):
    for produto in produtos:
        if produto["id"] == id:
            if novo_preco:
                produto["preco"] = novo_preco
            return True
    return False

def remover_produto(id):
    for produto in produtos:
        if produto["id"] == id:
            produtos.remove(produto)
            return True
    return False