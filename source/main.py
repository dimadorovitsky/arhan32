import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests
from tkinter import messagebox
import threading
import os


def set_dark_theme():
    style = ttk.Style()

    style.theme_use("clam") 
    style.configure("TButton", background="#495057", foreground="white", activebackground="#6c757d", activeforeground="white", padding=10, borderwidth=0)
    style.configure("TEntry", background="#495057", foreground="white", borderwidth=2, fieldbackground="#343a40")
    style.configure("TLabel", background="#282c34", foreground="white", font=("Arial", 12))
    style.configure("TNotebook.Tab", background="#282c34", foreground="white", padding=10, borderwidth=0)
    style.configure("TNotebook", background="#282c34")
    style.map("TNotebook.Tab", background=[("selected", "#343a40"), ("active", "#343a40")], foreground=[("selected", "white"), ("active", "white")])
    style.configure("Treeview", background="#343a40", foreground="white", fieldbackground="#343a40",
                     rowheight=25, 
                     selectbackground="#495057", 
                     selectforeground="white")
    style.configure("Treeview.Heading", background="#343a40", foreground="white", font=("Arial", 12, "bold"))
    style.configure("Treeview.Item", foreground="white")
 
    style.configure("Vertical.TScrollbar", background="#495057", borderwidth=0, arrowcolor="white")
    style.configure("Horizontal.TScrollbar", background="#495057", borderwidth=0, arrowcolor="white")
    style.configure("TFrame", background="#282c34")

root = tk.Tk()
root.title("Arhan32")
root.geometry("800x600")

set_dark_theme()

icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
root.iconbitmap(icon_path)

scan_frame = tk.Frame(root, background="#282c34")
scan_frame.pack(fill="both", expand=True)

title_label = tk.Label(scan_frame, text="Arhan32", font=("Arial", 24, "bold"), fg="white", bg="#282c34")
title_label.pack(pady=10)

url_label = tk.Label(scan_frame, text="Введите URL сайта:", font=("Arial", 12), fg="white", bg="#282c34")
url_entry = ttk.Entry(scan_frame, width=50)

file_info_label = tk.Label(scan_frame, text="Выбранный файл: ", font=("Arial", 12), fg="white", bg="#282c34")

def load_file():
    global dirs, filepath
    filepath = filedialog.askopenfilename(
        initialdir=os.path.dirname(__file__), 
        title="Выберите файл с директориями",
        filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*"))
    )
    if filepath:
        try:
            with open(filepath, "r") as f:
                dirs = [line.strip() for line in f]
            dirs = ["/" + dir for dir in dirs] 
            file_info_label.config(text=f"Выбранный файл: {filepath}\nСписок директорий: {dirs}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка чтения файла: {e}")

def start_scan():
    url = url_entry.get()
    if not url or not dirs:
        messagebox.showerror("Ошибка", "Введите URL сайта и загрузите файл с директориями!")
        return

    if "://" not in url:
        url = "http://" + url

    tree.delete(*tree.get_children())

    scan_thread = threading.Thread(target=bruteforce_dirs, args=(url, dirs))
    scan_thread.start()

def bruteforce_dirs(url, dirs):
    for dir in dirs:
        full_url = url + dir
        try:
            response = requests.get(full_url)
            response.raise_for_status()
            code = response.status_code
            color = "green" if code == 200 else "red"
            tree.insert("", "end", values=(url, dir, code), tags=(color,))
        except requests.exceptions.RequestException as e:
            tree.insert("", "end", values=(url, dir, "Ошибка"), tags=("red",))
            print(f"Ошибка при сканировании: {e}")

tree = ttk.Treeview(scan_frame, columns=("URL", "Директория", "Код"), show="headings", height=15)
tree.heading("URL", text="Ссылка на сайт")
tree.heading("Директория", text="/директория")
tree.heading("Код", text="Код доступа")
tree.column("URL", width=200, stretch=False)
tree.column("Директория", width=200, stretch=False)
tree.column("Код", width=100, stretch=False)

tree.tag_configure("green", foreground="green")
tree.tag_configure("red", foreground="red")

url_label.pack(pady=5)
url_entry.pack(pady=5)
file_info_label.pack(pady=5)
load_button = ttk.Button(scan_frame, text="Загрузить файл", command=load_file)
load_button.pack(pady=5)
scan_button = ttk.Button(scan_frame, text="Сканировать", command=start_scan)
scan_button.pack(pady=10)
tree.pack(pady=10, fill="both", expand=True)

root.mainloop()