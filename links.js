const apiUrl = 'https://app-de-tarefas-com-crud.onrender.com/tasks';
async function loadTasks() {
  const res = await fetch(apiUrl);
  const tasks = await res.json();

  const list = document.getElementById("taskList");
  list.innerHTML = ''; // limpa antes de renderizar

  tasks.forEach(task => {
    const li = document.createElement("li");
    li.className = task.done ? 'done' : '';
    li.textContent = task.title;

    // Marcar como concluída ao clicar
    li.onclick = () => toggleDone(task.id, !task.done);

    // Botão de deletar
    const delBtn = document.createElement("button");
    delBtn.textContent = "🗑️";
    delBtn.onclick = (e) => {
      e.stopPropagation();
      deleteTask(task.id);
    };

    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

async function addTask() {
  const input = document.getElementById("taskInput");
  const title = input.value.trim();
  if (!title) return;

  await fetch(apiUrl, {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title })
  });

  input.value = '';
  loadTasks();
}

async function toggleDone(id, done) {
  await fetch(`${apiUrl}/${id}`, {
    method: "PUT",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ done })
  });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`${apiUrl}/${id}`, {
    method: "DELETE"
  });
  loadTasks();
}

// Inicializa
loadTasks();

async function addTask(){
    const input = document.etElementById("taskInput");
    const title = input.value.trim();
    if (!title) return;
    
    await fetch(apiUrl, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringfy({title})
    });
    input.value = "";
    loadTasks();
}

async function toggleDone(id,done){
    await fetch ("${apiUrl}/${id}", {
        method: "PUT",
        headers: {"Content-Type": "aaplication/json"},
        body: JSON.stringfy({done})
    });
    loadTasks();
}

async function deleteTask(id){
    await fetch ("${apiUrl}/${id}", {
        method: "DELETE"
    });
    loadTasks();
}

loadTasks();
