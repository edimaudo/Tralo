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

   function triggerAction(actionName, borrower) {
            const message = `Workflow Initiated: ${actionName} for ${borrower}.`;
            const toast = document.createElement('div');
            toast.style.position = 'fixed';
            toast.style.bottom = '20px';
            toast.style.right = '20px';
            toast.style.background = 'var(--navy)';
            toast.style.color = 'white';
            toast.style.padding = '15px 25px';
            toast.style.borderRadius = '4px';
            toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.2)';
            toast.style.zIndex = '1000';
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }



function executeWorkflow(level) {
    const message = level === 'CRITICAL' 
        ? "ACTION: Technical Breach Memorandum initiated for Credit Committee review." 
        : "ACTION: Compliance status logged. RM notification dispatched.";
    alert(message);
}

function toggleDetails(id) {
    const el = document.getElementById(`details-${id}`);
    el.style.display = (el.style.display === 'none') ? 'table-row' : 'none';
}

function triggerWorkflow(level) {
    const msg = level === 'CRITICAL' 
        ? "ACTION: Formal technical breach memorandum initiated for Credit Committee." 
        : "ACTION: Facility status logged. Notification dispatched to Relationship Manager.";
    alert(msg);
}

function runWorkflow(level) {
    const msg = level === 'CRITICAL' 
        ? "ESCALATION: Generating Formal Notice of Technical Breach for Credit Committee approval." 
        : "WORKFLOW: Notification status updated. Dispatching inquiry to Relationship Manager.";
    alert(msg);
}

// Ensure the modal closes if clicking outside of the content
window.onclick = function(event) {
    const modal = document.getElementById('alertModal');
    if (event.target == modal) {
        closeAlert();
    }
}
