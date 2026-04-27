import streamlit as st

# Initialize session state for tasks and completed tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []

def view_tasks():
    """Display all tasks in the to-do list"""
    if len(st.session_state.tasks) == 0:
        st.info("No tasks in your to-do list!")
        return

    st.subheader("Your To-Do List")
    for i, task in enumerate(st.session_state.tasks, 1):
        if task in st.session_state.completed_tasks:
            st.write(f"✅ {i}. {task}")
        else:
            st.write(f"⬜ {i}. {task}")

def add_task():
    """Add a new task"""
    st.subheader("Add New Task")
    new_task = st.text_input("Enter task:", key="new_task_input")

    if st.button("Add Task"):
        if new_task.strip():
            st.session_state.tasks.append(new_task.strip())
            st.success(f"Task added: {new_task}")
            st.rerun()  # Refresh the app to clear the input
        else:
            st.error("Task cannot be empty!")

def complete_task():
    """Mark a task as completed"""
    st.subheader("Complete Task")

    if len(st.session_state.tasks) == 0:
        st.info("No tasks to complete!")
        return

    view_tasks()

    # Create options for the selectbox
    task_options = [f"{i+1}. {task}" for i, task in enumerate(st.session_state.tasks)]
    selected_task = st.selectbox("Select task to complete:", task_options, key="complete_select")

    if st.button("Mark as Completed"):
        if selected_task:
            task_index = int(selected_task.split('.')[0]) - 1
            task_name = st.session_state.tasks[task_index]
            if task_name not in st.session_state.completed_tasks:
                st.session_state.completed_tasks.append(task_name)
                st.success(f"Task '{task_name}' marked as completed!")
            else:
                st.warning("Task is already completed!")

def remove_task():
    """Remove a task"""
    st.subheader("Remove Task")

    if len(st.session_state.tasks) == 0:
        st.info("No tasks to remove!")
        return

    view_tasks()

    # Create options for the selectbox
    task_options = [f"{i+1}. {task}" for i, task in enumerate(st.session_state.tasks)]
    selected_task = st.selectbox("Select task to remove:", task_options, key="remove_select")

    if st.button("Remove Task"):
        if selected_task:
            task_index = int(selected_task.split('.')[0]) - 1
            removed_task = st.session_state.tasks.pop(task_index)
            # Also remove from completed list if it was there
            if removed_task in st.session_state.completed_tasks:
                st.session_state.completed_tasks.remove(removed_task)
            st.success(f"Removed task: {removed_task}")

def clear_completed():
    """Clear all completed tasks"""
    st.subheader("Clear Completed Tasks")

    completed_count = len(st.session_state.completed_tasks)
    if completed_count == 0:
        st.info("No completed tasks to clear!")
        return

    st.write(f"You have {completed_count} completed task(s).")

    if st.button("Clear All Completed Tasks"):
        # Remove completed tasks from the main list
        st.session_state.tasks = [task for task in st.session_state.tasks if task not in st.session_state.completed_tasks]
        # Clear the completed tasks list
        st.session_state.completed_tasks = []
        st.success(f"Cleared {completed_count} completed task(s)!")

def clear_all():
    """Clear all tasks and exit"""
    st.subheader("Clear All Tasks")

    if len(st.session_state.tasks) == 0:
        st.info("No tasks to clear!")
        return

    st.warning(f"You are about to clear all {len(st.session_state.tasks)} task(s). This action cannot be undone!")

    if st.button("Clear All Tasks"):
        st.session_state.tasks = []
        st.session_state.completed_tasks = []
        st.success("All tasks cleared!")

# Main app
def main():
    st.title("📝 To-Do List Web App")
    st.markdown("---")

    # Sidebar for navigation
    st.sidebar.title("Menu")
    menu_options = ["View Tasks", "Add Task", "Complete Task", "Remove Task", "Clear Completed", "Clear All"]
    choice = st.sidebar.radio("Choose an action:", menu_options)

    # Main content area
    if choice == "View Tasks":
        view_tasks()

    elif choice == "Add Task":
        add_task()

    elif choice == "Complete Task":
        complete_task()

    elif choice == "Remove Task":
        remove_task()

    elif choice == "Clear Completed":
        clear_completed()

    elif choice == "Clear All":
        clear_all()

    # Display current task count in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Task Summary")
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len(st.session_state.completed_tasks)
    pending_tasks = total_tasks - completed_tasks

    st.sidebar.write(f"Total tasks: {total_tasks}")
    st.sidebar.write(f"Completed: {completed_tasks}")
    st.sidebar.write(f"Pending: {pending_tasks}")

if __name__ == "__main__":
    main()