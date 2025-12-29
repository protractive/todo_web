const API = "http://localhost:8000";

async function loadTodos() {
    const res = await fetch(`${API}/todo`);
    const todos = await res.json();

    const list = document.getElementById("list");
    list.innerHTML = "";

    todos.forEach(t => {
        const li = document.createElement("li");
        li.textContent = '${t.id}. ${t.title} [${t.done ? "완료" : "미완료"}]';

        const btn = document.createElement("button");
        btn.textContent = "완료";
        btn.onclick = () => updatTodo(t.id);

        li.appendChild(btn);
        list.appendChild(li);
    });
}

async function addTodo() {
    const title = document.getElementById("title").value;

    await fetch(`${API}/todo`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title })
    });

    loadTodos();
}

async function updatTodo(id) {
    await fetch(`${API}/todo/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ done: true })
    });

    loadTodos();
}

loadTodos();