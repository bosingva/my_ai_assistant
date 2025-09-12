const form = document.getElementById("chat-form");
const chatbox = document.getElementById("chatbox");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const msgInput = document.getElementById("message");
  const message = msgInput.value;

  // Show user message
  chatbox.innerHTML += `<div><b>You:</b> ${message}</div>`;
  msgInput.value = "";

  // Send to backend
  const response = await fetch("/chat", {
    method: "POST",
    body: new URLSearchParams({ message })
  });

  const data = await response.json();
  if (data.reply) {
    chatbox.innerHTML += `<div><b>Assistant:</b> ${data.reply}</div>`;
  } else {
    chatbox.innerHTML += `<div><b>Error:</b> ${data.error}</div>`;
  }
});
