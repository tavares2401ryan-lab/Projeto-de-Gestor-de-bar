from tkinter import *
from tkinter import ttk, messagebox

from cliente import listar_clientes, criar_cliente, atualizar_cliente, remover_cliente, obter_cliente
from produtos import listar_produtos, criar_produto, atualizar_produto, remover_produto
from atendente import listar_atendentes, criar_atendente, atualizar_atendente, remover_atendente
from pedidos import listar_pedidos, criar_pedido, atualizar_pedido, remover_pedido, obter_pedido


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

Label(header, text="🍺  SISTEMA DE GESTÃO DE BAR",
      bg="#1d4ed8", fg="white",
      font=("Arial", 17, "bold")).pack(side=LEFT, padx=25, pady=18)

Label(header, text="Bar Manager v1.0",
      bg="#1d4ed8", fg="#bfdbfe",
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
    b = Button(sidebar, text=text, command=cmd,
               bg="#0b1220", fg="#e2e8f0",
               activebackground="#1e293b", activeforeground="white",
               relief=FLAT, pady=11, width=22,
               anchor=W, padx=18, font=("Arial", 10), cursor="hand2")
    b.pack(fill=X, pady=1)
    b.bind("<Enter>", lambda e: b.configure(bg="#1e293b"))
    b.bind("<Leave>", lambda e: b.configure(bg="#0b1220"))


sidebar_btn("  👥  Clientes",    lambda: abrir_tabela_clientes())
sidebar_btn("  🍺  Produtos",    lambda: abrir_tabela_produtos())
sidebar_btn("  🧑‍🍳  Atendentes",  lambda: abrir_tabela_atendentes())
sidebar_btn("  🧾  Pedidos",     lambda: abrir_tabela_pedidos())

Frame(sidebar, bg="#1e293b", height=1).pack(fill=X, padx=15, pady=20)

b_sair = Button(sidebar, text="  ❌  Sair", command=janela.destroy,
                bg="#0b1220", fg="#f87171",
                activebackground="#1e293b", activeforeground="#f87171",
                relief=FLAT, pady=11, width=22,
                anchor=W, padx=18, font=("Arial", 10), cursor="hand2")
b_sair.pack(fill=X, pady=1)


# =========================
# HELPERS
# =========================

def criar_tabela(parent, cols):
    frame = Frame(parent, bg="#0f172a")
    frame.pack(fill=BOTH, expand=True, padx=25, pady=(10, 0))

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
    tabela.delete(*tabela.get_children())
    for i, row in enumerate(rows):
        tabela.insert("", END, iid=row[0], values=row[1:],
                      tags=("odd" if i % 2 == 0 else "even",))


def frame_btns(parent):
    f = Frame(parent, bg="#0f172a")
    f.pack(pady=10)
    return f


def action_btn(parent, texto, cmd, cor="#1d4ed8"):
    Button(parent, text=texto, command=cmd,
           bg=cor, fg="white", relief=FLAT,
           padx=14, pady=6, cursor="hand2",
           font=("Arial", 9)).pack(side=LEFT, padx=5)


def titulo(win, texto):
    Label(win, text=texto, bg="#0f172a", fg="white",
          font=("Arial", 15, "bold")).pack(anchor=W, padx=25, pady=(20, 5))


# =========================
# CLIENTES
# =========================

def abrir_tabela_clientes():
    win = Toplevel(janela)
    win.state("zoomed")
    win.title("Clientes")
    win.configure(bg="#0f172a")

    titulo(win, "👥  Clientes")
    tabela = criar_tabela(win, ("Nome", "Telefone", "Email", "NIF"))

    def carregar():
        data = listar_clientes()
        if data and "data" in data:
            preencher(tabela, [(c["id"], c["nome"], c["telefone"], c["email"], c["nif"])
                               for c in data["data"]])

    carregar()

    def abrir_form(cliente=None):
        form = Toplevel(win)
        form.title("Novo Cliente" if not cliente else "Editar Cliente")
        form.geometry("320x280")
        form.configure(bg="#0f172a")
        form.grab_set()

        campos = {}
        for label in ("Nome", "Telefone", "Email", "NIF"):
            Label(form, text=label, bg="#0f172a", fg="#94a3b8",
                  font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
            e = Entry(form, width=36, bg="#1e293b", fg="white",
                      insertbackground="white", relief=FLAT)
            e.pack(padx=20, ipady=5)
            campos[label] = e

        if cliente:
            campos["Nome"].insert(0,     cliente["nome"])
            campos["Telefone"].insert(0, cliente["telefone"])
            campos["Email"].insert(0,    cliente["email"])
            campos["NIF"].insert(0,      cliente["nif"])

        def guardar():
            if cliente:
                res = atualizar_cliente(cliente["id"],
                    novo_nome=campos["Nome"].get(),
                    novo_telefone=campos["Telefone"].get(),
                    novo_email=campos["Email"].get(),
                    novo_nif=campos["NIF"].get())
            else:
                res = criar_cliente(campos["Nome"].get(), campos["Telefone"].get(),
                    campos["Email"].get(), campos["NIF"].get())
            if res["status"] in (200, 201):
                carregar()
                form.destroy()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"), parent=form)

        Button(form, text="Guardar", command=guardar,
               bg="#1d4ed8", fg="white", relief=FLAT,
               padx=14, pady=6, cursor="hand2").pack(pady=16)

    def editar():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um cliente.")
            return
        res = obter_cliente(sel[0])
        if res["status"] == 200:
            abrir_form(res["data"])

    def remover():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um cliente.")
            return
        if messagebox.askyesno("Confirmar", "Remover este cliente?"):
            res = remover_cliente(sel[0])
            if res["status"] == 200:
                carregar()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"))

    fb = frame_btns(win)
    action_btn(fb, "➕  Novo",    lambda: abrir_form())
    action_btn(fb, "✏️  Editar",  editar)
    action_btn(fb, "🗑️  Remover", remover, "#dc2626")


# =========================
# PRODUTOS
# =========================

def abrir_tabela_produtos():
    win = Toplevel(janela)
    win.state("zoomed")
    win.title("Produtos")
    win.configure(bg="#0f172a")

    titulo(win, "🍺  Produtos")
    tabela = criar_tabela(win, ("Nome", "Categoria", "Preço"))

    def carregar():
        data = listar_produtos()
        if data and "data" in data:
            preencher(tabela, [(p["id"], p["nome"], p["categoria"], f"€ {p['preco']:.2f}")
                               for p in data["data"]])

    carregar()

    def abrir_form(produto=None):
        form = Toplevel(win)
        form.title("Novo Produto" if not produto else "Editar Produto")
        form.geometry("320x240")
        form.configure(bg="#0f172a")
        form.grab_set()

        Label(form, text="Nome", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
        e_nome = Entry(form, width=36, bg="#1e293b", fg="white",
                       insertbackground="white", relief=FLAT)
        e_nome.pack(padx=20, ipady=5)

        Label(form, text="Preço (€)", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
        e_preco = Entry(form, width=36, bg="#1e293b", fg="white",
                        insertbackground="white", relief=FLAT)
        e_preco.pack(padx=20, ipady=5)

        Label(form, text="Categoria", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
        var_cat = StringVar()
        combo = ttk.Combobox(form, textvariable=var_cat,
                             values=("Bebida", "Comida", "Sobremesa", "Snack"),
                             state="readonly", width=33)
        combo.pack(padx=20)

        if produto:
            e_nome.insert(0, produto["nome"])
            e_preco.insert(0, produto["preco"])
            var_cat.set(produto["categoria"])

        def guardar():
            try:
                preco = float(e_preco.get())
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido.", parent=form)
                return
            if not var_cat.get():
                messagebox.showwarning("Atenção", "Seleciona a categoria.", parent=form)
                return
            if produto:
                res = atualizar_produto(produto["id"], novo_nome=e_nome.get(),
                    novo_preco=preco, nova_categoria=var_cat.get())
            else:
                res = criar_produto(e_nome.get(), preco, var_cat.get())
            if res["status"] in (200, 201):
                carregar()
                form.destroy()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"), parent=form)

        Button(form, text="Guardar", command=guardar,
               bg="#1d4ed8", fg="white", relief=FLAT,
               padx=14, pady=6, cursor="hand2").pack(pady=16)

    def editar():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um produto.")
            return
        for p in listar_produtos()["data"]:
            if p["id"] == sel[0]:
                abrir_form(p)
                return

    def remover():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um produto.")
            return
        if messagebox.askyesno("Confirmar", "Remover este produto?"):
            res = remover_produto(sel[0])
            if res["status"] == 200:
                carregar()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"))

    fb = frame_btns(win)
    action_btn(fb, "➕  Novo",    lambda: abrir_form())
    action_btn(fb, "✏️  Editar",  editar)
    action_btn(fb, "🗑️  Remover", remover, "#dc2626")


# =========================
# ATENDENTES
# =========================

def abrir_tabela_atendentes():
    win = Toplevel(janela)
    win.state("zoomed")
    win.title("Atendentes")
    win.configure(bg="#0f172a")

    titulo(win, "🧑‍🍳  Atendentes")
    tabela = criar_tabela(win, ("Nome", "Tipo", "Nascimento"))

    def carregar():
        data = listar_atendentes()
        if data and "data" in data:
            preencher(tabela, [(a["id"], a["nome"], a["tipo"], a["data_nascimento"])
                               for a in data["data"]])

    carregar()

    def abrir_form(atendente=None):
        form = Toplevel(win)
        form.title("Novo Atendente" if not atendente else "Editar Atendente")
        form.geometry("320x240")
        form.configure(bg="#0f172a")
        form.grab_set()

        Label(form, text="Nome", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
        e_nome = Entry(form, width=36, bg="#1e293b", fg="white",
                       insertbackground="white", relief=FLAT)
        e_nome.pack(padx=20, ipady=5)

        Label(form, text="Tipo", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
        var_tipo = StringVar()
        combo = ttk.Combobox(form, textvariable=var_tipo,
                             values=("Empregado", "Gerente", "Barman"),
                             state="readonly", width=33)
        combo.pack(padx=20)

        Label(form, text="Data Nascimento (AAAA-MM-DD)", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
        e_nasc = Entry(form, width=36, bg="#1e293b", fg="white",
                       insertbackground="white", relief=FLAT)
        e_nasc.pack(padx=20, ipady=5)

        if atendente:
            e_nome.insert(0, atendente["nome"])
            var_tipo.set(atendente["tipo"])
            e_nasc.insert(0, atendente["data_nascimento"])

        def guardar():
            if not var_tipo.get():
                messagebox.showwarning("Atenção", "Seleciona o tipo.", parent=form)
                return
            if atendente:
                res = atualizar_atendente(atendente["id"], novo_nome=e_nome.get())
            else:
                res = criar_atendente(e_nome.get(), var_tipo.get(), e_nasc.get())
            if res["status"] in (200, 201):
                carregar()
                form.destroy()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"), parent=form)

        Button(form, text="Guardar", command=guardar,
               bg="#1d4ed8", fg="white", relief=FLAT,
               padx=14, pady=6, cursor="hand2").pack(pady=16)

    def editar():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um atendente.")
            return
        for a in listar_atendentes()["data"]:
            if a["id"] == sel[0]:
                abrir_form(a)
                return

    def remover():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um atendente.")
            return
        if messagebox.askyesno("Confirmar", "Remover este atendente?"):
            res = remover_atendente(sel[0])
            if res["status"] == 200:
                carregar()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"))

    fb = frame_btns(win)
    action_btn(fb, "➕  Novo",    lambda: abrir_form())
    action_btn(fb, "✏️  Editar",  editar)
    action_btn(fb, "🗑️  Remover", remover, "#dc2626")


# =========================
# PEDIDOS
# =========================

def abrir_tabela_pedidos():
    win = Toplevel(janela)
    win.state("zoomed")
    win.title("Pedidos")
    win.configure(bg="#0f172a")

    titulo(win, "🧾  Pedidos")
    tabela = criar_tabela(win, ("Cliente", "Atendente", "Total"))

    clientes_d   = listar_clientes()["data"]
    atendentes_d = listar_atendentes()["data"]
    produtos_d   = listar_produtos()["data"]

    def id_nome(lista, vid):
        for x in lista:
            if x["id"] == vid:
                return x["nome"]
        return vid

    def carregar():
        data = listar_pedidos()
        if data and "data" in data:
            preencher(tabela, [(p["id"],
                                id_nome(clientes_d, p["cliente"]),
                                id_nome(atendentes_d, p["atendente"]),
                                f"€ {p['valor_total']:.2f}")
                               for p in data["data"]])

    carregar()

    def abrir_form(pedido=None):
        form = Toplevel(win)
        form.title("Novo Pedido" if not pedido else "Editar Pedido")
        form.geometry("360x460")
        form.configure(bg="#0f172a")
        form.grab_set()

        Label(form, text="Cliente", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
        var_c = StringVar()
        combo_c = ttk.Combobox(form, textvariable=var_c,
                               values=[c["nome"] for c in clientes_d],
                               state="readonly", width=38)
        combo_c.pack(padx=20)

        Label(form, text="Atendente", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))
        var_a = StringVar()
        combo_a = ttk.Combobox(form, textvariable=var_a,
                               values=[a["nome"] for a in atendentes_d],
                               state="readonly", width=38)
        combo_a.pack(padx=20)

        Label(form, text="Produtos", bg="#0f172a", fg="#94a3b8",
              font=("Arial", 9)).pack(anchor=W, padx=20, pady=(10, 0))

        frame_p = Frame(form, bg="#0f172a")
        frame_p.pack(fill=BOTH, expand=True, padx=20)

        vars_qtd = {}
        for prod in produtos_d:
            linha = Frame(frame_p, bg="#0f172a")
            linha.pack(fill=X, pady=2)
            Label(linha, text=prod["nome"], width=20, anchor=W,
                  bg="#0f172a", fg="white", font=("Arial", 9)).pack(side=LEFT)
            v = IntVar(value=0)
            vars_qtd[prod["id"]] = v
            Spinbox(linha, from_=0, to=99, width=5, textvariable=v,
                    bg="#1e293b", fg="white", buttonbackground="#1e293b",
                    relief=FLAT).pack(side=LEFT, padx=6)
            Label(linha, text=f"€{prod['preco']:.2f}",
                  bg="#0f172a", fg="#64748b", font=("Arial", 9)).pack(side=LEFT)

        if pedido:
            idx_c = next((i for i, c in enumerate(clientes_d) if c["id"] == pedido["cliente"]), None)
            idx_a = next((i for i, a in enumerate(atendentes_d) if a["id"] == pedido["atendente"]), None)
            if idx_c is not None: combo_c.current(idx_c)
            if idx_a is not None: combo_a.current(idx_a)
            for item in pedido.get("produtos", []):
                if item["id"] in vars_qtd:
                    vars_qtd[item["id"]].set(item["quantidade"])

        def guardar():
            if combo_c.current() < 0 or combo_a.current() < 0:
                messagebox.showwarning("Atenção", "Seleciona cliente e atendente.", parent=form)
                return
            lista_p = [{"id": pid, "quantidade": v.get()}
                       for pid, v in vars_qtd.items() if v.get() > 0]
            if not lista_p:
                messagebox.showwarning("Atenção", "Adiciona pelo menos um produto.", parent=form)
                return
            id_c = clientes_d[combo_c.current()]["id"]
            id_a = atendentes_d[combo_a.current()]["id"]
            if pedido:
                res = atualizar_pedido(pedido["id"], novos_produtos=lista_p)
            else:
                res = criar_pedido(id_c, id_a, lista_p)
            if res["status"] in (200, 201):
                carregar()
                form.destroy()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"), parent=form)

        Button(form, text="Guardar", command=guardar,
               bg="#1d4ed8", fg="white", relief=FLAT,
               padx=14, pady=6, cursor="hand2").pack(pady=10)

    def editar():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um pedido.")
            return
        res = obter_pedido(sel[0])
        if res["status"] == 200:
            abrir_form(res["data"])

    def remover():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Seleciona um pedido.")
            return
        if messagebox.askyesno("Confirmar", "Remover este pedido?"):
            res = remover_pedido(sel[0])
            if res["status"] == 200:
                carregar()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"))

    fb = frame_btns(win)
    action_btn(fb, "➕  Novo",    lambda: abrir_form())
    action_btn(fb, "✏️  Editar",  editar)
    action_btn(fb, "🗑️  Remover", remover, "#dc2626")


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