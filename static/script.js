async function fetchDialogue() {
    const response = await fetch('/dialogue');
    const data = await response.json();

    const dialogueDiv = document.getElementById('dialogue');
    const newLine = document.createElement('div');
    newLine.classList.add('line');
    newLine.innerHTML = `<span class="speaker">${data.speaker}:</span> ${data.line}`;
    dialogueDiv.appendChild(newLine);
    dialogueDiv.scrollTop = dialogueDiv.scrollHeight;
}

setInterval(fetchDialogue, 30000); // Updates every 30 seconds
fetchDialogue(); // Initial call
