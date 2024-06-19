import tkinter as tk
from tkinter import messagebox
import sqlite3

# Création de la base de données et de la table des tâches
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()

# Ajouter une tâche
def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task, completed) VALUES (?, ?)', (task, 0))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Entrée vide", "Veuillez entrer une tâche.")

# Charger les tâches
def load_tasks():
    task_list.delete(0, tk.END)
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    for row in cursor.fetchall():
        task_list.insert(tk.END, row)
    conn.close()

# Marquer une tâche comme terminée
def mark_completed():
    selected_task = task_list.curselection()
    if selected_task:
        task_id = task_list.get(selected_task)[0]
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    else:
        messagebox.showwarning("Sélection vide", "Veuillez sélectionner une tâche à marquer comme terminée.")

# Supprimer une tâche
def delete_task():
    selected_task = task_list.curselection()
    if selected_task:
        task_id = task_list.get(selected_task)[0]
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    else:
        messagebox.showwarning("Sélection vide", "Veuillez sélectionner une tâche à supprimer.")

# Initialisation de l'interface utilisateur
root = tk.Tk()
root.title("Gestionnaire de tâches")

task_frame = tk.Frame(root)
task_frame.pack(pady=10)

task_entry = tk.Entry(task_frame, width=50)
task_entry.pack(side=tk.LEFT, padx=10)

add_task_button = tk.Button(task_frame, text="Ajouter tâche", command=add_task)
add_task_button.pack(side=tk.LEFT)

task_list = tk.Listbox(root, width=50, height=10)
task_list.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

complete_task_button = tk.Button(button_frame, text="Marquer comme terminée", command=mark_completed)
complete_task_button.pack(side=tk.LEFT, padx=10)

delete_task_button = tk.Button(button_frame, text="Supprimer tâche", command=delete_task)
delete_task_button.pack(side=tk.LEFT, padx=10)

# Initialiser la base de données et charger les tâches
init_db()
load_tasks()

root.mainloop()