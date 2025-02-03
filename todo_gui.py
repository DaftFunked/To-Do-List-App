import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

BG_COLOR = "#2C3E50"
TEXT_COLOR = "#ECF0F1"
BUTTON_COLOR = "#3498DB"

class Task:
    def __init__(self, description, date=None, priority="Medium", completed=False):
        self.description = description
        self.completed = completed
        self.date = self.validate_date(date)
        self.priority = self.validate_priority(priority)
    
    def validate_date(self, date_str):
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                return None
        return None
    
    def validate_priority(self, priority):
        return priority if priority in ["High", "Medium", "Low"] else "Medium"
    
    def toggle_status(self):
        self.completed = not self.completed
    
    def to_dict(self):
        return {"description": self.description, "date": self.date, "priority": self.priority, "completed": self.completed}

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_from_file()
    
    def add_task(self, description, date=None, priority="Medium"):
        if not description.strip():
            return
        self.tasks.append(Task(description, date, priority))
        self.save_to_file()
    
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()
    
    def toggle_task_status(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].toggle_status()
            self.save_to_file()
    
    def edit_task(self, index, new_description=None, new_date=None, new_priority=None):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            if new_description:
                task.description = new_description
            if new_date:
                task.date = task.validate_date(new_date)
            if new_priority:
                task.priority = task.validate_priority(new_priority)
            self.save_to_file()
    
    def save_to_file(self):
        with open("data.json", "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)
    
    def load_from_file(self):
        try:
            with open("data.json", "r") as file:
                self.tasks = [Task(**t) for t in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
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
        
        tk.Label(self.root, text="Priority (High, Medium, Low)", bg=BG_COLOR, fg=TEXT_COLOR).grid(row=2, column=0)
        self.priority_entry = tk.Entry(self.root, width=10)
        self.priority_entry.grid(row=2, column=1)
        
        self.task_list = tk.Listbox(self.root, width=50, height=10, bg=TEXT_COLOR)
        self.task_list.grid(row=3, column=0, columnspan=2)
        
        tk.Button(self.root, text="Add Task", command=self.add_task, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=4, column=0)
        tk.Button(self.root, text="Delete Task", command=self.delete_task, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=4, column=1)
        tk.Button(self.root, text="Toggle Status", command=self.toggle_task_status, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=5, column=0)
        tk.Button(self.root, text="Edit Task", command=self.edit_task, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=5, column=1)
        tk.Button(self.root, text="Exit", command=self.root.quit, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=6, column=0, columnspan=2)
    
    def refresh_list(self):
        self.task_list.delete(0, tk.END)
        for i, task in enumerate(self.todo_list.tasks):
            status = "✔" if task.completed else "✘"
            due = f" (Due: {task.date})" if task.date else ""
            self.task_list.insert(tk.END, f"{status} {task.description} - {task.priority}{due}")
    
    def add_task(self):
        description = self.task_entry.get()
        date = self.date_entry.get()
        priority = self.priority_entry.get()
        self.todo_list.add_task(description, date, priority)
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
    
    def toggle_task_status(self):
        try:
            index = self.task_list.curselection()[0]
            self.todo_list.toggle_task_status(index)
            self.refresh_list()
        except IndexError:
            messagebox.showerror("Error", "No task selected!")
    
    def edit_task(self):
        try:
            index = self.task_list.curselection()[0]
            task = self.todo_list.tasks[index]
            new_description = simpledialog.askstring("Edit Task", "New description:", initialvalue=task.description)
            new_date = simpledialog.askstring("Edit Task", "New due date (YYYY-MM-DD):", initialvalue=task.date or "")
            new_priority = simpledialog.askstring("Edit Task", "New priority (High, Medium, Low):", initialvalue=task.priority)
            
            if new_description:
                self.todo_list.edit_task(index, new_description, new_date, new_priority)
                self.refresh_list()
        except IndexError:
            messagebox.showerror("Error", "No task selected!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
