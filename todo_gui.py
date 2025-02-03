import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

BG_COLOR = "#2C3E50"
TEXT_COLOR = "#ECF0F1"
BUTTON_COLOR = "#3498DB"
HIGHLIGHT_COLOR = "#1ABC9C"

class Task:
    def __init__(self, description, date = None, priority = 3, completed = False):
        self.description = description
        self.date = date
        self.priority = priority
        self.completed = completed
        
    def mark_completed(self):
        self.completed = not self.completed
        
    def to_dict(self):
        return {
            "description": self.description,
            "date": self.date,
            "priority": self.priority,
            "completed": self.completed
        }
        

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_from_file()
        
    def add_task(self, description, date, priority):
        if not description:
            return "Taks description cannot be empty!"
        task = Task(description, date, priority)
        self.tasks.append(task)
        self.save_to_file()
        return None
    
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()
            
    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_to_file()
            
    def save_to_file(self):
        with open("data.json", "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)
            
    def load_from_file(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.tasks = [Task(**t) for t in data]
        except FileNotFoundError:
            self.tasks = []
            

class ToDoApp:
    def __init__(self, root):
        self.todo_list = ToDoList()
        self.root = root
        self.root.title("To-Do List")
        self.root.configure(bg=BG_COLOR)
        self.create_widgets()
        self.refresh_list()
        
    def create_widgets(self):
        tk.Label(self.root, text="Task Description", bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0)
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Due Date (YYYY-MM-DD)", bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0)
        self.date_entry = tk.Entry(self.root, width=20)
        self.date_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Priority (1-5)", bg=BG_COLOR, fg=TEXT_COLOR).grid(row=2, column=0)
        self.priority_entry = tk.Entry(self.root, width=5)  # Ahora se define antes de usarse
        self.priority_entry.grid(row=2, column=1)

        self.task_list = tk.Listbox(self.root, width=50, height=10, bg=TEXT_COLOR)
        self.task_list.grid(row=3, column=0, columnspan=2)
        
        tk.Button(self.root, text="Add Task", command=self.add_task, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=4, column=0)
        tk.Button(self.root, text="Delete Task", command=self.delete_task, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=4, column=1)
        tk.Button(self.root, text="Complete Task", command=self.complete_task, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=5, column=0)
        tk.Button(self.root, text="Exit", command=self.root.quit, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=5, column=1)
        
    def refresh_list(self):
        self.task_list.delete(0, tk.END)
        for i, task in enumerate(self.todo_list.tasks):
            status = "✔" if task.completed else "✘"
            self.task_list.insert(tk.END, f"{status} {task.description} - Due: {task.date} - Priority: {task.priority}")
            
    def add_task(self):
        description = self.task_entry.get()
        date = self.date_entry.get()
        priority = self.priority_entry.get()
        error = self.todo_list.add_task(description, date, int(priority) if priority.isdigit() else 3)
        if error:
            messagebox.showerror("Error", error)
        else:
            self.refresh_list()
            self.task_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            
    def delete_task(self):
        try:
            index = self.task_list.curselection()[0]
            self.todo_list.remove_task(index)
            self.refresh_list()
        except IndexError:
            messagebox.showerror("Error", "No task selected!")
            
    def complete_task(self):
        try:
            index = self.task_list.curselection()[0]
            self.todo_list.mark_completed(index)
            self.refresh_list()
        except IndexError:
            messagebox.showerror("Error", "No task selected!")
            
            
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()