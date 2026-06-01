from tkinter import *
from tkinter import ttk

from cliente import listar_clientes
from produtos import listar_produtos
from atendente import listar_atendentes
from pedidos import listar_pedidos


# =========================
# JANELA PRINCIPAL
# =========================

janela = Tk()
janela.title("🍺 Sistema de Gestão de Bar")
janela.state("zoomed")
janela.configure(bg="#0f172a")


# =========================
# ESTILO
# =========================

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#1e293b",
                foreground="white",
                rowheight=32,
                fieldbackground="#1e293b",
                font=("Arial", 10))

style.configure("Treeview.Heading",
                background="#1d4ed8",
                foreground="white",
                font=("Arial", 10, "bold"),
                padding=8)

style.map("Treeview",
          background=[("selected", "#2563eb")],
          foreground=[("selected", "white")])


# =========================
# HEADER
# =========================

header = Frame(janela, bg="#1d4ed8", height=65)
header.pack(side=TOP, fill=X)
header.pack_propagate(False)

Label(header,
      text="🍺  SISTEMA DE GESTÃO DE BAR",
      bg="#1d4ed8",
      fg="white",
      font=("Arial", 17, "bold")).pack(side=LEFT, padx=25, pady=18)

Label(header,
      text="Bar Manager v1.0",
      bg="#1d4ed8",
      fg="#bfdbfe",
      font=("Arial", 9)).pack(side=RIGHT, padx=25)


# =========================
# SIDEBAR
# =========================

sidebar = Frame(janela, bg="#0b1220", width=220)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

content = Frame(janela, bg="#0f172a")
content.pack(side=RIGHT, fill=BOTH, expand=True)

Label(sidebar, text="MENU", bg="#0b1220", fg="#64748b",
      font=("Arial", 9, "bold")).pack(pady=(25, 5))


def sidebar_btn(text, cmd):
    b = Button(sidebar,
               text=text,
               command=cmd,
               bg="#0b1220",
               fg="#e2e8f0",
               activebackground="#1e293b",
               activeforeground="white",
               relief=FLAT,
               pady=11,
               width=22,
               anchor=W,
               padx=18,
               font=("Arial", 10),
               cursor="hand2")
    b.pack(fill=X, pady=1)

    def on_enter(e): b.configure(bg="#1e293b")
    def on_leave(e): b.configure(bg="#0b1220")
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)

    return b


sidebar_btn("  👥  Clientes",   lambda: abrir_tabela_clientes())
sidebar_btn("  🍺  Produtos",   lambda: abrir_tabela_produtos())
sidebar_btn("  🧑‍🍳  Atendentes", lambda: abrir_tabela_atendentes())
sidebar_btn("  🧾  Pedidos",    lambda: abrir_tabela_pedidos())

Frame(sidebar, bg="#1e293b", height=1).pack(fill=X, padx=15, pady=20)

b_sair = Button(sidebar,
                text="  ❌  Sair",
                command=janela.destroy,
                bg="#0b1220",
                fg="#f87171",
                activebackground="#1e293b",
                activeforeground="#f87171",
                relief=FLAT,
                pady=11,
                width=22,
                anchor=W,
                padx=18,
                font=("Arial", 10),
                cursor="hand2")
b_sair.pack(fill=X, pady=1)


# =========================
# FUNÇÃO TABELA
# =========================

def criar_tabela(parent, cols):
    frame = Frame(parent, bg="#0f172a")
    frame.pack(fill=BOTH, expand=True, padx=25, pady=20)

    tabela = ttk.Treeview(frame, columns=cols, show="headings")

    scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    scroll.pack(side=RIGHT, fill=Y)
    tabela.pack(fill=BOTH, expand=True)

    for c in cols:
        tabela.heading(c, text=c)
        tabela.column(c, width=200)

    tabela.tag_configure("odd",  background="#1e293b")
    tabela.tag_configure("even", background="#172035")

    return tabela


def preencher(tabela, rows):
    for i, row in enumerate(rows):
        tag = "odd" if i % 2 == 0 else "even"
        tabela.insert("", END, values=row, tags=(tag,))


