from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

from database import Database


class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cистема учета товаров")
        self.root.geometry("1000x600")
        self.db = Database("store.db")

        self.create_tables()
        self.insert_sample_data()
        self.create_widgets()
        self.load_categories()
        self.load_products()

        self.current_receipt_id = None
        self.receipt_items = []

    def create_tables(self):
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            total_amount REAL NOT NULL
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS receipt_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (receipt_id) REFERENCES receipts(receipt_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """)

    def insert_sample_data(self):
        row = self.db.query_one("SELECT COUNT(*) FROM categories")
        if row and row[0] != 0:
            return

        self.db.executemany(
            "INSERT INTO categories (category_name) VALUES (?)",
            [
                ("Напитки",),
                ("Молочные продукты",),
                ("Хлебобулочные изделия",),
                ("Консервы",),
            ]
        )

        self.db.executemany(
            "INSERT INTO products (product_name, category_id, price, stock_quantity) VALUES (?, ?, ?, ?)",
            [
                ("Вода минеральная", 1, 25.50, 100),
                ("Сок апельсиновый", 1, 89.90, 50),
                ("Молоко 2.5%", 2, 65.00, 80),
                ("Кефир 1%", 2, 72.50, 60),
                ("Хлеб белый", 3, 45.00, 120),
                ("Батон нарезной", 3, 52.00, 90),
                ("Горошек зеленый", 4, 68.00, 40),
                ("Кукуруза консервированная", 4, 75.00, 35),
            ]
        )

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        self.sales_tab = ttk.Frame(self.notebook)
        self.products_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.sales_tab, text="Продажи")
        self.notebook.add(self.products_tab, text="Товары")
        self.notebook.add(self.reports_tab, text="Отчеты")

        self.create_sales_tab()
        self.create_products_tab()
        self.create_reports_tab()

    def create_sales_tab(self):
        products_frame = ttk.LabelFrame(self.sales_tab, text="Товары")
        products_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        self.products_tree = ttk.Treeview(
            products_frame,
            columns=('id', 'name', 'category', 'price', 'quantity'),
            show='headings'
        )
        for col, text in zip(('id','name','category','price','quantity'),
                             ('ID','Название','Категория','Цена','Остаток')):
            self.products_tree.heading(col, text=text)

        self.products_tree.pack(fill=BOTH, expand=True)

        cart_frame = ttk.LabelFrame(self.sales_tab, text="Чек")
        cart_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

        self.cart_tree = ttk.Treeview(
            cart_frame,
            columns=('id','name','price','quantity','total'),
            show='headings'
        )
        for col, text in zip(('id','name','price','quantity','total'),
                             ('ID','Название','Цена','Кол-во','Сумма')):
            self.cart_tree.heading(col, text=text)

        self.cart_tree.pack(fill=BOTH, expand=True)

        btn_frame = ttk.Frame(cart_frame)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Добавить", command=self.add_to_cart).pack(side=LEFT)
        ttk.Button(btn_frame, text="Удалить", command=self.remove_from_cart).pack(side=LEFT)
        ttk.Button(btn_frame, text="Оформить", command=self.process_sale).pack(side=LEFT)

    def create_products_tab(self):
        self.products_management_tree = ttk.Treeview(
            self.products_tab,
            columns=('id','name','category','price','quantity'),
            show='headings'
        )
        for col in ('id','name','category','price','quantity'):
            self.products_management_tree.heading(col, text=col)

        self.products_management_tree.pack(fill=BOTH, expand=True)

    def create_reports_tab(self):
        self.report_tree = ttk.Treeview(
            self.reports_tab,
            columns=('name','quantity','total'),
            show='headings'
        )
        self.report_tree.pack(fill=BOTH, expand=True)

    def load_categories(self):
        data = self.db.query("SELECT category_id, category_name FROM categories")
        self.categories_dict = {name: cid for cid, name in data}

    def load_products(self):
        products = self.db.query("""
        SELECT p.product_id, p.product_name, c.category_name, p.price, p.stock_quantity
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        """)

        for tree in (self.products_tree, self.products_management_tree):
            tree.delete(*tree.get_children())
            for row in products:
                tree.insert('', END, values=row)

    def add_to_cart(self):
        sel = self.products_tree.focus()
        if not sel:
            return
        values = self.products_tree.item(sel)['values']
        self.cart_tree.insert('', END, values=(values[0], values[1], values[3], 1, values[3]))

    def remove_from_cart(self):
        sel = self.cart_tree.focus()
        if sel:
            self.cart_tree.delete(sel)

    def process_sale(self):
        messagebox.showinfo("Продажа", "Упрощенная версия: продажа выполнена")

    def __del__(self):
        self.db.close()