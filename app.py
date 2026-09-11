"""
To-do list manager.
Add, view, complete and delete tasks. Tasks are saved to a file so they
are still there the next time you run the program.
"""

import json
import os

SAVE_FILE = "tasks.json"


def load_tasks():
    """Read tasks from the save file, or start fresh if it doesn't exist."""
    if not os.path.exists(SAVE_FILE):
        return []
    with open(SAVE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    with open(SAVE_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def show_tasks(tasks):
    if not tasks:
        print("\nYour list is empty.")
        return

    print("\nYour tasks:")
    for i, task in enumerate(tasks, start=1):
        mark = "[x]" if task["done"] else "[ ]"
        priority = task["priority"].upper()
        print(f"  {i}. {mark} ({priority}) {task['title']}")

    done_count = sum(1 for t in tasks if t["done"])
    print(f"\n{done_count} of {len(tasks)} completed.")


def add_task(tasks):
    title = input("Task description: ").strip()
    if not title:
        print("Task can't be empty.")
        return

    priority = input("Priority (low/medium/high) [medium]: ").strip().lower()
    if priority not in ("low", "medium", "high"):
        priority = "medium"

    tasks.append({"title": title, "priority": priority, "done": False})
    save_tasks(tasks)
    print(f"Added: {title}")


def pick_task(tasks, action):
    """Ask the user for a task number and return its index, or None."""
    if not tasks:
        print("No tasks to " + action + ".")
        return None

    show_tasks(tasks)
    text = input(f"Number of task to {action}: ").strip()

    if not text.isdigit():
        print("Please enter a task number.")
        return None

    index = int(text) - 1
    if index < 0 or index >= len(tasks):
        print("No task with that number.")
        return None

    return index


def complete_task(tasks):
    index = pick_task(tasks, "complete")
    if index is None:
        return
    tasks[index]["done"] = True
    save_tasks(tasks)
    print(f"Marked as done: {tasks[index]['title']}")


def delete_task(tasks):
    index = pick_task(tasks, "delete")
    if index is None:
        return
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted: {removed['title']}")


def clear_completed(tasks):
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    save_tasks(tasks)
    print(f"Removed {before - len(tasks)} completed task(s).")


def main():
    tasks = load_tasks()

    menu = {
        "1": ("View tasks", lambda: show_tasks(tasks)),
        "2": ("Add task", lambda: add_task(tasks)),
        "3": ("Complete task", lambda: complete_task(tasks)),
        "4": ("Delete task", lambda: delete_task(tasks)),
        "5": ("Clear completed", lambda: clear_completed(tasks)),
    }

    while True:
        print("\n===== TO-DO LIST =====")
        for key, (label, _) in menu.items():
            print(f"{key}. {label}")
        print("6. Quit")

        choice = input("Choose: ").strip()

        if choice == "6":
            print("Bye! Your tasks are saved.")
            break

        if choice in menu:
            menu[choice][1]()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
