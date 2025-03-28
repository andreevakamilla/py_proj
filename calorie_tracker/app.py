import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import sqlite3

class CalorieTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Tracker")
        self.root.geometry("1500x800")  
        self.root.configure(bg="#ffe6f2") 
        self.theme_color = "#ffe6f2"  
        self.button_color = "#ff99cc"
        self.configure_theme(self.theme_color)  

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(9, weight=1)

        self.conn = sqlite3.connect('calorie_tracker.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            calories REAL NOT NULL,
            proteins REAL NOT NULL,
            fats REAL NOT NULL,
            carbohydrates REAL NOT NULL,
            date TEXT NOT NULL
        )
        ''')
        
        self.conn.commit()

        self.create_week_tracker()

        self.dishes = []
        self.load_dishes()

        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.create_input_fields(input_frame)

        self.add_button = ttk.Button(input_frame, text="Добавить блюдо", command=self.add_dish, style="Pink.TButton")
        self.add_button.grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")

        self.edit_button = ttk.Button(input_frame, text="Редактировать блюдо", command=self.edit_dish, style="Pink.TButton")
        self.edit_button.grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")

        self.search_label = ttk.Label(input_frame, text="Поиск блюда:", background=self.theme_color)
        self.search_label.grid(row=8, column=0, sticky="w")
        self.search_entry = ttk.Entry(input_frame)
        self.search_entry.grid(row=8, column=1, sticky="ew")

        self.search_button = ttk.Button(input_frame, text="Поиск", command=self.search_dish, style="Pink.TButton")
        self.search_button.grid(row=9, column=0, columnspan=2, pady=5, sticky="ew")

        self.dish_list = tk.Listbox(self.root, height=10, width=50, bg="#ffd9e8", fg="black", highlightbackground=self.theme_color)
        self.dish_list.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.select_button = ttk.Button(self.root, text="Выбрать блюдо", command=self.select_dish, style="Pink.TButton")
        self.select_button.grid(row=11, column=0, columnspan=2, pady=5, sticky="ew")

        self.plot_button = ttk.Button(self.root, text="Построить график", command=self.plot_calories, style="Pink.TButton")
        self.plot_button.grid(row=12, column=0, columnspan=2, pady=5, sticky="ew")

        self.bmi_button = ttk.Button(self.root, text="Калькулятор BMI", command=self.open_bmi_calculator, style="Pink.TButton")
        self.bmi_button.grid(row=13, column=0, columnspan=2, pady=5, sticky="ew")

        self.theme_button = ttk.Button(self.root, text="Сменить тему", command=self.toggle_theme, style="Pink.TButton")
        self.theme_button.grid(row=14, column=0, columnspan=2, pady=5, sticky="ew")



        self.fig_pie, self.ax_pie = plt.subplots()
        self.canvas_pie = FigureCanvasTkAgg(self.fig_pie, master=self.root)
        self.canvas_pie.get_tk_widget().grid(row=0, column=2, rowspan=13, padx=20, pady=20, sticky="nsew")

        self.root.bind('<Return>', self.handle_enter_key)  

        self.update_pie_chart()
    def configure_theme(self, color):
            """Конфигурирует цветовую тему приложения."""
            self.root.configure(bg=color)
            style = ttk.Style()
            style.configure("Pink.TButton", background=self.button_color, foreground="white", font=("Arial", 12))
            
        
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(background=color)
        
    def toggle_theme(self):
        if self.theme_color == "#ffe6f2": 
            self.theme_color = "#cce7ff"  
            self.button_color = "#66b3ff"  
        else:  
            self.theme_color = "#ffe6f2"  
            self.button_color = "#ff99cc"  

        self.configure_theme(self.theme_color)

    def open_bmi_calculator(self):
        bmi_window = tk.Toplevel(self.root)
        bmi_window.title("Калькулятор BMI")
        bmi_window.geometry("400x300")
        bmi_window.configure(bg="#ffe6f2")

        ttk.Label(bmi_window, text="Введите ваш вес (кг):").pack(pady=10)
        self.weight_entry = ttk.Entry(bmi_window)
        self.weight_entry.pack(pady=5)

        ttk.Label(bmi_window, text="Введите ваш рост (м):").pack(pady=10)
        self.height_entry = ttk.Entry(bmi_window)
        self.height_entry.pack(pady=5)

        ttk.Button(bmi_window, text="Рассчитать BMI", command=self.calculate_bmi).pack(pady=20)

        self.bmi_result_label = ttk.Label(bmi_window, text="")
        self.bmi_result_label.pack(pady=10)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = weight / ((height / 100) ** 2)
            self.bmi_result_label.config(text=f"Ваш BMI: {bmi:.2f}")
        except ValueError:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите корректные значения для веса и роста.")
        

    def create_input_fields(self, frame):
        labels = ["Название блюда:", "Калории (на 100г):", "Белки (на 100г):", "Жиры (на 100г):", "Углеводы (на 100г):", "Дата (YYYY-MM-DD):"]
        self.entries = []

        for i, label in enumerate(labels):
            ttk.Label(frame, text=label, background=self.theme_color).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, sticky="ew")
            self.entries.append(entry)

        self.name_entry, self.cal_entry, self.prot_entry, self.fat_entry, self.carb_entry, self.date_entry = self.entries

    def handle_enter_key(self, event):
        if self.root.focus_get() == self.search_entry:
            self.search_dish()
        elif self.root.focus_get() == self.add_button_entry:
            self.add_dish()
    
    def create_week_tracker(self):
        week_frame = ttk.Frame(self.root)
        week_frame.grid(row=20, column=0, columnspan=2, pady=10)  

        days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        self.day_labels = []
        
        for day in days:
            label = tk.Label(week_frame, text=day, bg="#ffe6f2", font=("Arial", 12))
            label.pack(side=tk.LEFT, padx=5)

            circle = tk.Canvas(week_frame, width=20, height=20, bg="#ffe6f2", highlightthickness=0)
            circle.create_oval(2, 2, 18, 18, fill="white")  
            circle.pack(side=tk.LEFT, padx=5)
            self.day_labels.append(circle)

        self.update_week_tracker() 

    def update_week_tracker(self):
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        self.cursor.execute("SELECT date FROM dishes")
        logged_dates = [row[0] for row in self.cursor.fetchall()]

        for i, day in enumerate(range(7)):
            current_day = start_of_week + datetime.timedelta(days=day)
            if str(current_day) in logged_dates:
                self.day_labels[i].itemconfig(1, fill="green")  
                self.day_labels[i].itemconfig(0, fill="green")  
            else:
                self.day_labels[i].itemconfig(0, fill="white")  
 
    def on_closing(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()

    def add_dish(self):
        name = self.name_entry.get()
        cal = self.cal_entry.get()
        prot = self.prot_entry.get()
        fat = self.fat_entry.get()
        carb = self.carb_entry.get()
        date = self.date_entry.get()

        if not name or not cal or not prot or not fat or not carb or not date:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Ошибка", "Неверный формат даты! Используйте YYYY-MM-DD.")
            return

        self.cursor.execute("INSERT INTO dishes (name, calories, proteins, fats, carbohydrates, date) VALUES (?, ?, ?, ?, ?, ?)",
                            (name, cal, prot, fat, carb, date))
        self.conn.commit()

        messagebox.showinfo("Успех", "Блюдо добавлено!")
        self.load_dishes()
        self.update_pie_chart() 
        self.update_week_tracker() 

    def edit_dish(self):
        selected = self.dish_list.curselection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите блюдо для редактирования!")
            return

        dish_name = self.dish_list.get(selected)
        dish = next((d for d in self.dishes if d['name'] == dish_name), None)

        if dish:
            self.name_entry.delete(0, tk.END)
            self.cal_entry.delete(0, tk.END)
            self.prot_entry.delete(0, tk.END)
            self.fat_entry.delete(0, tk.END)
            self.carb_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)

            self.name_entry.insert(0, dish['name'])
            self.cal_entry.insert(0, dish['calories'])
            self.prot_entry.insert(0, dish['proteins'])
            self.fat_entry.insert(0, dish['fats'])
            self.carb_entry.insert(0, dish['carbohydrates'])
            self.date_entry.insert(0, dish['date'])

            self.cursor.execute("DELETE FROM dishes WHERE id = ?", (dish['id'],))
            self.conn.commit()
            self.add_button.config(command=lambda: self.save_edited_dish(dish['id']))

    def save_edited_dish(self, dish_id):
        name = self.name_entry.get()
        cal = self.cal_entry.get()
        prot = self.prot_entry.get()
        fat = self.fat_entry.get()
        carb = self.carb_entry.get()
        date = self.date_entry.get()

        if not name or not cal or not prot or not fat or not carb or not date:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Ошибка", "Неверный формат даты! Используйте YYYY-MM-DD.")
            return

        self.cursor.execute("INSERT INTO dishes (id, name, calories, proteins, fats, carbohydrates, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (dish_id, name, cal, prot, fat, carb, date))
        self.conn.commit()

        messagebox.showinfo("Успех", "Блюдо обновлено!")
        self.load_dishes()
        self.update_pie_chart()  

        self.add_button.config(command=self.add_dish)
        self.update_week_tracker()

    def search_dish(self):
        search_term = self.search_entry.get().lower()
        self.dish_list.delete(0, tk.END)

        for dish in self.dishes:
            if search_term in dish['name'].lower():
                self.dish_list.insert(tk.END, dish['name'])

    def select_dish(self):
        selected = self.dish_list.curselection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите блюдо!")
            return
        dish_name = self.dish_list.get(selected)
        dish = next((d for d in self.dishes if d['name'] == dish_name), None)

        if dish:
            info = f"Калории: {dish['calories']} ккал\nБелки: {dish['proteins']} г\nЖиры: {dish['fats']} г\nУглеводы: {dish['carbohydrates']} г\nДата: {dish['date']}"
            messagebox.showinfo("Информация о блюде", info)

    def plot_calories(self):
        plot_window = tk.Toplevel(self.root)
        plot_window.title("График потребления калорий")
        plot_window.geometry("800x600")

        self.cursor.execute("SELECT date, SUM(calories) FROM dishes GROUP BY date")
        data = self.cursor.fetchall()

        if not data:
            messagebox.showinfo("Нет данных", "Данных для построения графика нет.")
            return

        dates = [datetime.datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
        calories = [row[1] for row in data]

        fig, ax = plt.subplots()
        ax.plot(dates, calories, marker='o', color='pink', label='Калории')
        ax.set_title('Динамика потребления калорий')
        ax.set_xlabel('Дата')
        ax.set_ylabel('Калории')
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        recommendation = self.get_calorie_recommendation(sum(calories))
        ttk.Label(plot_window, text=recommendation, font=("Arial", 14)).pack(pady=10)

    def get_calorie_recommendation(self, total_calories):
        if total_calories > 2500:  
            return "Рекомендуем уменьшить потребление калорий."
        else:
            return "Ваше потребление калорий в пределах нормы."

    def update_pie_chart(self):
        today = datetime.date.today()
        self.cursor.execute("SELECT SUM(calories), SUM(proteins), SUM(fats), SUM(carbohydrates) FROM dishes WHERE date = ?", (today,))
        data = self.cursor.fetchone()

        if data and any(data): 
            calories, proteins, fats, carbs = data
            labels = ['Калории', 'Белки', 'Жиры', 'Углеводы']
            sizes = [calories, proteins, fats, carbs]
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

            self.ax_pie.clear()  
            self.ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            self.ax_pie.axis('equal')  

            self.canvas_pie.draw() 
        else:
            self.ax_pie.clear()
            self.ax_pie.text(0.5, 0.5, "Нет данных за сегодня", ha='center', va='center', fontsize=12)
            self.ax_pie.axis('off')
            self.canvas_pie.draw()

    def load_dishes(self):
        self.cursor.execute("SELECT id, name, calories, proteins, fats, carbohydrates, date FROM dishes")
        rows = self.cursor.fetchall()
        self.dishes = [{'id': row[0], 'name': row[1], 'calories': row[2], 'proteins': row[3], 'fats': row[4], 'carbohydrates': row[5], 'date': row[6]} for row in rows]