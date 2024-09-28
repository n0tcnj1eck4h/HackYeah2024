let tb = document.getElementById("tb");
let span = document.getElementById("below");
let url_box = document.getElementById("url_box");
let interval;

function query_and_update_state() { }

tb.onsubmit = async function(e) {
  e.preventDefault();
  const form = document.getElementById("tb");
  const formData = new FormData(form);

  try {
    const response = await fetch("localhost:5000/task/0", {
      method: "GET",
      body: formData,
    });

    const result = await response.json();

    span.innerText = JSON.stringify(result);
  } catch (error) {
    console.error("Error:", error);
  }
  // interval = setInterval(query_and_update_state, 1000);
};
