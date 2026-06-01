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
janela.title("Sistema de Gestão de Bar")
janela.geometry("400x380")
janela.configure(bg="#f5f5f5")
janela.resizable(False, False)

# =========================
# HELPER - TABELA + BOTÕES
# =========================

def fazer_janela(titulo, colunas):
    nova = Toplevel()
    nova.title(titulo)
    nova.geometry("700x420")
    nova.configure(bg="#f5f5f5")

    frame = Frame(nova, bg="#f5f5f5")
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    tabela = ttk.Treeview(frame, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=150)

    scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)
    tabela.pack(side=LEFT, fill=BOTH, expand=True)
    scroll.pack(side=RIGHT, fill=Y)

    frame_btns = Frame(nova, bg="#f5f5f5")
    frame_btns.pack(pady=8)

    return nova, tabela, frame_btns


def btn(parent, texto, comando, cor="#4CAF50"):
    Button(
        parent, text=texto, command=comando,
        bg=cor, fg="white", relief=FLAT,
        padx=12, pady=4, cursor="hand2"
    ).pack(side=LEFT, padx=4)


# =========================
# CLIENTES
# =========================

def abrir_clientes():
    nova, tabela, frame_btns = fazer_janela("Clientes", ("Nome", "Telefone", "Email", "NIF"))

    def carregar():
        tabela.delete(*tabela.get_children())
        for c in listar_clientes()["data"]:
            tabela.insert("", END, iid=c["id"], values=(c["nome"], c["telefone"], c["email"], c["nif"]))

    carregar()

    def abrir_form(cliente=None):
        form = Toplevel(nova)
        form.title("Novo Cliente" if not cliente else "Editar Cliente")
        form.geometry("300x260")
        form.configure(bg="#f5f5f5")
        form.grab_set()

        campos = {}
        for label in ("Nome", "Telefone", "Email", "NIF"):
            Label(form, text=label, bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
            e = Entry(form, width=35)
            e.pack(padx=15)
            campos[label] = e

        if cliente:
            campos["Nome"].insert(0, cliente["nome"])
            campos["Telefone"].insert(0, cliente["telefone"])
            campos["Email"].insert(0, cliente["email"])
            campos["NIF"].insert(0, cliente["nif"])

        def guardar():
            if cliente:
                res = atualizar_cliente(cliente["id"], novo_nome=campos["Nome"].get(),
                    novo_telefone=campos["Telefone"].get(), novo_email=campos["Email"].get(),
                    novo_nif=campos["NIF"].get())
            else:
                res = criar_cliente(campos["Nome"].get(), campos["Telefone"].get(),
                    campos["Email"].get(), campos["NIF"].get())
            if res["status"] in (200, 201):
                carregar()
                form.destroy()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"), parent=form)

        Button(form, text="Guardar", command=guardar, bg="#4CAF50",
               fg="white", relief=FLAT, padx=12, pady=4).pack(pady=14)

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

    btn(frame_btns, "Novo",    lambda: abrir_form())
    btn(frame_btns, "Editar",  editar)
    btn(frame_btns, "Remover", remover, "#e53935")


# =========================
# PRODUTOS
# =========================

def abrir_produtos():
    nova, tabela, frame_btns = fazer_janela("Produtos", ("Nome", "Preço", "Categoria"))

    def carregar():
        tabela.delete(*tabela.get_children())
        for p in listar_produtos()["data"]:
            tabela.insert("", END, iid=p["id"], values=(p["nome"], f"€{p['preco']:.2f}", p["categoria"]))

    carregar()

    def abrir_form(produto=None):
        form = Toplevel(nova)
        form.title("Novo Produto" if not produto else "Editar Produto")
        form.geometry("300x240")
        form.configure(bg="#f5f5f5")
        form.grab_set()

        Label(form, text="Nome", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
        e_nome = Entry(form, width=35)
        e_nome.pack(padx=15)

        Label(form, text="Preço", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
        e_preco = Entry(form, width=35)
        e_preco.pack(padx=15)

        Label(form, text="Categoria", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
        e_cat = Entry(form, width=35)
        e_cat.pack(padx=15)

        if produto:
            e_nome.insert(0, produto["nome"])
            e_preco.insert(0, produto["preco"])
            e_cat.insert(0, produto["categoria"])

        def guardar():
            try:
                preco = float(e_preco.get())
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido.", parent=form)
                return
            if produto:
                res = atualizar_produto(produto["id"], novo_nome=e_nome.get(),
                    novo_preco=preco, nova_categoria=e_cat.get())
            else:
                res = criar_produto(e_nome.get(), preco, e_cat.get())
            if res["status"] in (200, 201):
                carregar()
                form.destroy()
            else:
                messagebox.showerror("Erro", res.get("erro", "Erro"), parent=form)

        Button(form, text="Guardar", command=guardar, bg="#4CAF50",
               fg="white", relief=FLAT, padx=12, pady=4).pack(pady=14)

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

    btn(frame_btns, "Novo",    lambda: abrir_form())
    btn(frame_btns, "Editar",  editar)
    btn(frame_btns, "Remover", remover, "#e53935")


# =========================
# ATENDENTES
# =========================

def abrir_atendentes():
    nova, tabela, frame_btns = fazer_janela("Atendentes", ("Nome", "Tipo", "Nascimento"))

    def carregar():
        tabela.delete(*tabela.get_children())
        for a in listar_atendentes()["data"]:
            tabela.insert("", END, iid=a["id"], values=(a["nome"], a["tipo"], a["data_nascimento"]))

    carregar()

    def abrir_form(atendente=None):
        form = Toplevel(nova)
        form.title("Novo Atendente" if not atendente else "Editar Atendente")
        form.geometry("300x220")
        form.configure(bg="#f5f5f5")
        form.grab_set()

        Label(form, text="Nome", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
        e_nome = Entry(form, width=35)
        e_nome.pack(padx=15)

        Label(form, text="Tipo", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
        var_tipo = StringVar()
        combo = ttk.Combobox(form, textvariable=var_tipo,
            values=("Empregado", "Gerente", "Barman"), state="readonly", width=32)
        combo.pack(padx=15)

        Label(form, text="Data Nascimento (AAAA-MM-DD)", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
        e_nasc = Entry(form, width=35)
        e_nasc.pack(padx=15)

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

        Button(form, text="Guardar", command=guardar, bg="#4CAF50",
               fg="white", relief=FLAT, padx=12, pady=4).pack(pady=14)

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

    btn(frame_btns, "Novo",    lambda: abrir_form())
    btn(frame_btns, "Editar",  editar)
    btn(frame_btns, "Remover", remover, "#e53935")


# =========================
# PEDIDOS
# =========================

def abrir_pedidos():
    nova, tabela, frame_btns = fazer_janela("Pedidos", ("Cliente", "Atendente", "Total"))

    clientes_d   = listar_clientes()["data"]
    atendentes_d = listar_atendentes()["data"]
    produtos_d   = listar_produtos()["data"]

    def id_nome(lista, vid):
        for x in lista:
            if x["id"] == vid:
                return x["nome"]
        return vid

    def carregar():
        tabela.delete(*tabela.get_children())
        for p in listar_pedidos()["data"]:
            tabela.insert("", END, iid=p["id"], values=(
                id_nome(clientes_d, p["cliente"]),
                id_nome(atendentes_d, p["atendente"]),
                f"€{p['valor_total']:.2f}"
            ))

    carregar()

    def abrir_form(pedido=None):
        form = Toplevel(nova)
        form.title("Novo Pedido" if not pedido else "Editar Pedido")
        form.geometry("380x460")
        form.configure(bg="#f5f5f5")
        form.grab_set()

        Label(form, text="Cliente", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
        var_c = StringVar()
        combo_c = ttk.Combobox(form, textvariable=var_c,
            values=[c["nome"] for c in clientes_d], state="readonly", width=38)
        combo_c.pack(padx=15)

        Label(form, text="Atendente", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))
        var_a = StringVar()
        combo_a = ttk.Combobox(form, textvariable=var_a,
            values=[a["nome"] for a in atendentes_d], state="readonly", width=38)
        combo_a.pack(padx=15)

        Label(form, text="Produtos (quantidade)", bg="#f5f5f5").pack(anchor=W, padx=15, pady=(8,0))

        frame_p = Frame(form, bg="#f5f5f5")
        frame_p.pack(fill=BOTH, expand=True, padx=15)

        vars_qtd = {}
        for prod in produtos_d:
            linha = Frame(frame_p, bg="#f5f5f5")
            linha.pack(fill=X, pady=1)
            Label(linha, text=prod["nome"], width=20, anchor=W, bg="#f5f5f5").pack(side=LEFT)
            v = IntVar(value=0)
            vars_qtd[prod["id"]] = v
            Spinbox(linha, from_=0, to=99, width=5, textvariable=v).pack(side=LEFT, padx=4)
            Label(linha, text=f"€{prod['preco']:.2f}", fg="gray", bg="#f5f5f5").pack(side=LEFT)

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
            lista_p = [{"id": pid, "quantidade": v.get()} for pid, v in vars_qtd.items() if v.get() > 0]
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

        Button(form, text="Guardar", command=guardar, bg="#4CAF50",
               fg="white", relief=FLAT, padx=12, pady=4).pack(pady=10)

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

    btn(frame_btns, "Novo",    lambda: abrir_form())
    btn(frame_btns, "Editar",  editar)
    btn(frame_btns, "Remover", remover, "#e53935")


# =========================
# MENU PRINCIPAL
# =========================

Label(janela, text="🍺 Gestão de Bar", font=("Arial", 20, "bold"),
      bg="#f5f5f5", fg="#333").pack(pady=30)

for texto, comando in [
    ("Clientes",   abrir_clientes),
    ("Produtos",   abrir_produtos),
    ("Atendentes", abrir_atendentes),
    ("Pedidos",    abrir_pedidos),
]:
    Button(janela, text=texto, command=comando, width=22,
           bg="white", fg="#333", relief=FLAT, pady=8,
           font=("Arial", 11), cursor="hand2",
           highlightthickness=1, highlightbackground="#ddd"
    ).pack(pady=4)

Button(janela, text="Sair", command=janela.destroy, width=22,
       bg="#e53935", fg="white", relief=FLAT, pady=8,
       font=("Arial", 11), cursor="hand2"
).pack(pady=16)

janela.mainloop()