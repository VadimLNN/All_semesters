import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# --- Настройки интерфейса ---
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
BUTTON_COLOR = "#007acc"
HIGHLIGHT_COLOR = "#569cd6"
FONT = ("Segoe UI", 14)
HEADER_FONT = ("Segoe UI", 18, "bold")

# --- Подключение к БД ---
DB_PATH = "DreamHackers.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Основное окно ---
root = tk.Tk()
root.title("DreamHackers Database")
root.geometry("1600x900")
root.configure(bg=BG_COLOR)

# --- Стили ---
style = ttk.Style()
style.theme_use("default")

# Увеличиваем текст в названиях вкладок
style.configure(
    "TNotebook.Tab",
    background=BG_COLOR,
    foreground=FG_COLOR,
    padding=(10, 5),
    font=("Segoe UI", 14, "bold")  # Увеличенный шрифт
)
style.map("TNotebook.Tab", background=[("selected", BUTTON_COLOR)])

# Увеличиваем текст в таблицах (Treeview)
style.configure(
    "Treeview",
    background=BG_COLOR,
    foreground=FG_COLOR,
    fieldbackground=BG_COLOR,
    rowheight=30,  # Увеличенная высота строки
    font=("Segoe UI", 12)  # Увеличенный шрифт
)
style.map("Treeview", background=[("selected", HIGHLIGHT_COLOR)])

# Увеличиваем текст в заголовках таблиц
style.configure(
    "Treeview.Heading",
    background=BUTTON_COLOR,
    foreground=FG_COLOR,
    font=("Segoe UI", 14, "bold")  # Увеличенный шрифт заголовков
)
style.configure("TNotebook", background=BG_COLOR)
style.configure("TNotebook.Tab", background=BG_COLOR, foreground=FG_COLOR, padding=(10, 5))
style.map("TNotebook.Tab", background=[("selected", BUTTON_COLOR)])

style.configure("TFrame", background=BG_COLOR)
style.configure("TButton", background=BUTTON_COLOR, foreground=FG_COLOR, borderwidth=0, padding=(5, 2))
style.map("TButton", background=[("active", HIGHLIGHT_COLOR)])

style.configure("Treeview", background=BG_COLOR, foreground=FG_COLOR, fieldbackground=BG_COLOR, rowheight=25)
style.map("Treeview", background=[("selected", HIGHLIGHT_COLOR)])
style.configure("Treeview.Heading", background=BUTTON_COLOR, foreground=FG_COLOR)

# --- Заголовок ---
title_label = tk.Label(root, text="DreamHackers Database Management", font=HEADER_FONT, bg=BG_COLOR, fg=FG_COLOR)
title_label.pack(anchor="w", padx=10, pady=10)

# --- Панель вкладок ---
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both", padx=10, pady=10)

