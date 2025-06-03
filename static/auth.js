const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();
    const messageEL = document.getElementById("login-message");

    if (!username || !password) {
      messageEL.textContent = "Username and password are required.";
      messageEL.style.color = "red";
      return;
    }

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", username)
        messageEL.textContent = data.message;
        messageEL.style.color = "green";
        setTimeout(() => {
          window.location.href = "/tasks";
        }, 1000);
      } else {
        messageEL.textContent = data.message;
        messageEL.style.color = "red";
      }

    } catch (error) {
      messageEL.textContent = "An error occurred.";
      messageEL.style.color = "red";
      console.error("Error:", error.message);
    }
  });
}

const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("reg-username").value.trim();
    const password = document.getElementById("reg-password").value.trim();
    const messageER = document.getElementById("reg-message");

    if (!username || !password) {
      messageER.textContent = "Username and password are required.";
      messageER.style.color = "red";
      return;
    }

    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.access_token);

        messageER.textContent = data.message;
        messageER.style.color = "green";
      } else {
        messageER.textContent = data.message;
        messageER.style.color = "red";
      }
    } catch (error) {
      messageER.textContent = "An error occurred.";
      messageER.style.color = "red";
      console.error("Error:", error.message);
    }
  });
}
