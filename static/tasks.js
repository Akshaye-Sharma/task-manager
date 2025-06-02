const token = localStorage.getItem("token");

fetch("/api/tasks", {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${token}`
  }
})

.then(response => {
  // console.log("Response status:", response.status);
  return response.text().then(text => {
    // console.log("Raw response:", text);
    // Try parsing JSON manually
    try {
      const data = JSON.parse(text);
      console.log("Parsed tasks:", data);
    } catch (e) {
      console.error("Failed to parse JSON:", e.message);
    }
  });
})

.catch(() => {
  console.error("There was an error fetching tasks:");
});