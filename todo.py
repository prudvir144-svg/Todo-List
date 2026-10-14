
import json
import os
import sys

TASKS_FILE = "tasks.json"


def load_tasks():
    """Load tasks from JSON, or return an empty list."""
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            print("Error: tasks.json must contain a list.")
            return []

        return tasks

    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not load tasks: {error}")
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
        return True

    except OSError as error:
        print(f"Could not save tasks: {error}")
        return False


def add_task(tasks, description):
    description = description.strip()

    if not description:
        print("Task description cannot be empty.")
        return

    task = {
        "id": max((item.get("id", 0) for item in tasks), default=0) + 1,
        "description": description,
        "completed": False
    }

    tasks.append(task)

    if save_tasks(tasks):
        print(f"Task added: {description}")


def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    print("\n===== To-Do List =====")

    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        print(f'{task["id"]}. [{status}] {task["description"]}')


def complete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print("This task is already completed.")
                return

            task["completed"] = True

            if save_tasks(tasks):
                print(f'Task completed: {task["description"]}')
            return

    print(f"Task ID {task_id} was not found.")


def main():
    tasks = load_tasks()

    if len(sys.argv) < 2:
        print("To-Do List CLI")
        print("Commands:")
        print('  python todo.py add "Buy milk"')
        print("  python todo.py list")
        print("  python todo.py done 1")
        return

    command = sys.argv[1].lower()

    if command == "add":
        description = " ".join(sys.argv[2:])
        add_task(tasks, description)

    elif command == "list":
        list_tasks(tasks)

    elif command == "done":
        if len(sys.argv) != 3:
            print("Usage: python todo.py done <task_id>")
            return

        try:
            task_id = int(sys.argv[2])
            if task_id < 1:
                raise ValueError
        except ValueError:
            print("Please provide a valid positive task ID.")
            return

        complete_task(tasks, task_id)

    else:
        print("Unknown command. Use add, list, or done.")


if __name__ == "__main__":
    main()
