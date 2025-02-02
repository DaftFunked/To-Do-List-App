import json
from datetime import datetime

class Task:
    def __init__(self, description, date = None, priority = "Medium", completed = False):
        "Initializes a new task."
        self.description = description
        self.completed = completed
        self.date = self.validate_date(date)
        self.priority = self.validate_priority(priority)
        
    def validate_date(self, date_str):
        "Validates the due date format."
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
        return None
    
    def validate_priority(self, priority):
        "Ensure priority is valid."
        if priority not in ["High", "Medium", "Low"]:
            return "Medium"
        return priority
    
    def mark_completed(self):
        "Marks the task as completed."
        self.completed = True
    
    def mark_pending(self):
        "Marks the task as pending."
        self.completed = False
        
    def __str__(self):
        "Returns a string representation of the task."
        status = "[✔]" if self.completed else "[ ]"
        due = f" (Due: {self.date})" if self.date else ""
        return f"{status} {self.description} - {self.priority}{due}"
    
    
class ToDoList:
    def __init__(self):
        "Initializes a list of tasks and charge from the JSON file if it exists."
        self.tasks = []
        self.load_from_file()
        
    def add_task(self, description, date = None, priority = "Medium"):
        "Adds a new task to the list."
        if not description.strip():
            print("Description cannot be empty.")
            return
        task = Task(description, date, priority)
        self.tasks.append(task)
        self.save_to_file()
        
    def show_tasks(self, filter_by = None):
        "Show all the tasks in the list."
        filtered_tasks = self.tasks
        if filter_by == "completed":
            filtered_tasks = [t for t in self.tasks if t.completed]
        elif filter_by == "pending":
            filtered_tasks = [t for t in self.tasks if not t.completed]
            
        sorted_tasks = sorted(filtered_tasks, key= lambda t : (t.priority == "High", t.priority == "Medium", t.date or "9999-12-31"), reverse=True)
        
        if not sorted_tasks:
            print("Not found.")
        else:
            for i, task in enumerate(sorted_tasks, 1):
                print(f"{i}. {task}")
        
    def mark_completed(self, index):
        "Mark a task as completed."
        if 1 <= index <= len(self.tasks):
            self.tasks[index - 1].mark_completed()
            self.save_to_file()
        else:
            print("Index does not exist.")
        
    def mark_pending(self, index):
        "Mark a task as pending."
        if 1 <= index <= len(self.tasks):
            self.tasks[index - 1].mark_pending()
            self.save_to_file()
        else:
            print("Index does not exist.")
        
    def delete_task(self, index):
        "Delete a task from the list."
        if 1 <= index <= len(self.tasks):
            del self.tasks[index - 1]
            self.save_to_file()
        else:
            print("Index does not exist.")
            
    def edit_task(self, index, new_description = None, new_date = None, new_priority = None):
        "Edit a task in the list."
        if 1 <= index <= len(self.tasks):
            task = self.tasks[index - 1]
            if new_description:
                task.description = new_description
            if new_date:
                task.date = task.validate_date(new_date)
            if new_priority:
                task.priority = task.validate_priority(new_priority)
            self.save_to_file()
        else:
            print("Index does not exist.")
            
    def search_task(self, query):
        results = [t for t in self.tasks if query.lower() in t.description.lower()]
        if results:
            for i, task in enumerate(results, 1):
                print(f"{i}. {task}")
        else:
            print("No tasks found.")
            
    def save_to_file(self):
        "Save the tasks to a JSON file."
        data = [
            {
                "description": t.description,
                "completed": t.completed,
                "date": t.date,
                "priority": t.priority
            }
            for t in self.tasks
        ]
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
            
    def load_from_file(self):
        "Load the tasks from a JSON file."
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.tasks = [Task(t["description"], t.get("date"), t.get("priority", "Medium"), t["completed"]) for t in data]
        except (FileNotFoundError, json.JSONDecodeError):
            pass # If the file does not exist, start with a empty list.
        
        
def show_menu():
    print("\n===== To-Do List =====")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Show completed tasks")
    print("4. Show pending tasks")
    print("5. Mark task as completed")
    print("6. Mark task as pending")
    print("7. Edit task")
    print("8. Delete task")
    print("9. Search task")
    print("10. Exit")
    
def main():
    list = ToDoList()
    while True:
        show_menu()
        option = input("Select an option: ")
        
        if option == "1":
            description = input("Enter the description of the task: ")
            date = input("Enter the due date (YYYY-MM-DD, optional): ") or None
            priority = input("Enter the priority (High, Medium, Low): ") or "Medium"
            list.add_task(description, date, priority)
        elif option == "2":
            list.show_tasks()
        elif option == "3":
            list.show_tasks("completed")
        elif option == "4":
            list.show_tasks("pending")
        elif option == "5":
            index = int(input("Enter task number: "))
            list.mark_completed(index)
        elif option == "6":
            index = int(input("Enter task number: "))
            list.mark_pending(index)
        elif option == "7":
            index = int(input("Enter task number: "))
            description = input("New description (leave blank to keep the same): ") or None
            date = input("New due date (YYYY-MM-DD, optional): ") or None
            priority = input("New priority (High, Medium, Low, optional): ") or None
            list.edit_task(index, description, date, priority)
        elif option == "8":
            index = int(input("Enter task number: "))
            list.delete_task(index)
        elif option == "9":
            query = input("Enter a search query: ")
            list.search_task(query)
        elif option == "10":
            print("Saving tasks and exiting.")
            break
        else:
            print("Invalid Option. Please try again.")
            
if __name__ == "__main__":
    main()