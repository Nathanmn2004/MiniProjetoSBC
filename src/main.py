from pathlib import Path
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from fuzzy_controller import calcular_risco_nocaute


ROOT_DIR = Path(__file__).resolve().parent.parent
IMGS_DIR = ROOT_DIR / "imgs"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".jfif", ".webp", ".bmp")


class UFCNocauteApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Risco de Nocaute UFC")
        self.geometry("780x460")
        self.minsize(720, 420)

        self.dano = tk.DoubleVar(value=5)
        self.fadiga = tk.DoubleVar(value=5)
        self.resultado = tk.StringVar(value="Informe os valores e clique em Calcular.")
        self.imagem_tk = None

        self._configurar_estilo()
        self._montar_interface()
        self._carregar_imagem()

    def _configurar_estilo(self):
        self.configure(bg="#111827")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#111827")
        style.configure("Card.TFrame", background="#1f2937")
        style.configure("TLabel", background="#111827", foreground="#f9fafb", font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Card.TLabel", background="#1f2937", foreground="#f9fafb", font=("Segoe UI", 11))
        style.configure("Result.TLabel", background="#1f2937", foreground="#facc15", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8)

    def _montar_interface(self):
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(1, weight=1)

        titulo = ttk.Label(
            container,
            text="Sistema Fuzzy para Risco de Nocaute",
            style="Title.TLabel",
        )
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))

        controles = ttk.Frame(container, style="Card.TFrame", padding=18)
        controles.grid(row=1, column=0, sticky="nsew", padx=(0, 16))
        controles.columnconfigure(1, weight=1)

        self._criar_controle(controles, "Dano recebido", self.dano, 0)
        self._criar_controle(controles, "Fadiga", self.fadiga, 1)

        botao = ttk.Button(controles, text="Calcular risco", command=self.calcular)
        botao.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(18, 14))

        resultado = ttk.Label(
            controles,
            textvariable=self.resultado,
            style="Result.TLabel",
            justify="center",
            anchor="center",
            wraplength=420,
        )
        resultado.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 0))

        imagem_card = ttk.Frame(container, style="Card.TFrame", padding=12)
        imagem_card.grid(row=1, column=1, sticky="nsew")
        imagem_card.columnconfigure(0, weight=1)
        imagem_card.rowconfigure(0, weight=1)

        self.imagem_label = ttk.Label(
            imagem_card,
            text="Nenhuma imagem encontrada em imgs/",
            style="Card.TLabel",
            anchor="center",
            justify="center",
        )
        self.imagem_label.grid(row=0, column=0, sticky="nsew")

    def _criar_controle(self, parent, texto, variavel, linha):
        linha_base = linha * 2

        label = ttk.Label(parent, text=f"{texto} (0 a 10)", style="Card.TLabel")
        label.grid(row=linha_base, column=0, columnspan=3, sticky="w", pady=(0 if linha == 0 else 18, 6))

        slider = tk.Scale(
            parent,
            from_=0,
            to=10,
            resolution=0.1,
            orient="horizontal",
            variable=variavel,
            bg="#1f2937",
            fg="#f9fafb",
            troughcolor="#374151",
            highlightthickness=0,
            activebackground="#facc15",
        )
        slider.grid(row=linha_base + 1, column=0, columnspan=2, sticky="ew", padx=(0, 12))

        spinbox = ttk.Spinbox(
            parent,
            from_=0,
            to=10,
            increment=0.1,
            textvariable=variavel,
            width=7,
            format="%.1f",
            command=self._limitar_valores,
        )
        spinbox.grid(row=linha_base + 1, column=2, sticky="e")
        spinbox.bind("<FocusOut>", lambda _event: self._limitar_valores())
        spinbox.bind("<Return>", lambda _event: self._limitar_valores())

    def _carregar_imagem(self):
        imagens = sorted(
            arquivo for arquivo in IMGS_DIR.iterdir()
            if arquivo.is_file() and arquivo.suffix.lower() in IMAGE_EXTENSIONS
        ) if IMGS_DIR.exists() else []

        if not imagens:
            return

        imagem = Image.open(imagens[0])
        imagem.thumbnail((300, 330), Image.Resampling.LANCZOS)
        self.imagem_tk = ImageTk.PhotoImage(imagem)
        self.imagem_label.configure(image=self.imagem_tk, text="")

    def _limitar_valores(self):
        for variavel in (self.dano, self.fadiga):
            try:
                valor = float(variavel.get())
            except (tk.TclError, ValueError):
                valor = 0

            variavel.set(min(10, max(0, valor)))

    def calcular(self):
        self._limitar_valores()

        dano = self.dano.get()
        fadiga = self.fadiga.get()
        risco, classificacao = calcular_risco_nocaute(dano, fadiga)

        self.resultado.set(
            f"Risco de nocaute: {risco:.2f}%\n"
            f"Classificacao: {classificacao}"
        )


def main():
    app = UFCNocauteApp()
    app.mainloop()


if __name__ == "__main__":
    main()
