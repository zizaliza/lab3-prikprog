import tkinter as tk
from tkinter import messagebox
import random
import time

from core.models import Record

class MainWindow:
    def __init__(self, root, record_service):
        self.root = root
        self.record_service = record_service
        self.start_time = None
        self.current_letter = None
        self.letters = [ 'a' ]
        self.correct_letters = 0
        self.total_letters = 0
        self.username = ""
        self.is_training = False
        self.number_letters_displayed = 5

        random.seed(time.time())

        root.title("Вариант 16. клавиатурный тренажер")

        # Главная страница
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.name_label = tk.Label(self.main_frame, text="Введите имя:", font=("Arial", 14))
        self.name_label.pack()

        self.name_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(self.main_frame, text="Начать тренировку", command=self.start_training)
        self.start_button.pack(pady=5)

        self.records_table = tk.Label(self.main_frame, text="Рекорды:", font=("Arial", 14))
        self.records_table.pack(pady=5)

        self.update_records_display()

    def start_training(self):
        self.username = self.name_entry.get()
        self.is_training = True

        if not self.username:
            messagebox.showwarning("Ошибка", "Введите имя!")
            return

        self.main_frame.pack_forget()
        self.training_frame = tk.Frame(self.root)
        self.training_frame.pack(padx=10, pady=10)

        self.description_label = tk.Label(self.training_frame, text="Введите показанную букву", font=("Arial", 18))
        self.description_label.pack()

        self.current_letter_label = tk.Label(self.training_frame, text="", font=("Arial", 48))
        self.current_letter_label.pack()

        self.cancel_button = tk.Button(self.training_frame, text="Отменить тренировку", font=("Arial", 18), command=self.cancel_training)
        self.cancel_button.pack(pady=5)

        self.timer_label = tk.Label(self.training_frame, text="60 секунд", font=("Arial", 18))
        self.timer_label.pack(pady=5)

        self.input_entry = tk.Entry(self.training_frame, font=("Arial", 24))
        self.input_entry.focus()
        self.input_entry.pack(pady=5)
        self.input_entry.bind("<KeyRelease>", self.check_input)

        self.start_time = time.time()
        self.correct_letters = 0
        self.total_letters = 0
        self.next_letter()
        self.update_timer()

    def next_letter(self):
        self.generate_letters()
        self.current_letter_label.config(text=self.letters[self.total_letters:self.total_letters + self.number_letters_displayed])
        self.input_entry.delete(0, tk.END)
    
    def generate_letters(self):
        while self.total_letters + self.number_letters_displayed >= len(self.letters):
            letter = random.choice("abcdefghijklmnopqrstuvwxyz")
            self.letters.append(letter)

    def check_input(self, event):
        if self.input_entry.get() == self.letters[self.total_letters]:
            self.correct_letters += 1
        self.total_letters += 1
        self.next_letter()

    def update_timer(self):
        remaining_time = 60 - int(time.time() - self.start_time)
        self.timer_label.config(text=f"{remaining_time} секунд")

        if remaining_time > 0 and self.is_training:
            self.root.after(1000, self.update_timer)
        elif self.is_training:
            self.show_results()

    def cancel_training(self):
        self.is_training = False
        self.training_frame.pack_forget()
        self.main_frame.pack()
        self.update_records_display()

    def show_results(self):
        accuracy = round(((self.correct_letters / self.total_letters) * 100), 2) if self.total_letters > 0 else 0
        result_text = f"Результат: {self.correct_letters} правильных букв из {self.total_letters} ({accuracy:.2f}% точность)"
        self.current_letter_label.config(text=result_text)
        self.record_service.add_record(Record(self.username, self.correct_letters, accuracy))
        self.training_frame.pack_forget()
        self.main_frame.pack()
        self.update_records_display()

    def update_records_display(self):
        records = self.record_service.get_top_records()
        records_text = "\n".join([f"{r.name} - {r.score} букв, {r.accuracy}% точность" for r in records])
        self.records_table.config(text="Рекорды:\n" + (records_text if records_text else "Нет рекордов"))
