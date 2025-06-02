const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const messageEL = document.getElementById("login-message");

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
        messageEL.textContent = "Login successful!";
        messageEL.style.color = "green";
        setTimeout(() => {
          window.location.href = "/tasks";
        }, 1000);
      } else {
        messageEL.textContent = "Login failed";
        messageEL.style.color = "red";
      }
    } catch (error) {
      messageEL.textContent = "An error occurred.";
      messageEL.style.color = "red";
      console.error("Error:", error);
    }
  });
}

const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;
    const messageER = document.getElementById("reg-message");

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

        messageER.textContent = "Registration successful";
        messageER.style.color = "green";
      } else {
        messageER.textContent = "Registration failed";
        messageER.style.color = "red";
      }
    } catch (error) {
      messageER.textContent = "An error occurred.";
      messageER.style.color = "red";
      console.error("Error:", error);
    }
  });
}
