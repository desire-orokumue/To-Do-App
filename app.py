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

st.set_page_config(page_title="To-Do List", page_icon="✅", layout="centered")
st.title("✅ My To-Do List")

if "todos" not in st.session_state:
    st.session_state.todos = load_todos()

# --- Add new task ---
with st.form("add_task", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("New task", label_visibility="collapsed", placeholder="Add a new task...")
    with col2:
        submitted = st.form_submit_button("Add")
    if submitted and new_task.strip():
        st.session_state.todos.append({
            "task": new_task.strip(),
            "done": False,
            "created": str(date.today())
        })
        save_todos(st.session_state.todos)

st.divider()

# --- Filter ---
filter_choice = st.radio("Filter", ["All", "Active", "Completed"], horizontal=True, label_visibility="collapsed")

# --- Task list ---
if not st.session_state.todos:
    st.info("No tasks yet. Add one above!")
else:
    for i, todo in enumerate(st.session_state.todos):
        if filter_choice == "Active" and todo["done"]:
            continue
        if filter_choice == "Completed" and not todo["done"]:
            continue

        col1, col2, col3 = st.columns([0.5, 4, 0.5])
        with col1:
            checked = st.checkbox("", value=todo["done"], key=f"chk_{i}")
            if checked != todo["done"]:
                st.session_state.todos[i]["done"] = checked
                save_todos(st.session_state.todos)
                st.rerun()
        with col2:
            if todo["done"]:
                st.markdown(f"~~{todo['task']}~~")
            else:
                st.markdown(todo["task"])
        with col3:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.todos.pop(i)
                save_todos(st.session_state.todos)
                st.rerun()

st.divider()
remaining = len([t for t in st.session_state.todos if not t["done"]])
st.caption(f"{remaining} task(s) remaining")