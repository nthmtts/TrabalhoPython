import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

tipos = {
    'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documentos': ['.pdf', '.docx', '.txt', '.pptx'],
    'Planilhas': ['.xlsx', '.xls', '.csv'],
    'Vídeos': ['.mp4', '.mov', '.avi'],
    'Compactados': ['.zip', '.rar', '.7z'],
    'Executáveis': ['.exe', '.msi', '.bat']
}

def organizar_pasta(caminho, lista_widget, barra_progresso):
    arquivos = os.listdir(caminho)
    total = len(arquivos)
    organizados = 0

    lista_widget.delete(0, tk.END)

    for arquivo in arquivos:
        caminho_completo = os.path.join(caminho, arquivo)

        if os.path.isfile(caminho_completo):
            nome, extensao = os.path.splitext(arquivo)
            movido = False

            for categoria, extensoes in tipos.items():
                if extensao.lower() in extensoes:
                    pasta_destino = os.path.join(caminho, categoria)
                    if not os.path.exists(pasta_destino):
                        os.makedirs(pasta_destino)

                    shutil.move(caminho_completo, os.path.join(pasta_destino, arquivo))
                    lista_widget.insert(tk.END, f"{arquivo} → {categoria}")
                    movido = True
                    break

            if not movido:
                pasta_outros = os.path.join(caminho, 'Outros')
                if not os.path.exists(pasta_outros):
                    os.makedirs(pasta_outros)
                shutil.move(caminho_completo, os.path.join(pasta_outros, arquivo))
                lista_widget.insert(tk.END, f"{arquivo} → Outros")

        organizados += 1
        barra_progresso['value'] = (organizados / total) * 100
        root.update_idletasks()

    messagebox.showinfo("Sucesso", "Organização concluída!")

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        caminho_var.set(pasta)
        status_var.set("Pasta selecionada: " + pasta)

def iniciar():
    pasta = caminho_var.get()
    if not pasta:
        messagebox.showwarning("Atenção", "Por favor, selecione uma pasta!")
        return
    try:
        barra_progresso['value'] = 0
        organizar_pasta(pasta, lista_arquivos, barra_progresso)
        status_var.set("Organização concluída!")
    except Exception as e:
        status_var.set(f"Erro: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

def on_enter(e):
    e.widget['background'] = '#7da6d8' 
def on_leave(e):
    e.widget['background'] = '#a3cef1'  

root = tk.Tk()
import sys

if hasattr(sys, '_MEIPASS'):
    caminho_icone = os.path.join(sys._MEIPASS, 'icone.ico')
else:
    caminho_icone = os.path.abspath("icone.ico")

try:
    root.iconbitmap(caminho_icone)
except Exception as e:
    print(f"Erro ao definir ícone: {e}")

root.title("Organizador de Pastas Visual")

try:
    root.iconbitmap('icone.ico')
except Exception:
    pass

window_width = 600
window_height = 550
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

root.configure(bg="#a3cef1")

caminho_var = tk.StringVar()
status_var = tk.StringVar()

style = ttk.Style(root)
style.theme_use('clam')
style.configure("TLabel", background="#a3cef1", foreground="#3d0066") 

welcome_label = tk.Label(root, text="Bem-vindo ao Organizador de Pastas!", 
                         font=("Segoe UI", 18, "bold"), bg="#a3cef1", fg="#000000")  
welcome_label.pack(pady=15)

frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill=tk.X)

label_selecione = ttk.Label(frame_top, text="Selecione a pasta para organizar:", font=("Calibri", 12, "bold"))
label_selecione.configure(foreground="#000000") 
label_selecione.pack(anchor='w')

entry_caminho = ttk.Entry(frame_top, textvariable=caminho_var, width=60, font=("Calibri", 11))
entry_caminho.pack(side=tk.LEFT, pady=5, padx=(0,10))

btn_escolher = tk.Button(frame_top, text="Escolher Pasta", bg="#a3cef1", fg="#000000",
                         font=("Segoe UI", 11, "bold"), relief='flat', padx=12, pady=6)
btn_escolher.pack(side=tk.LEFT)
btn_escolher.bind("<Button-1>", lambda e: escolher_pasta())
btn_escolher.bind("<Enter>", on_enter)
btn_escolher.bind("<Leave>", on_leave)

frame_middle = ttk.Frame(root, padding=10)
frame_middle.pack(fill=tk.X)

btn_organizar = tk.Button(frame_middle, text="Organizar", bg="#a3cef1", fg="#000000",
                          font=("Segoe UI", 13, "bold"), relief='flat', padx=20, pady=10)
btn_organizar.pack()
btn_organizar.bind("<Button-1>", lambda e: iniciar())
btn_organizar.bind("<Enter>", on_enter)
btn_organizar.bind("<Leave>", on_leave)

barra_progresso = ttk.Progressbar(root, orient="horizontal", length=560, mode="determinate")
barra_progresso.pack(pady=15)

label_arquivos = ttk.Label(root, text="Arquivos organizados:", font=("Calibri", 12, "bold"))
label_arquivos.configure(foreground="#000000") 
label_arquivos.pack(anchor='w', padx=10)

frame_list = ttk.Frame(root)
frame_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

lista_arquivos = tk.Listbox(frame_list, font=("Calibri", 10), fg="#FFFFFF", bg="#000000", selectbackground="#5555aa")
lista_arquivos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=lista_arquivos.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_arquivos.config(yscrollcommand=scrollbar.set)

status_label = ttk.Label(root, textvariable=status_var, font=("Calibri", 10, "italic"), foreground="#3d0066", background="#a3cef1")
status_label.pack(pady=(0,10))

root.mainloop()
