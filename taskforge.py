import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

COR_FUNDO = "#0b1122"
COR_TABELA = "#0d1c40"
COR_TITULO = "#00aaff"
COR_HEADER = "#003366"
COR_TEXTO = "#d0d0ff"
COR_SELECIONADO = "#330000"
COR_LINHA = "#112244"
COR_MAIS = "#ff3333"
COR_BOTAO_MAIS = "#220000"
COR_BOTAO_APAGAR = "#001122"

projetos = []
arquivo = "projects.json"

def salvar():
    with open(arquivo, "w") as f:
        json.dump(projetos, f, indent=4)

def carregar():
    global projetos
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            projetos = json.load(f)
    else:
        projetos = []

carregar()

root = tk.Tk()

# Ícone compatível com .exe (PyInstaller)
caminho_base = getattr(sys, "_MEIPASS", os.path.abspath("."))
icone_path = os.path.join(caminho_base, "icon.ico")
if os.path.exists(icone_path):
    root.iconbitmap(icone_path)

root.title("TaskForge")
root.geometry("700x600")
root.configure(bg=COR_FUNDO)

def centralizar(janela, largura, altura):
    x = root.winfo_screenwidth()//2 - largura//2
    y = root.winfo_screenheight()//2 - altura//2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def atualizar_tabela():
    tabela.delete(*tabela.get_children())
    if projetos:
        for tarefa in projetos[0]["tarefas"]:
            tabela.insert("", "end", values=(tarefa["titulo"], tarefa.get("etapa", ""), tarefa["status"]))

def abrir_formulario():
    janela = tk.Toplevel(root)
    centralizar(janela, 700, 550)
    janela.configure(bg="#020b30")
    janela.overrideredirect(True)

    frame = tk.Frame(janela, bg="#020b30")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="NOME", font=("Orbitron", 10), fg="#a0a0ff", bg="#020b30").pack(anchor="w")
    entry_nome = tk.Entry(frame, width=50)
    entry_nome.pack(pady=5)

    tk.Label(frame, text="ETAPA", font=("Orbitron", 10), fg="#a0a0ff", bg="#020b30").pack(anchor="w")
    entry_etapa = tk.Entry(frame, width=50)
    entry_etapa.pack(pady=5)

    tk.Label(frame, text="STATUS", font=("Orbitron", 10), fg="#a0a0ff", bg="#020b30").pack(anchor="w")
    combo_status = ttk.Combobox(frame, values=["em progresso", "pausado", "cancelado", "concluído"])
    combo_status.set("em progresso")
    combo_status.pack(pady=5)

    tk.Label(frame, text="DESCRIÇÃO", font=("Orbitron", 10), fg="#a0a0ff", bg="#020b30").pack(anchor="w")
    entry_desc = tk.Text(frame, width=50, height=6)
    entry_desc.pack(pady=5)

    def salvar_tarefa():
        nome = entry_nome.get().strip()
        etapa = entry_etapa.get().strip()
        status = combo_status.get()
        desc = entry_desc.get("1.0", tk.END).strip()
        if nome:
            projetos[0]["tarefas"].append({
                "titulo": nome,
                "etapa": etapa,
                "status": status,
                "descricao": desc
            })
            salvar()
            atualizar_tabela()
            janela.destroy()

    btn_salvar = tk.Button(janela, text="+", font=("Arial", 16, "bold"),
                           fg=COR_MAIS, bg=COR_BOTAO_MAIS, width=2,
                           command=salvar_tarefa, borderwidth=0, activebackground=COR_MAIS)
    btn_salvar.place(relx=0.88, rely=0.88)

