import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

# Чтение данных из CSV файла
relative_path = "output.csv"
absolute_path = os.path.abspath(relative_path)
data = pd.read_csv(absolute_path)

# Функция для добавления переноса строки после 100 символов
def add_line_breaks(text, length):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > length:
            lines.append(current_line.strip())
            current_line = word
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    lines.append(current_line.strip())
    return "\n".join(lines)

# Функция для фильтрации данных и обновления Treeview
def Poz_otz():
    filtered_data = data[data.iloc[:, 2] > 3]
    update_treeview(filtered_data)

# Функция для фильтрации данных и обновления Treeview
def Neg_otz():
    filtered_data = data[data.iloc[:, 2] <= 3]
    update_treeview(filtered_data)

# Функция для показа всех отзывов
def show_all_reviews():
    update_treeview(data)

# Функция для обновления Treeview
def update_treeview(filtered_data):
    for item in tree.get_children():
        tree.delete(item)
    for index, row in filtered_data.iterrows():
        broken_text1 = add_line_breaks(str(row.iloc[1]), 175)
        broken_text2 = add_line_breaks(str(row.iloc[2]), 175)
        tree.insert("", "end", values=(broken_text1, broken_text2))

# Функция для выхода из приложения
def exit_app():
    root.destroy()

# Функция для проверки авторизации
def check_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "123":
        login_window.destroy()
        create_main_window()
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

# Создание окна авторизации
def create_login_window():
    global login_window, username_entry, password_entry
    login_window = tk.Tk()
    login_window.title("Авторизация")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Имя пользователя:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Пароль:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Войти", command=check_login)
    login_button.pack(pady=10)

    login_window.mainloop()

# Создание основного окна Tkinter
def create_main_window():
    global root, tree
    root = tk.Tk()
    root.title("Система мониторинга публичного рейтинга учебного заведения")
    root.geometry("1550x600")  # Ширина 800 пикселей, высота 600 пикселей

    # Создание верхнего Frame для кнопок
    button_frame = tk.Frame(root, relief='ridge', borderwidth=2)
    button_frame.pack(side='top', fill='x')

    # Создание кнопки для фильтрации данных
    filter_button = tk.Button(button_frame, text="Вывести отрицательные отзывы", command=Neg_otz)
    filter_button.pack(side='left', padx=10, pady=10)

    # Создание кнопки для фильтрации данных
    filter_button2 = tk.Button(button_frame, text="Вывести положительные отзывы", command=Poz_otz)
    filter_button2.pack(side='left', padx=10, pady=10)

    # Создание кнопки для показа всех отзывов
    show_all_button = tk.Button(button_frame, text="Показать все отзывы", command=show_all_reviews)
    show_all_button.pack(side='left', padx=10, pady=10)

    # Создание кнопки для выхода из приложения
    exit_button = tk.Button(button_frame, text="Выход", command=exit_app)
    exit_button.pack(side='right', padx=10, pady=10)

    # Создание нижнего Frame для Treeview
    tree_frame = tk.Frame(root, relief='ridge', borderwidth=2)
    tree_frame.pack(side='bottom', expand=True, fill='both')

    # Создание стиля для Treeview
    style = ttk.Style()
    style.configure("Treeview",
                    rowheight=150,  # Увеличиваем высоту строк для лучшей компоновки текста
                    font=('Arial', 12),  # Устанавливаем шрифт для текста в ячейках
                    borderwidth=1,  # Добавляем границу вокруг ячеек
                    relief="raised")  # Устанавливаем тип границы

    # Создание Treeview виджета
    tree = ttk.Treeview(tree_frame, show='headings')

    # Определение столбцов
    tree["columns"] = ("Column1", "Column2")
    tree.column("Column1", width=350, anchor='w')  # Центрируем текст в ячейках
    tree.column("Column2", width=70, anchor='w', stretch=False)  # Центрируем текст в ячейках
    tree.heading("Column1", text="Комментарий")
    tree.heading("Column2", text="Оценка")

    # Заполнение Treeview данными
    for index, row in data.iterrows():
        broken_text1 = add_line_breaks(str(row.iloc[1]), 175)
        broken_text2 = add_line_breaks(str(row.iloc[2]), 175)
        tree.insert("", "end", values=(broken_text1, broken_text2))

    # Размещение Treeview в Frame
    tree.pack(expand=True, fill='both')

    # Запуск основного цикла Tkinter
    root.mainloop()

# Запуск окна авторизации
create_login_window()