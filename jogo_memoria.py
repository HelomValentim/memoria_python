import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time

class MemoryGame:
    def __init__(self, root, images):
        self.root = root
        self.root.title("Jogo da Memória")
        self.images = images * 2
        self.shuffle_cards()
        self.create_widgets()
        self.opened_cards = []  # Lista para rastrear as cartas abertas
        self.locked = False  # Flag para impedir a seleção de novas cartas durante o atraso
        self.start_time = time.time()
        self.errors = 0

    def shuffle_cards(self):
        random.shuffle(self.images)

    def create_widgets(self):
        self.buttons = []
        placeholder = Image.open("placeholder.jpg")
        placeholder = placeholder.resize((300, 300), Image.LANCZOS)
        placeholder_photo = ImageTk.PhotoImage(placeholder)

        for i, _ in enumerate(self.images):
            button = tk.Button(
                self.root, image=placeholder_photo, text=" ",
                command=lambda i=i: self.flip_card(i)
            )
            button.image = placeholder_photo
            button.grid(row=i // 4, column=i % 4)
            self.buttons.append(button)

    def flip_card(self, index):
        if not self.locked and index not in self.opened_cards:
            image_path = self.images[index]
            img = Image.open(image_path)
            img = img.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            self.buttons[index].config(image=photo, text="")
            self.buttons[index].image = photo
            self.opened_cards.append(index)

            if len(self.opened_cards) == 2:
                self.locked = True
                self.root.after(350, self.check_match)

    def check_match(self):
        if len(self.opened_cards) == 2:
            index1, index2 = self.opened_cards
            card1, card2 = self.images[index1], self.images[index2]

            if card1 == card2:
                self.opened_cards = []  # Limpa as cartas abertas
            else:
                self.root.after(350, lambda i=index1, j=index2: self.unflip_cards(i, j))
                self.errors += 1

            self.locked = False
            self.check_game_over()

    def unflip_cards(self, index1, index2):
        placeholder = Image.open("placeholder.jpg")
        placeholder = placeholder.resize((300, 300), Image.LANCZOS)
        placeholder_photo = ImageTk.PhotoImage(placeholder)

        self.buttons[index1].config(image=placeholder_photo, text=" ")
        self.buttons[index1].image = placeholder_photo

        self.buttons[index2].config(image=placeholder_photo, text=" ")
        self.buttons[index2].image = placeholder_photo

        self.opened_cards = []  # Limpa as cartas abertas
        self.locked = False

    def check_game_over(self):
        if all(button["text"] != " " for button in self.buttons):
            messagebox.showinfo("Jogo da Memória", "Parabéns, você ganhou!")
            
    def check_game_over(self):
        if all(button["text"] != " " for button in self.buttons):
            end_time = time.time()
            total_time = end_time - self.start_time
            score = 1000 - (total_time + self.errors * 10)  # Exemplo de cálculo de pontuação
            messagebox.showinfo("Fim de jogo", f"Sua pontuação é {round(score,2)}")

root = tk.Tk()
images = [f"imagem{i}.jpg" for i in range(1, 5)]
game = MemoryGame(root, images)
root.mainloop()
