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

/*
function toggleDetails(id) {
    const el = document.getElementById(`details-${id}`);
    el.style.display = (el.style.display === 'none') ? 'table-row' : 'none';
}
*/

function triggerWorkflow(level) {
    if (level === 'CRITICAL') {
        alert("CRITICAL ESCALATION: Generating Credit Committee Breach Memo...");
    } else {
        alert("MANAGEMENT ACTION: Updating compliance log and notifying RM.");
    }
}

function toggleDetails(id) {
    const el = document.getElementById(`details-${id}`);
    el.style.display = (el.style.display === 'none') ? 'table-row' : 'none';
}

function executeWorkflow(level) {
    const message = level === 'CRITICAL' 
        ? "ACTION: Technical Breach Memorandum initiated for Credit Committee review." 
        : "ACTION: Compliance status logged. RM notification dispatched.";
    alert(message);
}

// Ensure the modal closes if clicking outside of the content
window.onclick = function(event) {
    const modal = document.getElementById('alertModal');
    if (event.target == modal) {
        closeAlert();
    }
}
