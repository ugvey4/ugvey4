import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            grade INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_student():
    name = entry_name.get()
    course = entry_course.get()
    grade = entry_grade.get()

    if not name or not course or not grade:
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
        return

    try:
        grade = int(grade)
        if grade < 1 or grade > 5:
            raise ValueError("Оценка должна быть от 1 до 5.")
    except ValueError as e:
        messagebox.showwarning("Warning", str(e))
        return

    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, course, grade) VALUES (?, ?, ?)', (name, course, grade))
        conn.commit()
        conn.close()

        entry_name.delete(0, tk.END)
        entry_course.delete(0, tk.END)
        entry_grade.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Студент успешно добавлен")
        show_students()
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))

def show_students():
    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        records = cursor.fetchall()
        conn.close()

        for row in tree.get_children():
            tree.delete(row)

        for record in records:
            tree.insert("", tk.END, values=record)
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))

def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Ошибка", "Выберите студента которого хотите удалить")
        return

    student_id = tree.item(selected_item)['values'][0]

    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успешно", "Студент удалён")
        show_students()
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))

def edit_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Ошибка", "Выберите студента которого хотите отредактировать")
        return

    student_id = tree.item(selected_item)['values'][0]
    name = entry_name.get()
    course = entry_course.get()
    grade = entry_grade.get()

    if not name or not course or not grade:
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
        return

    try:
        grade = int(grade)
        if grade < 1 or grade > 5:
            raise ValueError("Оценка должна быть от 1 до 5.")
    except ValueError as e:
        messagebox.showwarning("Ошибка", str(e))
        return

    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET name = ?, course = ?, grade = ? WHERE id = ?', (name, course, grade, student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успешно", "Студент успешно обновлен")
        show_students()
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Учет успеваемости студентов")

    # Поля ввода
    tk.Label(root, text="Имя студента").grid(row=0, column=0)
    entry_name = tk.Entry(root)
    entry_name.grid(row=0, column=1)

    tk.Label(root, text="Курс").grid(row=1, column=0)
    entry_course = tk.Entry(root)
    entry_course.grid(row=1, column=1)

    tk.Label(root, text="Оценка").grid(row=2, column=0)
    entry_grade = tk.Entry(root)
    entry_grade.grid(row=2, column=1)

    # Кнопки
    tk.Button(root, text="Добавить студента", command=add_student).grid(row=3, column=0)
    tk.Button(root, text="Редактировать студента", command=edit_student).grid(row=3, column=1)
    tk.Button(root, text="Удалить студента", command=delete_student).grid(row=4, column=0)
    tk.Button(root, text="Показать успеваемость", command=show_students).grid(row=4, column=1)

    # Таблица для отображения успеваемости
    tree = ttk.Treeview(root, columns=("ID", "Имя", "Курс", "Оценка"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Имя", text="Имя")
    tree.heading("Курс", text="Курс")
    tree.heading("Оценка", text="Оценка")
    tree.grid(row=5, columnspan=2)

    # Сортировка по столбцам
    def sort_treeview(col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        tree.heading(col, command=lambda: sort_treeview(col, not reverse))

    for col in ("ID", "Имя", "Курс", "Оценка"):
        tree.heading(col, text=col, command=lambda c=col: sort_treeview(c, False))

    create_db()
    show_students()
    root.mainloop()