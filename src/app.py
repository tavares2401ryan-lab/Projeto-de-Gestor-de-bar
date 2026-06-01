from tkinter import *
from tkinter import ttk, messagebox

from cliente import listar_clientes, criar_cliente
from produtos import listar_produtos
from atendente import listar_atendentes
from pedidos import listar_pedidos


# =========================
# JANELA PRINCIPAL
# =========================

janela = Tk()
janela.title("Sistema de Gestão de Bar")
janela.geometry("600x400")
janela.resizable(False, False)


# =========================
# FORM CLIENTE (CRIAR)
# =========================

def abrir_form_cliente():
    form = Toplevel()
    form.title("Adicionar Cliente")
    form.geometry("350x300")

    Label(form, text="Nome").pack()
    nome = Entry(form)
    nome.pack()

    Label(form, text="Telefone").pack()
    telefone = Entry(form)
    telefone.pack()

    Label(form, text="Email").pack()
    email = Entry(form)
    email.pack()

    Label(form, text="NIF").pack()
    nif = Entry(form)
    nif.pack()


    def salvar():
        resultado = criar_cliente(
            nome.get(),
            telefone.get(),
            email.get(),
            nif.get()
        )

        if resultado["status"] == 201:
            messagebox.showinfo("Sucesso", "Cliente criado! 👍")
            form.destroy()
        else:
            messagebox.showerror("Erro", resultado.get("erro", "Erro"))


    Button(form, text="Salvar", command=salvar, bg="green", fg="white").pack(pady=15)


# =========================
# CLIENTES
# =========================

def abrir_clientes():
    nova = Toplevel()
    nova.title("Clientes")
    nova.geometry("700x400")

    tabela = ttk.Treeview(
        nova,
        columns=("Nome", "Telefone", "Email", "NIF"),
        show="headings"
    )

    for col in ("Nome", "Telefone", "Email", "NIF"):
        tabela.heading(col, text=col)
        tabela.column(col, width=150)

    tabela.pack(fill=BOTH, expand=True)

    resultado = listar_clientes()

    if resultado and "data" in resultado:
        for c in resultado["data"]:
            tabela.insert(
                "",
                END,
                values=(c["nome"], c["telefone"], c["email"], c["nif"])
            )

    Button(
        nova,
        text="➕ Adicionar Cliente",
        command=abrir_form_cliente,
        bg="green",
        fg="white"
    ).pack(pady=10)


# =========================
# PRODUTOS (🍺 MENU BAR MELHORADO)
# =========================

def abrir_produtos():
    nova = Toplevel()
    nova.title("🍺 Menu do Bar")
    nova.geometry("750x450")

    Label(
        nova,
        text="🍺 MENU DO BAR",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    tabela = ttk.Treeview(
        nova,
        columns=("Nome", "Categoria", "Preço"),
        show="headings"
    )

    tabela.heading("Nome", text="Nome")
    tabela.heading("Categoria", text="Categoria")
    tabela.heading("Preço", text="Preço (€)")

    tabela.column("Nome", width=250)
    tabela.column("Categoria", width=150)
    tabela.column("Preço", width=100)

    tabela.pack(fill=BOTH, expand=True)

    resultado = listar_produtos()

    if resultado and "data" in resultado:
        for p in resultado["data"]:
            tabela.insert(
                "",
                END,
                values=(
                    p["nome"],
                    p["categoria"],
                    f"{p['preco']:.2f} €"
                )
            )


# =========================
# ATENDENTES
# =========================

def abrir_atendentes():
    nova = Toplevel()
    nova.title("Atendentes")
    nova.geometry("700x400")

    tabela = ttk.Treeview(
        nova,
        columns=("Nome", "Tipo", "Nascimento"),
        show="headings"
    )

    for col in ("Nome", "Tipo", "Nascimento"):
        tabela.heading(col, text=col)
        tabela.column(col, width=150)

    tabela.pack(fill=BOTH, expand=True)

    resultado = listar_atendentes()

    if resultado and "data" in resultado:
        for a in resultado["data"]:
            tabela.insert(
                "",
                END,
                values=(a["nome"], a["tipo"], a["data_nascimento"])
            )


# =========================
# PEDIDOS
# =========================

def abrir_pedidos():
    nova = Toplevel()
    nova.title("Pedidos")
    nova.geometry("700x400")

    tabela = ttk.Treeview(
        nova,
        columns=("Cliente", "Atendente", "Total"),
        show="headings"
    )

    for col in ("Cliente", "Atendente", "Total"):
        tabela.heading(col, text=col)
        tabela.column(col, width=150)

    tabela.pack(fill=BOTH, expand=True)

    resultado = listar_pedidos()

    if resultado and "data" in resultado:
        for p in resultado["data"]:
            tabela.insert(
                "",
                END,
                values=(p["cliente"], p["atendente"], p["valor_total"])
            )


# =========================
# MENU PRINCIPAL
# =========================

Label(
    janela,
    text="🍺 SISTEMA DE BAR",
    font=("Arial", 18, "bold")
).pack(pady=20)

Button(janela, text="Clientes", width=20, command=abrir_clientes).pack(pady=5)
Button(janela, text="Produtos (Menu)", width=20, command=abrir_produtos).pack(pady=5)
Button(janela, text="Atendentes", width=20, command=abrir_atendentes).pack(pady=5)
Button(janela, text="Pedidos", width=20, command=abrir_pedidos).pack(pady=5)

Button(
    janela,
    text="Sair",
    width=20,
    command=janela.destroy,
    bg="red",
    fg="white"
).pack(pady=20)


janela.mainloop()