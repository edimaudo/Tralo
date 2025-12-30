function openAlert(level, stakeholder) {
    const modal = document.getElementById('alertModal');
    const text = document.getElementById('templateText');
    const header = document.getElementById('modalTarget');
    
    header.innerText = `Target Recipient: ${stakeholder}`;
    
    // Fetch template based on the calculated risk level
    fetch(`/api/template/${level}`)
        .then(res => res.json())
        .then(data => {
            text.value = data.body;
            modal.style.display = 'block';
        });
}

function closeAlert() {
    document.getElementById('alertModal').style.display = 'none';
}

function confirmDispatch() {
    alert("Official Notification Dispatched via Secure Channel.");
    closeAlert();
}

// Ensure the modal closes if clicking outside of the content
window.onclick = function(event) {
    const modal = document.getElementById('alertModal');
    if (event.target == modal) {
        closeAlert();
    }
}
