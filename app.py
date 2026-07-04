import streamlit as st
import json
import os
from datetime import date

DATA_FILE = "todos.json"

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)

st.set_page_config(
    page_title="Smart To-Do Manager",
    page_icon="📝",
    layout="wide"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown("""
# 📝 Smart To-Do Manager

### Organize your tasks, set priorities, and stay productive every day.
""")

st.divider()
st.sidebar.title("📋 Menu")
st.sidebar.write("Welcome to Smart To-Do Manager!")

st.sidebar.info(
    """
    ### Features
    ✅ Add Tasks
    🔍 Search Tasks
    🎯 Set Priority
    📅 Due Dates
    📊 Progress Tracker
    """
)

if "todos" not in st.session_state:
    st.session_state.todos = load_todos()

# --- Add new task ---
with st.form("add_task", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("New task", label_visibility="collapsed", placeholder="Add a new task...")
        priority = st.selectbox(
            "Priority",
             ["High", "Medium", "Low"]
        )

        due_date =st.date_input("Due Date")
    with col2:
        submitted = st.form_submit_button("Add")
    if submitted and new_task.strip():
        st.session_state.todos.append({
            "task": new_task.strip(),
            "priority":priority,
            "due_date": str(due_date),
            "done": False,
            "created": str(date.today())
        })
        save_todos(st.session_state.todos)

st.divider()

# ---Search and Filter ---

search = st.text_input("🔍 Search tasks")

filter_choice = st.radio("Filter", ["All", "Active", "Completed"], horizontal=True, label_visibility="collapsed")

# --- Task list ---
if not st.session_state.todos:
    st.info("No tasks yet. Add one above!")
else:
    for i, todo in enumerate(st.session_state.todos): 
        
         if search.lower() not in todo["task"].lower():
            continue
         if filter_choice == "Active" and todo["done"]:
            continue
         if filter_choice == "Completed" and not todo["done"]:
            continue
         
         with st.container(border=True):

             col1, col2, col3 = st.columns([0.5, 4, 0.5])
             with col1:
                 checked = st.checkbox("", value=todo["done"], key=f"chk_{i}")
                 if checked != todo["done"]:
                    st.session_state.todos[i]["done"] = checked
                    save_todos(st.session_state.todos)
                    st.rerun()
        
   
             with col2:
                 if todo["priority"] == "High":
                    icon = "🔴"
                 elif todo["priority"] == "Medium":
                    icon = "🟡"
                 else:
                    icon = "🟢"

                 if todo["done"]:
                     st.markdown(f"~~{icon} {todo['task']}~~")
                 else:
                     st.markdown(f"{icon} {todo['task']}")

                 st.caption(f"📅 Due: {todo['due_date']}")

             with col3:
                 if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.todos.pop(i)
                    save_todos(st.session_state.todos)
                    st.rerun()           
st.divider()
remaining = len([t for t in st.session_state.todos if not t["done"]])
st.caption(f"{remaining} task(s) remaining")
total_tasks = len(st.session_state.todos)

if total_tasks > 0:
    completed_tasks = total_tasks - remaining
    progress = completed_tasks / total_tasks
else:
    completed_tasks = 0
    progress = 0
    st.progress(progress)
    st.caption(f"Progress: {progress:.0%}") 

    st.divider()
    st.subheader("📊 Task Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📋 Total", total_tasks)

    with col2:
        st.metric("✅ Completed", completed_tasks)

    with col3:
        st.metric("⏳ Remaining", remaining)

st.progress(progress)
st.caption(f"Progress: {progress:.0%}")
if st.button("🗑️ Clear Completed Tasks"):
        st.session_state.todos = [
        task for task in st.session_state.todos
        if not task["done"]
    ]
        save_todos(st.session_state.todos)
        st.rerun()        