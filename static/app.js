// app.js - UPDATED

let currentScanId = null;
let pollInterval = null;
const startButton = document.getElementById("startScanButton");
const statusOutput = document.getElementById("statusOutput");
const resultsOutput = document.getElementById("resultsOutput");
const scanMessageEl = document.getElementById("scanMessage");

// Initial state cleanup
resultsOutput.innerText = "[]";
statusOutput.innerText = JSON.stringify({ "status": "Awaiting scan start..." }, null, 2);

function setButtonState(isScanning) {
    startButton.disabled = isScanning;
    if (isScanning) {
        startButton.innerHTML = '<span class="spinner"></span> Scanning...';
    } else {
        startButton.innerText = "Start Scan";
    }
}

function displayMessage(message, type = 'success') {
    scanMessageEl.innerText = message;
    scanMessageEl.style.display = 'block';
    // Simple color styling based on type (requires CSS update)
    scanMessageEl.style.backgroundColor = type === 'error' ? '#f8d7da' : '#d4edda';
    scanMessageEl.style.color = type === 'error' ? '#721c24' : '#155724';
    scanMessageEl.style.border = type === 'error' ? '1px solid #f5c6cb' : '1px solid #c3e6cb';
}

async function startScan() {
    // Clear previous results/messages
    scanMessageEl.style.display = 'none';
    resultsOutput.innerText = "[]";
    statusOutput.innerText = JSON.stringify({ "status": "Starting scan..." }, null, 2);
    if (pollInterval) clearInterval(pollInterval);
    
    setButtonState(true);

    const ipRange = document.getElementById("ipRange").value;
    const portsInput = document.getElementById("ports").value;
    const demoMode = document.getElementById("demoMode").checked;

    const ports = portsInput
        ? portsInput.split(",").map(p => parseInt(p.trim()))
        : [22, 80, 443];

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                ip_range: ipRange,
                ports: ports,
                demo: demoMode
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }

        const data = await response.json();
        currentScanId = data.scan_id;

        displayMessage(`Scan started with ID: ${currentScanId}. Polling for results...`, 'success');

        pollInterval = setInterval(fetchResults, 3000);
        
    } catch (error) {
        displayMessage(`Error starting scan: ${error.message}. Check server logs.`, 'error');
        setButtonState(false);
    }
}

async function fetchResults() {
    if (!currentScanId) return;

    try {
        const response = await fetch(`/results/${currentScanId}`);
        const data = await response.json();

        // Update status display with color-coded status
        let statusText = data.status || "pending";
        let statusClass = `status-${statusText.toLowerCase()}`;
        
        statusOutput.className = statusClass; // Add class for styling
        statusOutput.innerText = JSON.stringify({
            scan_id: data.scan_id,
            status: statusText,
            mode: data.mode,
            created_at: data.created_at
        }, null, 2);

        // Update results
        if (data.results && Array.isArray(data.results)) {
             resultsOutput.innerText = JSON.stringify(data.results, null, 2);
        } else {
             resultsOutput.innerText = JSON.stringify("Awaiting results...", null, 2);
        }

        // Check for completion
        if (statusText === "completed" || statusText === "failed") {
            clearInterval(pollInterval);
            pollInterval = null;
            setButtonState(false);

            if (statusText === "completed") {
                displayMessage(`Scan ${currentScanId} completed successfully.`, 'success');
            } else if (statusText === "failed") {
                displayMessage(`Scan ${currentScanId} failed. Check status output.`, 'error');
            }
        }
    } catch (error) {
        clearInterval(pollInterval);
        pollInterval = null;
        setButtonState(false);
        displayMessage(`Error fetching results: ${error.message}. Scan stopped.`, 'error');
        currentScanId = null;
    }
}