def abrir_detalhes(event):
    item = tabela.identify_row(event.y)
    if not item:
        return
    valores = tabela.item(item, "values")
    titulo, etapa, status = valores
    for t in projetos[0]["tarefas"]:
        if t["titulo"] == titulo:
            tarefa = t
            break
    else:
        return

    janela = tk.Toplevel(root)
    centralizar(janela, 700, 550)
    janela.configure(bg="#020b30")
    janela.overrideredirect(True)

    frame = tk.Frame(janela, bg="#020b30")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="NOME", font=("Orbitron", 10), fg="#a0a0ff", bg="#020b30").pack(anchor="w")
    entry_nome = tk.Entry(frame, width=50)
    entry_nome.insert(0, tarefa["titulo"])
    entry_nome.pack(pady=5)

    tk.Label(frame, text="ETAPA", font=("Orbitron", 10), fg="#a0a0ff", bg="#020b30").pack(anchor="w")
    entry_etapa = tk.Entry(frame, width=50)
    entry_etapa.insert(0, tarefa.get("etapa", ""))
    entry_etapa.pack(pady=5)

    tk.Label(frame, text="STATUS", font=("Orbitron", 10), fg="#a0a0ff", bg="#020b30").pack(anchor="w")
    combo_status = ttk.Combobox(frame, values=["em progresso", "pausado", "cancelado", "concluído"])
    combo_status.set(tarefa["status"])
    combo_status.pack(pady=5)

    tk.Label(frame, text="DESCRIÇÃO", font=("Orbitron", 10), fg="#a0a0ff", bg="#020b30").pack(anchor="w")
    entry_desc = tk.Text(frame, width=50, height=6)
    entry_desc.insert("1.0", tarefa.get("descricao", ""))
    entry_desc.pack(pady=5)

    def salvar_edicao():
        tarefa["titulo"] = entry_nome.get().strip()
        tarefa["etapa"] = entry_etapa.get().strip()
        tarefa["status"] = combo_status.get()
        tarefa["descricao"] = entry_desc.get("1.0", tk.END).strip()
        salvar()
        atualizar_tabela()
        janela.destroy()

    btn_salvar = tk.Button(janela, text="SALVAR", font=("Orbitron", 12),
                           fg="white", bg=COR_BOTAO_APAGAR,
                           command=salvar_edicao)
    btn_salvar.pack(pady=5)

    janela.focus_set()
    janela.bind("<FocusOut>", lambda e: janela.destroy())

tk.Label(root, text="Tarefas", font=("Orbitron", 24), fg=COR_TITULO, bg=COR_FUNDO).pack(pady=10)

colunas = ("nome", "etapa", "status")
tabela = ttk.Treeview(root, columns=colunas, show="headings", selectmode="extended")
tabela.heading("nome", text="NOME")
tabela.heading("etapa", text="ETAPA")
tabela.heading("status", text="STATUS")
tabela.pack(pady=0, expand=True, fill="both")

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background=COR_TABELA,
    fieldbackground=COR_TABELA,
    foreground=COR_TEXTO,
    rowheight=35,
    font=("Orbitron", 10),
    borderwidth=0
)
style.map("Treeview", background=[("selected", COR_SELECIONADO)])
style.configure("Treeview.Heading",
    background=COR_HEADER,
    foreground=COR_TEXTO,
    font=("Orbitron", 11, "bold")
)

btn_frame = tk.Frame(root, bg=COR_FUNDO)
btn_frame.pack(fill="x", padx=20, pady=10)

btn_add = tk.Button(btn_frame, text="+", font=("Arial", 18, "bold"), fg=COR_MAIS,
                    bg=COR_BOTAO_MAIS, width=2, height=1, command=abrir_formulario,
                    borderwidth=0, activebackground=COR_MAIS)
btn_add.pack(side="right")

btn_apagar = tk.Button(root, text="APAGAR", font=("Orbitron", 12), bg=COR_BOTAO_APAGAR,
                       fg=COR_TEXTO, padx=20, pady=5)

def apagar_tarefas():
    selecionados = tabela.selection()
    if not selecionados:
        return
    if not messagebox.askyesno("Confirmar", "Deseja apagar as tarefas selecionadas?"):
        return
    for item in selecionados:
        nome = tabela.item(item, "values")[0]
        projetos[0]["tarefas"] = [t for t in projetos[0]["tarefas"] if t["titulo"] != nome]
    salvar()
    atualizar_tabela()
    btn_apagar.pack_forget()

btn_apagar.config(command=apagar_tarefas)

def ao_selecionar(event):
    if tabela.selection():
        btn_apagar.pack(pady=5)
    else:
        btn_apagar.pack_forget()

tabela.bind("<<TreeviewSelect>>", ao_selecionar)
tabela.bind("<Double-Button-1>", abrir_detalhes)

if not projetos:
    projetos.append({"nome": "Meu Projeto", "descricao": "", "tarefas": []})

atualizar_tabela()
root.mainloop()