# =========================
# CLIENTES
# =========================

def abrir_tabela_clientes():
    win = Toplevel(janela)
    win.state("zoomed")
    win.title("Clientes")
    win.configure(bg="#0f172a")

    Label(win, text="👥  Clientes", bg="#0f172a", fg="white",
          font=("Arial", 15, "bold")).pack(anchor=W, padx=25, pady=(20, 0))

    tabela = criar_tabela(win, ("Nome", "Telefone", "Email", "NIF"))

    data = listar_clientes()
    if data and "data" in data:
        preencher(tabela, [(c["nome"], c["telefone"], c["email"], c["nif"])
                           for c in data["data"]])


# =========================
# PRODUTOS
# =========================

def abrir_tabela_produtos():
    win = Toplevel(janela)
    win.state("zoomed")
    win.title("Produtos")
    win.configure(bg="#0f172a")

    Label(win, text="🍺  Produtos", bg="#0f172a", fg="white",
          font=("Arial", 15, "bold")).pack(anchor=W, padx=25, pady=(20, 0))

    tabela = criar_tabela(win, ("Nome", "Categoria", "Preço"))

    data = listar_produtos()
    if data and "data" in data:
        preencher(tabela, [(p["nome"], p["categoria"], f"€ {p['preco']:.2f}")
                           for p in data["data"]])


# =========================
# ATENDENTES
# =========================

def abrir_tabela_atendentes():
    win = Toplevel(janela)
    win.state("zoomed")
    win.title("Atendentes")
    win.configure(bg="#0f172a")

    Label(win, text="🧑‍🍳  Atendentes", bg="#0f172a", fg="white",
          font=("Arial", 15, "bold")).pack(anchor=W, padx=25, pady=(20, 0))

    tabela = criar_tabela(win, ("Nome", "Tipo", "Nascimento"))

    data = listar_atendentes()
    if data and "data" in data:
        preencher(tabela, [(a["nome"], a["tipo"], a["data_nascimento"])
                           for a in data["data"]])


# =========================
# PEDIDOS
# =========================

def abrir_tabela_pedidos():
    win = Toplevel(janela)
    win.state("zoomed")
    win.title("Pedidos")
    win.configure(bg="#0f172a")

    Label(win, text="🧾  Pedidos", bg="#0f172a", fg="white",
          font=("Arial", 15, "bold")).pack(anchor=W, padx=25, pady=(20, 0))

    tabela = criar_tabela(win, ("Cliente", "Atendente", "Total"))

    data = listar_pedidos()
    if data and "data" in data:
        preencher(tabela, [(p["cliente"], p["atendente"], f"€ {p['valor_total']:.2f}")
                           for p in data["data"]])


# =========================
# DASHBOARD CARDS
# =========================

Label(content, text="RESUMO", bg="#0f172a", fg="#475569",
      font=("Arial", 9, "bold")).pack(anchor=W, padx=30, pady=(30, 10))

cards = Frame(content, bg="#0f172a")
cards.pack(anchor=W, padx=25)


def card(emoji, texto, valor, cor):
    f = Frame(cards, bg="#1e293b", width=175, height=105)
    f.pack(side=LEFT, padx=8)
    f.pack_propagate(False)

    Label(f, text=emoji, bg="#1e293b", font=("Arial", 20)).pack(pady=(12, 0))
    Label(f, text=valor, bg="#1e293b", fg=cor,
          font=("Arial", 16, "bold")).pack()
    Label(f, text=texto, bg="#1e293b", fg="#64748b",
          font=("Arial", 9)).pack()


try:
    card("👥", "Clientes",   len(listar_clientes()["data"]),   "#38bdf8")
    card("🍺", "Produtos",   len(listar_produtos()["data"]),   "#34d399")
    card("🧑‍🍳", "Atendentes", len(listar_atendentes()["data"]), "#a78bfa")
    card("🧾", "Pedidos",    len(listar_pedidos()["data"]),    "#fb923c")
except:
    pass


janela.mainloop()