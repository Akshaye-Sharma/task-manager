const token = localStorage.getItem("token");
const displayMessage = document.getElementById("action-message");

const nameIcon = document.getElementById("username-display");
const username = localStorage.getItem("username");

nameIcon.textContent = username;


loadTasks();

document.getElementById("add-task").addEventListener("click", async () => {
  const descriptionInput = document.getElementById("add-desc");
  const description = descriptionInput?.value?.trim();

  if (!description) {
    displayMessage.textContent = "Task description cannot be empty.";
    return;
  }

  try {
    const response = await fetch("/api/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({description})
    });

    if (!response.ok) {
      displayMessage.textContent = "Failed to add task.";
      return;
    }

    const data = await response.json();
    displayMessage.textContent = data.message;
    descriptionInput.value = ""; // Clear input field after successful add
    loadTasks();

  } catch (error) {
    displayMessage.textContent = "There was an error sending the add task request.";
    console.error("Error sending the add task request:", error.message);
  }
});

document.getElementById("edit-task").addEventListener("click", async () => {
  const inputId = document.getElementById("edit-index");
  const descriptionInput = document.getElementById("edit-desc");

  const description = descriptionInput?.value?.trim();
  const taskId = inputId?.value?.trim();

  if (!taskId || isNaN(taskId)) {
    displayMessage.textContent = "Task ID must be a valid number.";
    return;
  }

  if (!description) {
    displayMessage.textContent = "Task description cannot be empty.";
    return;
  }

  try {
    const response = await fetch(`/api/tasks/${taskId}`, {
      method: "PATCH",
      headers: {
        "Content-type": "application/json",
        "Authorization" : `Bearer ${token}`
      },
      body: JSON.stringify({description})
    });

    if (!response.ok) {
      displayMessage.textContent = "Failed to edit task.";
      return;
    }

    const data = await response.json();
    displayMessage.textContent = data.message;

    inputId.value = "";           
    descriptionInput.value = "";   // Clear input field after successful add

    loadTasks();

  } catch (error) {
    displayMessage.textContent = "There was an error sending the edit task request.";
    console.error("Error sending the edit task request:", error.message);
  }
});

document.getElementById("delete-task").addEventListener("click", async () => {
  const inputId = document.getElementById("delete-index");
  const taskId = inputId?.value?.trim();

  if(!taskId || isNaN(taskId)) {
    displayMessage.textContent = "Task ID must be a valid number";
    return
  }

  try{
    const response = await fetch(`/api/tasks/${taskId}`, {
      method: "DELETE",
      headers: {
        "Authorization" : `Bearer ${token}`
      }
    })

    if (!response.ok) {
      displayMessage.textContent = "Failed to delete task.";
      return
    }

    const data = await response.json()
    displayMessage.textContent = data.message;

    inputId.value = "";   // Clear input field after successful delete
    loadTasks();

  } catch (error) {
    displayMessage.textContent = "There was an error sending the delete task request.";
    console.error("Error sending the delete task request:", error.message);
  }
});

document.getElementById("clear-tasks").addEventListener("click", async () => {
  try {
    const response = await fetch("/api/tasks/clear", {
      method: "DELETE", // Consider changing this to DELETE or POST (see note below)
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) {
      displayMessage.textContent = "Failed to clear tasks.";
      return;
    }

    const data = await response.json();
    displayMessage.textContent = data.message;

    loadTasks();

  } catch (error) {
    displayMessage.textContent = "There was an error sending the clear request.";
    console.error("Error sending the clear request:", error.message);
  }
});

async function loadTasks() {
  try {
    const response = await fetch("/api/tasks", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const text = await response.text();
    let data;

    try {
      data = JSON.parse(text);
    } catch (e) {
      console.error("Failed to parse JSON:", e.message);
      return;
    }

    console.log("Parsed tasks:", data);

    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

    if (Array.isArray(data)) {
      data.forEach(task => {
        const li = document.createElement("li");
        li.textContent = task;
        taskList.appendChild(li);
      });
    } else {
      console.warn("Expected an array of tasks, got:", data);
    }

  } catch (error) {
    console.error("There was an error fetching tasks:", error.message);
  }
}