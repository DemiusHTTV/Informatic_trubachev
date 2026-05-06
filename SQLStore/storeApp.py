from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

from database import Database


class StoreApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Система учета товаров")
        self.root.geometry("1000x600")

        self.db = Database("store.db")

        self.create_tables()
        self.insert_sample_data()
        self.create_widgets()
        self.load_categories()
        self.load_products()



    def create_tables(self):
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            category_id INTEGER,
            price REAL,
            stock_quantity INTEGER
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT,
            total_amount REAL
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS receipt_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price_per_unit REAL,
            total_price REAL
        )
        """)

    def insert_sample_data(self):
        if self.db.query_one("SELECT COUNT(*) FROM categories")[0] != 0:
            return

        self.db.executemany(
            "INSERT INTO categories (category_name) VALUES (?)",
            [("Напитки",), ("Еда",)]
        )

        self.db.executemany(
            "INSERT INTO products (product_name, category_id, price, stock_quantity) VALUES (?, ?, ?, ?)",
            [
                ("Вода", 1, 25, 100),
                ("Сок", 1, 80, 50),
                ("Хлеб", 2, 40, 70),
            ]
        )

   

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=BOTH, expand=True)

        self.sales_tab = Frame(notebook)
        self.products_tab = Frame(notebook)
        self.reports_tab = Frame(notebook)

        notebook.add(self.sales_tab, text="Продажи")
        notebook.add(self.products_tab, text="Товары")
        notebook.add(self.reports_tab, text="Отчеты")

        self.create_sales_tab()
        self.create_products_tab()
        self.create_reports_tab()



    def create_sales_tab(self):

        left = Frame(self.sales_tab, width=800)
        left.pack(side=LEFT, fill=BOTH, expand=False)
        left.pack_propagate(False)

        self.products_tree = ttk.Treeview(
            left,
            columns=("id", "name", "cat", "price", "qty"),
            show="headings"
        )

        headers = ["ID", "Название", "Категория", "Цена", "Остаток"]

        for i, col in enumerate(("id", "name", "cat", "price", "qty")):
            self.products_tree.heading(col, text=headers[i])
            self.products_tree.column(col, width=110)

        self.products_tree.pack(fill=BOTH, expand=True)


        right = Frame(self.sales_tab, width=380, bg="#2b2b2b")
        right.pack(side=RIGHT, fill=Y, expand=False)
        right.pack_propagate(False)

        self.cart_tree = ttk.Treeview(
            right,
            columns=("id", "name", "price", "qty", "sum"),
            show="headings",
            height=15
        )

        headers2 = ["ID", "Товар", "Цена", "Кол-во", "Сумма"]

        for i, col in enumerate(("id", "name", "price", "qty", "sum")):
            self.cart_tree.heading(col, text=headers2[i])
            self.cart_tree.column(col, width=100)

        self.cart_tree.pack(fill=BOTH, padx=5, pady=5)

        btns = Frame(right, bg="#2b2b2b")
        btns.pack(fill=X, pady=10)

        Button(btns, text="Добавить", command=self.add_to_cart, width=12, height=2).pack(side=LEFT, padx=5)
        Button(btns, text="Удалить", command=self.remove_from_cart, width=12, height=2).pack(side=LEFT, padx=5)
        Button(btns, text="ОК", command=self.process_sale, width=25, height=2).pack(side=LEFT, padx=5)

        
    def create_products_tab(self):

        top = Frame(self.products_tab)
        top.pack()

        self.name_entry = Entry(top)
        self.name_entry.pack(side=LEFT)
        self.name_entry.insert(0, "Название")

        self.price_entry = Entry(top)
        self.price_entry.pack(side=LEFT)
        self.price_entry.insert(0, "Цена")

        self.qty_entry = Entry(top)
        self.qty_entry.pack(side=LEFT)
        self.qty_entry.insert(0, "Кол-во")

        Button(top, text="Добавить товар", command=self.add_product).pack(side=LEFT)

        self.products_management_tree = ttk.Treeview(
            self.products_tab,
            columns=("id", "name", "cat", "price", "qty"),
            show="headings"
        )

        for col in ("id", "name", "cat", "price", "qty"):
            self.products_management_tree.heading(col, text=col)

        self.products_management_tree.pack(fill=BOTH, expand=True)



    def create_reports_tab(self):

        top = Frame(self.reports_tab)
        top.pack()

        self.date_entry = Entry(top)
        self.date_entry.pack(side=LEFT)

        Button(top, text="Показать",
               command=lambda: self.load_report(self.date_entry.get())
               ).pack(side=LEFT)

        self.report_tree = ttk.Treeview(
            self.reports_tab,
            columns=("name", "qty", "sum"),
            show="headings"
        )

        for col in ("name", "qty", "sum"):
            self.report_tree.heading(col, text=col)

        self.report_tree.pack(fill=BOTH, expand=True)


    def load_categories(self):
        data = self.db.query("SELECT * FROM categories")
        self.categories = {name: cid for cid, name in data}

    def load_products(self):
        data = self.db.query("""
        SELECT p.product_id, p.product_name, c.category_name, p.price, p.stock_quantity
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        """)

        for tree in (self.products_tree, self.products_management_tree):
            tree.delete(*tree.get_children())
            for row in data:
                tree.insert("", END, values=row)

    def add_to_cart(self):
        sel = self.products_tree.focus()
        if not sel:
            return

        v = self.products_tree.item(sel)["values"]

        if v[4] <= 0:
            messagebox.showerror("Ошибка", "Нет на складе")
            return

        self.cart_tree.insert("", END, values=(v[0], v[1], v[3], 1, v[3]))

    def remove_from_cart(self):
        sel = self.cart_tree.focus()
        if sel:
            self.cart_tree.delete(sel)

    def process_sale(self):
        items = self.cart_tree.get_children()
        if not items:
            return

        total = 0
        sale = []

        for i in items:
            v = self.cart_tree.item(i)["values"]
            total += float(v[4])
            sale.append(v)

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.db.execute(
            "INSERT INTO receipts (sale_date, total_amount) VALUES (?, ?)",
            (date, total)
        )

        rid = self.db.query_one("SELECT last_insert_rowid()")[0]

        for v in sale:
            self.db.execute("""
            INSERT INTO receipt_items
            (receipt_id, product_id, quantity, price_per_unit, total_price)
            VALUES (?, ?, ?, ?, ?)
            """, (rid, v[0], v[3], v[2], v[4]))

            self.db.execute("""
            UPDATE products
            SET stock_quantity = stock_quantity - ?
            WHERE product_id = ?
            """, (v[3], v[0]))

        messagebox.showinfo("OK", f"Чек {rid}")

        self.cart_tree.delete(*self.cart_tree.get_children())
        self.load_products()

    def load_report(self, date):
        data = self.db.query("""
        SELECT p.product_name, SUM(ri.quantity), SUM(ri.total_price)
        FROM receipt_items ri
        JOIN receipts r ON ri.receipt_id = r.receipt_id
        JOIN products p ON ri.product_id = p.product_id
        WHERE DATE(r.sale_date) = ?
        GROUP BY p.product_name
        """, (date,))

        self.report_tree.delete(*self.report_tree.get_children())

        for row in data:
            self.report_tree.insert("", END, values=row)

    def add_product(self):
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        qty = int(self.qty_entry.get())

        self.db.execute("""
        INSERT INTO products (product_name, category_id, price, stock_quantity)
        VALUES (?, ?, ?, ?)
        """, (name, 1, price, qty))

        self.load_products()
        messagebox.showinfo("OK", "Добавлено")

    def __del__(self):
        self.db.close()