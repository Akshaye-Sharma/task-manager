const token = localStorage.getItem("token");

loadTasks();

document.getElementById("add-task").addEventListener("click", () => {
  const description = document.getElementById("add-desc").value;
  fetch("/api/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({description})
  })
  .then(response => {
    const displayMessage = document.getElementById("action-message");
    if (response.ok){
      response.json().then(data => {
        displayMessage.textContent = data.message;
      })
      loadTasks();
    } else {
      displayMessage.textContent = "Failed to add task.";
    }
  })
  .catch(error => {
    const displayMessage = document.getElementById("action-message");
    displayMessage.textContent = "There was an error sending the add task request.";
    console.error("There was an error sending the clear request: ", error.message);
  })
})

document.getElementById("clear-tasks").addEventListener("click", () => {
  fetch("/api/tasks/clear", {
    method: "GET",
    headers: {
      "Authorization" :`Bearer ${token}`
    }
  })
  .then(response => {
    const displayMessage = document.getElementById("action-message");
    if (response.ok){
      response.json().then(data => {
        displayMessage.textContent = data.message;
      });
      loadTasks();
    } else {
      displayMessage.textContent = "Failed to clear tasks.";
    }
  })
  .catch(error => {
    const displayMessage = document.getElementById("action-message");
    displayMessage.textContent = "There was an error sending the clear request";
    console.error("There was an error sending the clear request: ", error.message);
  });
})

function loadTasks() {
  fetch("/api/tasks", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  .then(response => {
    return response.text().then(text => {
      try {
        const data = JSON.parse(text);
        console.log("Parsed tasks:", data);

        const taskList = document.getElementById("task-list");
        taskList.innerHTML = "";

        if (Array.isArray(data)) {
          data.forEach(element => {
            const li = document.createElement("li");
            li.textContent = element;
            taskList.appendChild(li);
          });
        } else {
          // Optional: handle non-array response (e.g. status message)
          console.warn("Expected an array of tasks, got:", data);
        }

      } catch (e) {
        console.error("Failed to parse JSON:", e.message);
      }
    });
  })
  .catch(() => {
    console.error("There was an error fetching tasks.");
  });
}
