async function generatePaper() {
    const prompt = document.getElementById("prompt").value;
    const model = document.getElementById("model").value;

    const response = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt, model: model })
    });

    const data = await response.json();
    document.getElementById("output").innerText = data.response;
}

document.getElementById("submit").addEventListener("click", generatePaper);
