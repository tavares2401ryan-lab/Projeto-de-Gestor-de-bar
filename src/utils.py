def validar_int(valor):
    try:
        return int(valor)
    except ValueError:
        return None


def validar_float(valor):
    try:
        return float(valor)
    except ValueError:
        return None


def validar_email(email):
    return "@" in email and "." in email


def validar_nif(nif):
    return nif.isdigit() and len(nif) == 9


def input_seguro_int(mensagem):
    while True:
        valor = input(mensagem)
        convertido = validar_int(valor)
        if convertido is not None:
            return convertido
        print("Erro: introduza um número válido!")


def input_seguro_float(mensagem):
    while True:
        valor = input(mensagem)
        convertido = validar_float(valor)
        if convertido is not None:
            return convertido
        print("Erro: introduza um número válido!")