# --- Универсальная функция обработки данных ---
def execute_query(query, params=(), fetch=False):
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall() if fetch else None
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# --- Универсальная функция создания вкладки ---
def create_tab(tab_name, columns, table_name, custom_query=None, insert_query=None, update_query=None):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=tab_name)

    # --- Заголовок ---
    tab_header = tk.Label(tab, text=f"{tab_name} Management", font=HEADER_FONT, bg=BG_COLOR, fg=FG_COLOR)
    tab_header.pack(anchor="w", padx=10, pady=10)

    # --- Форма ввода ---
    form_frame = tk.LabelFrame(tab, text="Manage Records", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    form_frame.pack(side="left", padx=10, pady=10, fill="y")

    entries = {}
    for idx, col in enumerate(columns[1:], start=1):  # Пропускаем первое поле (ID)
        lbl = tk.Label(form_frame, text=f"{col}:", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        lbl.grid(row=idx - 1, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(form_frame, bg="#2e2e2e", fg=FG_COLOR, font=FONT)
        entry.grid(row=idx - 1, column=1, padx=5, pady=5, sticky="w")
        entries[col] = entry

    # --- Таблица ---
    table_frame = tk.LabelFrame(tab, text="Records", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    table_frame.pack(side="left", expand=1, fill="both", padx=10, pady=10)

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
    tree.pack(expand=1, fill="both", padx=5, pady=5)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    # --- Функции ---
    def refresh():
        query = custom_query if custom_query else f"SELECT * FROM {table_name};"
        rows = execute_query(query, fetch=True)
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)

    def insert():
        values = [entries[col].get() for col in columns[1:]]
        if any(v.strip() == "" for v in values):
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        try:
            query = insert_query if insert_query else f"INSERT INTO {table_name} ({', '.join(columns[1:])}) VALUES ({', '.join('?' for _ in values)});"
            execute_query(query, values)
            refresh()
            messagebox.showinfo("Success", "Record has been added.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "No record selected.")
            return
        values = tree.item(selected, "values")
        updated_values = [entries[col].get() for col in columns[1:]] + [values[0]]
        try:
            query = update_query if update_query else f"UPDATE {table_name} SET {', '.join(f'{col} = ?' for col in columns[1:])} WHERE {columns[0]} = ?;"
            execute_query(query, updated_values)
            refresh()
            messagebox.showinfo("Success", "Record has been updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "No record selected.")
            return
        values = tree.item(selected, "values")
        try:
            execute_query(f"DELETE FROM {table_name} WHERE {columns[0]} = ?;", (values[0],))
            refresh()
            messagebox.showinfo("Success", "Record has been deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields():
        for entry in entries.values():
            entry.delete(0, tk.END)

    # --- Кнопки ---
    btn_frame = tk.Frame(form_frame, bg=BG_COLOR)
    btn_frame.grid(row=len(columns), columnspan=2, pady=10)
    ttk.Button(btn_frame, text="Add", command=insert).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Update", command=update).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Delete", command=delete).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Clear", command=clear_fields).pack(side="left", padx=5)

    # --- Событие выбора записи ---
    def on_select(event):
        selected = tree.focus()
        values = tree.item(selected, "values")
        for col, value in zip(columns[1:], values[1:]):
            entries[col].delete(0, tk.END)
            entries[col].insert(0, value)

    tree.bind("<<TreeviewSelect>>", on_select)

    refresh()

# --- Универсальная функция создания вкладки ---
def create_tab_cmb(tab_name, columns, table_name, custom_query=None, insert_query=None, update_query=None, combo_fields=None, bd_combo_fields=None):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=tab_name)

    # --- Заголовок ---
    tab_header = tk.Label(tab, text=f"{tab_name} Management", font=HEADER_FONT, bg=BG_COLOR, fg=FG_COLOR)
    tab_header.pack(anchor="w", padx=10, pady=10)

    # --- Форма ввода ---
    form_frame = tk.LabelFrame(tab, text="Manage Records", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    form_frame.pack(side="left", padx=10, pady=10, fill="y")

    entries = {}
    combos = {}
    for idx, col in enumerate(columns[1:], start=1):  # Пропускаем первое поле (ID)
        if combo_fields and col in combo_fields:
            lbl = tk.Label(form_frame, text=f"{col}:", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
            lbl.grid(row=idx - 1, column=0, padx=5, pady=5, sticky="w")
            combo = ttk.Combobox(form_frame, state="readonly", background=BG_COLOR, font=FONT, name=col)
            combo.grid(row=idx-1, column=1, sticky="ew", padx=5, pady=5)
            combos[col] = combo
            entries[col] = combo
        else:
            lbl = tk.Label(form_frame, text=f"{col}:", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
            lbl.grid(row=idx - 1, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(form_frame, bg="#2e2e2e", fg=FG_COLOR, font=FONT)
            entry.grid(row=idx - 1, column=1, padx=5, pady=5, sticky="w")
            entries[col] = entry

    # Заполнение комбобоксов
    def populate_comboboxes():
        try:
            for i in range(len(combo_fields)):
                query_result = execute_query("SELECT {} FROM {};".format(combo_fields[i], bd_combo_fields[i]), fetch=True)
                if combo_fields[i] in combos:
                    combos[combo_fields[i]]["values"] = [row[0] for row in query_result]
                print(f"Refreshing comboboxes for tab '{tab_name}'")  # 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data for comboboxes: {str(e)}")

    # --- Таблица ---
    table_frame = tk.LabelFrame(tab, text="Records", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    table_frame.pack(side="left", expand=1, fill="both", padx=10, pady=10)

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
    tree.pack(expand=1, fill="both", padx=5, pady=5)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    # Функции управления
    def refresh():
        try:
            rows = execute_query(custom_query, fetch=True)
            tree.delete(*tree.get_children())
            for row in rows:
                tree.insert("", "end", values=row)

            if combo_fields:
                populate_comboboxes()
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить записи: {str(e)}")

    def insert():
        values = [entries[col].get() for col in columns[1:]]
        if not all(values):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            execute_query(insert_query, values)
            refresh()
            messagebox.showinfo("Успех", "Запись добавлена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить запись: {str(e)}")

    def update():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Ошибка", "Не выбрана запись для обновления.")
            return
        values = [entries[col].get() for col in columns[1:]]
        record_id = tree.item(selected, "values")[0]

        if not all(values):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            execute_query(update_query, values + [record_id])
            refresh()
            messagebox.showinfo("Успех", "Запись обновлена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить запись: {str(e)}")

    def delete():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Ошибка", "Не выбрана запись для удаления.")
            return
        record_id = tree.item(selected, "values")[0]
        try:
            execute_query(f"DELETE FROM {table_name} WHERE {columns[0]} = ?;", (record_id,))
            refresh()
            messagebox.showinfo("Успех", "Запись удалена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить запись: {str(e)}")

    def clear_fields():
        for col in columns[1:]:
            if col in combos:
                combos[col].set("")
            else:
                entries[col].delete(0, tk.END)

    # Событие выбора записи
    def on_select(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        for idx, col in enumerate(columns[1:], start=1):
            if col in combos:
                combos[col].set(values[idx])
            else:
                entries[col].delete(0, tk.END)
                entries[col].insert(0, values[idx])

    # --- Кнопки ---
    btn_frame = tk.Frame(form_frame, bg=BG_COLOR)
    btn_frame.grid(row=len(columns), columnspan=2, pady=10)
    ttk.Button(btn_frame, text="Add", command=insert).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Update", command=update).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Delete", command=delete).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Clear", command=clear_fields).pack(side="left", padx=5)
    ttk.Button(btn_frame, command=populate_comboboxes, name="refresh")

    tree.bind("<<TreeviewSelect>>", on_select)
    
    refresh()



# --- Создание вкладок ---
create_tab("Users", ["user_id", "username", "email", "registration_date"], "Users")
create_tab_cmb(
    "Games",
    ["game_id", "title", "genre_name", "price", "release_date"],
    "Games",
    custom_query="""SELECT g.game_id, g.title, gn.genre_name, g.price, g.release_date FROM Games g JOIN Genres gn ON g.genre_id = gn.genre_id;""",
    insert_query="""INSERT INTO Games (title, genre_id, price, release_date) VALUES (?, (SELECT genre_id FROM Genres WHERE genre_name = ?), ?, ?);""",
    update_query="""UPDATE Games SET title = ?, genre_id = (SELECT genre_id FROM Genres WHERE genre_name = ?), price = ?, release_date = ? WHERE game_id = ?;""",
    combo_fields=["genre_name"],
    bd_combo_fields=["Genres"]
)
create_tab_cmb(
    "Orders",
    ["order_id", "username", "order_date"],
    "Orders",
    custom_query="""SELECT o.order_id, u.username, o.order_date FROM Orders o JOIN Users u ON o.user_id = u.user_id;""",
    insert_query="""INSERT INTO Orders (user_id, order_date) VALUES ((SELECT user_id FROM Users WHERE username = ?), ?);""",
    update_query="""UPDATE Orders SET user_id = (SELECT user_id FROM Users WHERE username = ?), order_date = ? WHERE order_id = ?;""",
    combo_fields = ["username"],
    bd_combo_fields = ["Users"]
)
create_tab("Genres", ["genre_id", "genre_name"], "Genres")
create_tab_cmb(
    "OrderList",
    ["orderlist_id", "order_id", "title", "quantity"],
    "OrderList",
    custom_query="""SELECT ol.orderlist_id, ol.order_id, g.title AS game_name, ol.quantity FROM OrderList ol JOIN Games g ON ol.game_id = g.game_id;""",
    insert_query="""INSERT INTO OrderList (order_id, game_id, quantity) VALUES (?, (SELECT game_id FROM Games WHERE title = ?), ?);""",
    update_query="""UPDATE OrderList SET order_id = ?, game_id = (SELECT game_id FROM Games WHERE title = ?), quantity = ? WHERE orderlist_id = ?;""",
    combo_fields = ["order_id", "title"],
    bd_combo_fields = ["OrderList" ,"Games"]
)


def create_reports_tab():
    reports_tab = ttk.Frame(notebook)
    notebook.add(reports_tab, text="Reports")

    # --- Фрейм для левой части: секция кнопок ---
    left_frame = tk.LabelFrame(reports_tab, text="Generate Reports", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    left_frame.pack(side="left", padx=10, pady=10, fill="y")

    # Получение списка уникальных дат заказов
    def get_available_dates():
        try:
            query = "SELECT DISTINCT order_date FROM Orders ORDER BY order_date;"
            dates = execute_query(query, fetch=True)
            return [row[0] for row in dates]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch order dates: {e}")
            return []

    # Обновление комбобоксов
    def populate_comboboxes():
        available_dates = get_available_dates()
        start_date_combo["values"] = available_dates
        end_date_combo["values"] = available_dates
        point_date_combo["values"] = available_dates

    tk.Label(left_frame, text="Start Date:", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    start_date_combo = ttk.Combobox(left_frame, font=FONT, state="readonly")
    start_date_combo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(left_frame, text="End Date:", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    end_date_combo = ttk.Combobox(left_frame, font=FONT, state="readonly")
    end_date_combo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(left_frame, text="Generate Range Report", command=lambda: generate_range_report(start_date_combo, end_date_combo)).grid(row=2, column=0, columnspan=2, pady=10)

    tk.Label(left_frame, text="Control Point:", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=3, column=0, padx=5, pady=5, sticky="w")
    point_date_combo = ttk.Combobox(left_frame, font=FONT, state="readonly")
    point_date_combo.grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(left_frame, text="Generate Point Report", command=lambda: generate_point_report(point_date_combo)).grid(row=4, column=0, columnspan=2, pady=10)

    # --- Фрейм для правой части: таблица отчётов ---
    right_frame = tk.LabelFrame(reports_tab, text="Report Details", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    right_frame.pack(side="left", padx=10, pady=10, expand=True, fill="both")

    report_tree = ttk.Treeview(right_frame, show="headings", style="Treeview")
    report_tree.pack(expand=1, fill="both", padx=5, pady=5)

    # --- Вывод данных в таблицу ---
    def update_report(columns, query, params=()):
        report_tree.delete(*report_tree.get_children())
        report_tree["columns"] = columns
        for col in columns:
            report_tree.heading(col, text=col)
            report_tree.column(col, anchor="center", width=150)
        rows = execute_query(query, params, fetch=True)
        for row in rows:
            report_tree.insert("", "end", values=row)

    # --- Отчёты ---
    def generate_range_report(start_date_combo, end_date_combo):
        start_date = start_date_combo.get()
        end_date = end_date_combo.get()
        query = """
            SELECT o.order_id, u.username, SUM(ol.quantity), SUM(ol.quantity * g.price) AS total_price, o.order_date
            FROM Orders o
            JOIN OrderList ol ON o.order_id = ol.order_id
            JOIN Games g ON ol.game_id = g.game_id
            JOIN Users u ON o.user_id = u.user_id
            WHERE o.order_date BETWEEN ? AND ?
            GROUP BY o.order_id;
        """
        update_report(["Order ID", "Username", "Quantity", "Total Price", "Order Date"], query, (start_date, end_date))

    def generate_point_report(point_date_combo):
        point_date = point_date_combo.get()
        query = """
            SELECT o.order_id, u.username, SUM(ol.quantity), SUM(ol.quantity * g.price) AS total_price, o.order_date
            FROM Orders o
            JOIN OrderList ol ON o.order_id = ol.order_id
            JOIN Games g ON ol.game_id = g.game_id
            JOIN Users u ON o.user_id = u.user_id
            WHERE o.order_date = ?
            GROUP BY o.order_id;
        """
        update_report(["Order ID", "Username", "Quantity", "Total Price", "Order Date"], query, (point_date,))

    def top_selling_games():
        query = """
            SELECT g.title, SUM(ol.quantity) AS total_sold
            FROM OrderList ol
            JOIN Games g ON ol.game_id = g.game_id
            GROUP BY g.game_id
            ORDER BY total_sold DESC
            LIMIT 7;
        """
        update_report(["Game Title", "Total Sold"], query)

    def top_expensive_orders():
        query = """
            SELECT o.order_id, SUM(ol.quantity * g.price) AS total_price
            FROM Orders o
            JOIN OrderList ol ON o.order_id = ol.order_id
            JOIN Games g ON ol.game_id = g.game_id
            GROUP BY o.order_id
            ORDER BY total_price DESC
            LIMIT 8;
        """
        update_report(["Order ID", "Total Price"], query)

    def top_profit_games():
        query = """
            SELECT g.title, SUM(ol.quantity * g.price) AS total_revenue
            FROM OrderList ol
            JOIN Games g ON ol.game_id = g.game_id
            GROUP BY g.game_id
            ORDER BY total_revenue DESC
            LIMIT 5;
        """
        update_report(["Game Title", "Total Revenue"], query)

    def top_profit_users():
        query = """
            WITH MaxOrderPrice AS (
                SELECT SUM(ol.quantity * g.price) AS total_order_price
                FROM Orders o
                JOIN OrderList ol ON o.order_id = ol.order_id
                JOIN Games g ON ol.game_id = g.game_id
                GROUP BY o.order_id
                ORDER BY total_order_price DESC
                LIMIT 1
            )
            SELECT u.username, o.order_id, SUM(ol.quantity * g.price) AS total_order_price
            FROM Orders o
            JOIN Users u ON o.user_id = u.user_id
            JOIN OrderList ol ON o.order_id = ol.order_id
            JOIN Games g ON ol.game_id = g.game_id
            GROUP BY o.order_id, u.username
            HAVING SUM(ol.quantity * g.price) = (SELECT total_order_price FROM MaxOrderPrice);
        """
        update_report(["username", "order_id", "total_order_price"], query)

    # Кнопки для отчётов
    tk.Label(left_frame, text="Top 7 Selling Games", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=5, column=0, columnspan=2, pady=10)
    ttk.Button(left_frame, text="Show", command=top_selling_games).grid(row=6, column=0, columnspan=2, pady=10)
    
    tk.Label(left_frame, text="Top 8 Expensive Orders", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(left_frame, text="Show", command=top_expensive_orders).grid(row=8, column=0, columnspan=2, pady=10)
    
    tk.Label(left_frame, text="Top 5 Profit Games", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=9, column=0, columnspan=2, pady=10)
    ttk.Button(left_frame, text="Show", command=top_profit_games).grid(row=10, column=0, columnspan=2, pady=10)
    
    tk.Label(left_frame, text="Top Profit Users", bg=BG_COLOR, fg=FG_COLOR, font=FONT).grid(row=11, column=0, columnspan=2, pady=10)
    ttk.Button(left_frame, text="Show", command=top_profit_users).grid(row=12, column=0, columnspan=2, pady=10)
    
    ttk.Button(left_frame, command=populate_comboboxes, name="refresh")

create_reports_tab()

def refresh_comboboxes_in_tab():
    selected_tab = notebook.nametowidget(notebook.select())
    
    # Обходим все виджеты в текущей вкладке
    def find(widget):
        if isinstance(widget, ttk.Button):
            #print(widget._name)
            if widget._name == "refresh":
                #print(notebook.tab(notebook.select(), "text"))
                widget.invoke()
        elif widget.winfo_children():
            # Рекурсивно обходим дочерние виджеты
            for child in widget.winfo_children():
                find(child)

    # Запускаем обновление для текущей вкладки
    find(selected_tab)

notebook.bind("<<NotebookTabChanged>>", lambda event: refresh_comboboxes_in_tab())

# --- Запуск приложения ---
root.mainloop()