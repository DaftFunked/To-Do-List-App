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
        task = Task(description, date, priority)
        self.tasks.append(task)
        self.save_to_file()
        
    def edit_task(self, index, new_description = None, new_date = None, new_priority = None):
        "Edit a task in the list."
        if 1 <= index <= len(self.tasks):
            self.tasks[index - 1].edit_task(new_description, new_date, new_priority)
            self.save_to_file()
        else:
            print("Index does not exist.")
        
    def show_tasks(self):
        "Show all the tasks in the list."
        if not self.tasks:
            print("You don't have task on the list.")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task}")
                
    def mark_completed(self, index):
        "Mark a task as completed."
        if 1 <= index <= len(self.tasks):
            self.tasks[index - 1].mark_completed()
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
                self.tasks = [Task(t["description"], t.get("date"), t.get("priority", "Medium")) for t in data]
                for i, task in enumerate(self.tasks):
                    if data[i]["completed"]:
                        task.mark_completed()
                        
        except FileNotFoundError:
            pass # If the file does not exist, start with a empty list.
        
        
def show_menu():
    print("\n===== To-Do List =====")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Edit task")
    print("4. Mark task as completed")
    print("5. Delete task")
    print("6. Exit")
    
def main():
    list = ToDoList()
    
    while True:
        show_menu()
        option = input("Select an option: ")
        
        if option == "1":
            description = input("Enter the description of the task: ")
            date = input("Enter the due date (YYYY-MM-DD) or leave blank: ") or None
            priority = input("Enter the priority (High, Medium, Low) or leave blank: ") or "Medium"
            list.add_task(description, date, priority)
            
        elif option == "2":
            list.show_tasks()
            
        elif option == "3":
            list.show_tasks()
            try:
                index = int(input("Enter the number of the task to edit: "))
                new_description = input("New description (leave blank to keep): ") or None
                new_date = input("New due date (YYYY-MM-DD, leave blank to keep): ") or None
                new_priority = input("New priority (Low, Medium, High, leave blank to keep): ") or None
                list.edit_task(index, new_description, new_date, new_priority)
            except ValueError:
                print("Please enter a valid number.")
                
        elif option == "4":
            list.show_tasks()
            try:
                index = int(input("Enter the task number to mark as completed:"))
                list.mark_completed(index)
            except ValueError:
                print("Please enter a valid number.")
                
        elif option == "5":
            list.show_tasks()
            try:
                index = int(input("Enter the task number to delete: "))
                list.delete_task(index)
            except ValueError:
                print("Please enter a valid number.")
        
        elif option == "6":
            print("Saving tasks and exiting...")
            list.save_to_file()
            break
        
        else:
            print("Invalid Option. Please try again.")
            
            
if __name__ == "__main__":
    main()