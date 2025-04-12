async function fetchDialogue() {
    try {
        const response = await fetch('/dialogue');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        
        const data = await response.json();
        const dialogueDiv = document.getElementById('dialogue');
        const newLine = document.createElement('div');
        newLine.classList.add('line');
        newLine.innerHTML = `<span class="speaker">${data.speaker}:</span> ${data.line}`;
        dialogueDiv.appendChild(newLine);
        dialogueDiv.scrollTop = dialogueDiv.scrollHeight;
    } catch (err) {
        console.error("Dialogue fetch failed:", err);
        const errorDiv = document.getElementById('dialogue');
        errorDiv.innerHTML = `<div style="color: red;">Error fetching dialogue: ${err.message}</div>`;
    }
}

setInterval(fetchDialogue, 30000);
fetchDialogue();

