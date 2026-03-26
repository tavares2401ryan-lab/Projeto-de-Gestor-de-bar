def validar_int(valor):
    try:
        return int(valor)
    except ValueError:
        print("Erro: deve ser um número inteiro!")
        return None

def validar_float(valor):
    try:
        return float(valor)
    except ValueError:
        print("Erro: deve ser um número!")
        return None

def validar_email(email):
    if "@" in email and "." in email:
        return True
    print("Email inválido!")
    return False

def validar_nif(nif):
    if nif.isdigit() and len(nif) == 9:
        return True
    print("NIF inválido! Deve ter 9 dígitos.")
    return False

def input_seguro_int(mensagem):
    while True:
        valor = input(mensagem)
        try:
            return int(valor)
        except ValueError:
            print("Erro: introduza um número válido!")

def input_seguro_float(mensagem):
    while True:
        valor = input(mensagem)
        try:
            return float(valor)
        except ValueError:
            print("Erro: introduza um número válido!")