import tkinter as tk
from tkinter import scrolledtext, messagebox
import re
import requests

class GematriaApp:
    def __init__(self, master):
        self.master = master
        master.title("English Qaballa Gematria Quote Finder")

        # URL Entry
        tk.Label(master, text="Enter URL of .txt file:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        # Target Sum Entry
        tk.Label(master, text="Enter target sum:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sum_entry = tk.Entry(master, width=10)
        self.sum_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Search Button
        self.search_button = tk.Button(master, text="Search Quotes", command=self.search_quotes)
        self.search_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Results Text Area
        self.results_area = scrolledtext.ScrolledText(master, width=70, height=20)
        self.results_area.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def create_eq_dict(self):
        return {chr(97 + i): 10 + i for i in range(26)}

    def eq_value(self, char):
        return self.eq_dict.get(char.lower(), 0)

    def eq_sum(self, text):
        return sum(self.eq_value(c) for c in text)

    def find_sentence_start_quotes(self, text, target_sum, max_length=50):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        quotes = []
        
        for sentence in sentences:
            words = sentence.split()
            current_sum = 0
            for i in range(min(len(words), max_length)):
                current_sum += self.eq_sum(words[i])
                if current_sum == target_sum:
                    quote = ' '.join(words[:i+1])
                    quotes.append(quote)
                elif current_sum > target_sum:
                    break
        
        return quotes

    def search_quotes(self):
        url = self.url_entry.get()
        try:
            target_sum = int(self.sum_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the target sum.")
            return

        try:
            response = requests.get(url, timeout=10)
            text = response.text
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch the text from the URL.")
            return

        self.eq_dict = self.create_eq_dict()
        matching_quotes = self.find_sentence_start_quotes(text, target_sum)

        self.results_area.delete(1.0, tk.END)
        self.results_area.insert(tk.END, f"Found {len(matching_quotes)} matching quotes:\n\n")
        for i, quote in enumerate(matching_quotes, 1):
            self.results_area.insert(tk.END, f"{i}. '{quote}' (Sum: {self.eq_sum(quote)})\n\n")

root = tk.Tk()
app = GematriaApp(root)
root.mainloop()