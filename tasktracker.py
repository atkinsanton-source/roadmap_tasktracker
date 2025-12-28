

import sys
import json
import datetime
from tabulate import tabulate

def add_task (task_name):
    tasks_list = load_tasks()
    #Find max id and name new id max id + 1
    if tasks_list:
        max_id = max(task["id"] for task in tasks_list)
        id = max_id + 1
    else:
        id = 1

    # Create a new task dictionary
    status = "todo"
    task = {
        "id" : id,
        "name" : task_name,
        "status" : status,
        "created_at" : datetime.datetime.now().isoformat(),
        "updated_at" : None

    }
    tasks_list.append(task)
    save_tasks(tasks_list)
    row = [task["id"], task["name"], task["status"], task["created_at"], task["updated_at"]]
    tablify([row])
    print(f"Task added succesfully (ID: {id})")
    


def update_task(task_id, new_task_name):
    tasks_list = load_tasks()
    for task in tasks_list:
        if int(task["id"]) == task_id:
            task["name"] = new_task_name
            task["updated_at"] = datetime.datetime.now().isoformat()
            save_tasks(tasks_list)
            row = [task["id"], task["name"], task["status"], task["created_at"], task["updated_at"]]
            tablify([row])
            print(f"Updated task: {task_id} to {new_task_name} at {datetime.datetime.now().isoformat()}")

def mark_in_progress (task_id):
    tasks_list = load_tasks()
    for task in tasks_list:
        if int(task["id"]) == task_id:
            old_status = task["status"]
            task["status"] = "in-progress"
            task["updated_at"] = datetime.datetime.now().isoformat()
            save_tasks(tasks_list)
            row = [task["id"], task["name"], task["status"], task["created_at"], task["updated_at"]]
            tablify([row])
            print(f"Changed Satus: Task ID:{task_id}, from {old_status} to in-progress at {datetime.datetime.now().isoformat()}")

def mark_done (task_id):
    tasks_list = load_tasks()
    for task in tasks_list:
        if int(task["id"]) == task_id:
            old_status = task["status"]
            task["status"] = "done"
            task["updated_at"] = datetime.datetime.now().isoformat()
            save_tasks(tasks_list)
            row = [task["id"], task["name"], task["status"], task["created_at"], task["updated_at"]]
            tablify([row])
            print(f"Changed Satus: Task ID:{task_id}, from {old_status} to done at {datetime.datetime.now().isoformat()}. Well Done!")


def load_tasks():
    # Open and load the JSON file in read mode
    try:
        with open("tasks-cli.json", "r") as file:
            tasks_list = json.load(file)
    except FileNotFoundError:
        print("Error: tasks-cli.json file not found.")
        tasks_list = [] 
    except json.JSONDecodeError:
        print("Error: JSON decode error.")
        tasks_list = []
    except:
        print("Error: Could not read tasks-cli.json file.")
        tasks_list = []
    return tasks_list

def save_tasks(tasks_list):
    with open("tasks-cli.json", "w") as file:
        json.dump(tasks_list, file)
        

def list_tasks(sort_by = None):
    tasks_list = load_tasks()
    if sort_by == None:
        tasks_to_show = [[task["id"], task["name"], task["status"], task["created_at"], task["updated_at"]] for task in tasks_list]
            
    else:
        tasks_to_show = [[task["id"], task["name"], task["status"], task["created_at"], task["updated_at"]] for task in tasks_list if task["status"]==sort_by]

    tablify(tasks_to_show)


def tablify (tasks_to_show):
    headers = ["ID", "Task Name", "Status", "Created at", "Updated at"]
    print(tabulate(tasks_to_show, headers, tablefmt="double_outline"))

def delete_task(task_id):
    tasks_list = load_tasks()
    filtered_tasks = [task for task in tasks_list if int(task["id"]) != task_id]
    save_tasks(filtered_tasks)
    print(f"Task {task_id} deleted successfully")


                

#Controller loop
if __name__ == "__main__":
    
    #Haupt controller loop
    if sys.argv[1] == "add":
        try:
            task_name = sys.argv[2]
            add_task(task_name)
        except IndexError:
            print("Usage: python add <task_name>")

    elif sys.argv[1] == "update":
        try:
            new_task_name = sys.argv[3]
            task_id = int(sys.argv[2])
            update_task(task_id, new_task_name)
        except IndexError:
            print("Usage: python update <ID> <New task name>")
    
    elif sys.argv[1] == "mark-in-progress":
        try:
            task_id = int(sys.argv[2])
            mark_in_progress(task_id)
        except IndexError:
            print("Usage: python mark-in-progress <ID>")
    
    elif sys.argv[1] == "mark-done":
        try:
            task_id = int(sys.argv[2])
            mark_done(task_id)
        except IndexError:
            print("Usage: python mark-done <ID>")
    
    elif sys.argv[1] == "list":
        try:
            sort_by = sys.argv[2]
            list_tasks(sort_by)
        except IndexError:
            list_tasks(None)
    
    elif sys.argv[1] == "delete":
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except IndexError:
            print("Usage: python delete <task id>")
    

    
            
        