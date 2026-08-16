const API_URL = "http://127.0.0.1:8000";

const taskForm = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const titleError = document.getElementById("title-error");
const taskList = document.getElementById("task-list");

// Load from localStorage first
function loadFromCache() {
    const cached = localStorage.getItem("tasks");
    if (cached) {
        renderTasks(JSON.parse(cached));
    }
}

async function fetchTasks() {
    try {
        const res = await fetch(`${API_URL}/tasks/`);
        const tasks = await res.json();
        localStorage.setItem("tasks", JSON.stringify(tasks));
        renderTasks(tasks);
    } catch (err) {
        console.error(err);
        taskList.innerHTML = "<p>Error loading tasks. Is the backend running?</p>";
    }
}

function renderTasks(tasks) {
    taskList.innerHTML = "";
    if (tasks.length === 0) {
        taskList.innerHTML = "<p>No tasks yet.</p>";
        return;
    }

    tasks.forEach(task => {
        const div = document.createElement("div");
        div.className = "task-item";

        const info = document.createElement("div");
        info.className = "task-info";

        const title = document.createElement("h3");
        title.textContent = task.title;

        const meta = document.createElement("div");
        meta.className = "meta";
        meta.textContent = `Priority: ${task.priority} | Due: ${task.due_date || "—"} | Status: ${task.status}`;

        info.appendChild(title);
        info.appendChild(meta);

        const actions = document.createElement("div");
        actions.className = "actions";

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "delete-btn";
        deleteBtn.textContent = "Delete";
        deleteBtn.addEventListener("click", () => deleteTask(task.id));

        actions.appendChild(deleteBtn);

        div.appendChild(info);
        div.appendChild(actions);
        taskList.appendChild(div);
    });
}

async function deleteTask(id) {
    await fetch(`${API_URL}/tasks/${id}`, { method: "DELETE" });
    fetchTasks();
}

taskForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = titleInput.value.trim();
    if (!title) {
        titleError.textContent = "Title cannot be empty";
        return;
    }
    titleError.textContent = "";

    const body = {
        title: title,
        priority: document.getElementById("priority").value,
        due_date: document.getElementById("due_date").value || null,
        project_id: parseInt(document.getElementById("project_id").value) || 1
    };

    await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    taskForm.reset();
    fetchTasks();
});

// Initial load
loadFromCache();
fetchTasks();