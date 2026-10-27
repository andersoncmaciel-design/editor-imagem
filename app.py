
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk, ImageEnhance


class EditorFotos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Meu Editor de Fotos")
        self.janela.geometry("950x750")

        # Estado inicial do editor
        self.original = None
        self.foto_tela = None
        self.rotacao = 0
        self.preto_branco = False

        # Área de visualização da fotografia
        self.area_imagem = tk.Label(
            janela, text="Abra uma fotografia para começar"
        )
        self.area_imagem.pack(pady=15)

        # Botões principais
        controles = tk.Frame(janela)
        controles.pack(pady=5)

        tk.Button(
            controles, text="Abrir foto",
            command=self.abrir_foto
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            controles, text="Girar 90°",
            command=self.girar
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            controles, text="Preto e branco",
            command=self.alternar_preto_branco
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            controles, text="Restaurar",
            command=self.restaurar
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            controles, text="Salvar como",
            command=self.salvar_foto
        ).grid(row=0, column=4, padx=5)

        # Controle de brilho
        tk.Label(janela, text="Brilho").pack()

        self.controle_brilho = tk.Scale(
            janela, from_=0.2, to=2.0,
            resolution=0.1, orient=tk.HORIZONTAL,
            command=self.atualizar_preview
        )
        self.controle_brilho.set(1.0)
        self.controle_brilho.pack()

        # Controle de contraste
        tk.Label(janela, text="Contraste").pack()

        self.controle_contraste = tk.Scale(
            janela, from_=0.2, to=2.0,
            resolution=0.1, orient=tk.HORIZONTAL,
            command=self.atualizar_preview
        )
        self.controle_contraste.set(1.0)
        self.controle_contraste.pack()

    def abrir_foto(self):
        caminho = filedialog.askopenfilename(
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not caminho:
            return

        try:
            self.original = Image.open(caminho).convert("RGB")
            self.restaurar()
        except Exception as erro:
            messagebox.showerror(
                "Erro", f"Não foi possível abrir a imagem:\n{erro}"
            )

    def processar_foto(self):
        if self.original is None:
            return None

        # Trabalhamos em uma cópia da imagem original
        imagem = self.original.copy()

        # Converte para preto e branco, se solicitado
        if self.preto_branco:
            imagem = imagem.convert("L").convert("RGB")

        # Aplica os ajustes de brilho e contraste
        brilho = self.controle_brilho.get()
        contraste = self.controle_contraste.get()

        imagem = ImageEnhance.Brightness(imagem).enhance(brilho)
        imagem = ImageEnhance.Contrast(imagem).enhance(contraste)

        # Gira a imagem sem alterar o arquivo original
        if self.rotacao:
            imagem = imagem.rotate(self.rotacao, expand=True)

        return imagem

    def atualizar_preview(self, valor=None):
        imagem = self.processar_foto()

        if imagem is None:
            return

        # Redimensiona apenas a cópia destinada à tela
        previa = imagem.copy()
        previa.thumbnail((850, 520))

        self.foto_tela = ImageTk.PhotoImage(previa)
        self.area_imagem.configure(image=self.foto_tela, text="")

    def girar(self):
        if self.original is None:
            return

        self.rotacao = (self.rotacao + 90) % 360
        self.atualizar_preview()

    def alternar_preto_branco(self):
        if self.original is None:
            return

        self.preto_branco = not self.preto_branco
        self.atualizar_preview()

    def restaurar(self):
        self.rotacao = 0
        self.preto_branco = False
        self.controle_brilho.set(1.0)
        self.controle_contraste.set(1.0)
        self.atualizar_preview()

    def salvar_foto(self):
        imagem = self.processar_foto()

        if imagem is None:
            messagebox.showwarning(
                "Atenção", "Abra uma fotografia primeiro."
            )
            return

        caminho = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("WebP", "*.webp")
            ]
        )

        if not caminho:
            return

        try:
            # JPEG não suporta transparência; a imagem está em RGB
            imagem.save(caminho)
            messagebox.showinfo(
                "Sucesso", "Fotografia salva com sucesso!"
            )
        except Exception as erro:
            messagebox.showerror(
                "Erro", f"Não foi possível salvar:\n{erro}"
            )


if __name__ == "__main__":
    janela = tk.Tk()
    aplicativo = EditorFotos(janela)
    janela.mainloop()
