# Projeto-de-Gestor-de-bar

-1. O que o teu sistema faz no geral

Tu tens 4 “bases de dados” em listas:

clientes = []
atendentes = []
produtos = []
pedidos = []

👉 Isso significa que tudo fica guardado na memória do programa, não em ficheiro nem base de dados real.

🧩 2. Como cada parte funciona
👤 CLIENTES / ATENDENTES / PRODUTOS / PEDIDOS

Cada módulo segue o mesmo padrão:

➕ Criar
criar_cliente(...)

✔ Cria um dicionário (tipo “registo”)
✔ Adiciona à lista

Exemplo:

{"id": 1, "nome": "João"}
📄 Listar
listar_clientes()

✔ Devolve toda a lista

Ex:

[{"id": 1, "nome": "João"}]
✏️ Atualizar
atualizar_cliente(id, ...)

✔ Procura pelo id
✔ Se encontrar:

altera campos
✔ Se não:
retorna False
❌ Remover
remover_cliente(id)

✔ Procura pelo id
✔ Remove da lista

⚙️ 3. Como o teu sistema “pensa”

Ele funciona assim:

input → função → procura na lista → altera/mostra/remove
🔐 4. Sobre os “401 Unauthorized”

Quando adicionámos isso:

if not autorizado(auth):
    return {"status": 401}

👉 Isso simula um sistema de API

Mas no teu código original:

não existe login real
então auth=True sempre permite
📦 5. Validações (o último código)

Esse aqui:

validar_int
validar_float
validar_email
validar_nif

👉 serve para garantir que os dados estão corretos antes de serem usados

Ex:

NIF tem 9 números
email tem @ e .
número não pode ser texto
🧠 6. O que o teu projeto é na prática

👉 É um:

🟡 Mini sistema CRUD em Python

CRUD =

Create (criar)
Read (listar)
Update (atualizar)
Delete (remover)
⚠️ 7. Limitações do teu código

O teu sistema ainda:

❌ não guarda dados quando fecha
❌ não tem base de dados
❌ não tem login real
❌ não tem interface (só código)
