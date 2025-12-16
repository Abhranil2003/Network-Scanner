let currentScanId = null;
let pollInterval = null;

const startButton = document.getElementById("startScanButton");
const statusOutput = document.getElementById("statusOutput");
const resultsOutput = document.getElementById("resultsOutput");
const scanMessageEl = document.getElementById("scanMessage");

// Initial state
resultsOutput.innerText = "[]";
statusOutput.innerText = JSON.stringify(
    { status: "Awaiting scan start..." },
    null,
    2
);

// -------------------- UI Helpers --------------------

function setButtonState(isScanning) {
    startButton.disabled = isScanning;
    startButton.innerHTML = isScanning
        ? '<span class="spinner"></span> Scanning...'
        : "Start Scan";
}

function displayMessage(message, type = "success") {
    scanMessageEl.innerText = message;
    scanMessageEl.style.display = "block";

    scanMessageEl.style.backgroundColor =
        type === "error" ? "#f8d7da" : "#d4edda";
    scanMessageEl.style.color =
        type === "error" ? "#721c24" : "#155724";
    scanMessageEl.style.border =
        type === "error"
            ? "1px solid #f5c6cb"
            : "1px solid #c3e6cb";
}

function getStatusMessage(status) {
    switch (status) {
        case "pending":
            return "Scan queued… preparing to start";
        case "running":
            return "Scanning network… please wait";
        case "completed":
            return "Scan completed successfully";
        case "failed":
            return "Scan failed. Check logs or try again.";
        default:
            return "Unknown scan state";
    }
}

// -------------------- Scan Start --------------------

async function startScan() {
    scanMessageEl.style.display = "none";
    resultsOutput.innerText = "[]";
    statusOutput.innerText = JSON.stringify(
        { status: "Starting scan..." },
        null,
        2
    );

    if (pollInterval) clearInterval(pollInterval);
    setButtonState(true);

    const ipRange = document.getElementById("ipRange").value.trim();
    if (!ipRange) {
        displayMessage(
            "Please enter a valid IP range (e.g. 192.168.1.0/24).",
            "error"
        );
        setButtonState(false);
        return;
    }

    const portsInput = document.getElementById("ports").value;
    const demoMode = document.getElementById("demoMode").checked;

    const ports = portsInput
        ? portsInput
              .split(",")
              .map(p => parseInt(p.trim()))
              .filter(p => Number.isInteger(p) && p > 0 && p <= 65535)
        : [22, 80, 443];

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ip_range: ipRange,
                ports: ports,
                demo: demoMode
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();
        currentScanId = data.scan_id;

        displayMessage(
            `Scan #${currentScanId} started. Polling for results…`,
            "success"
        );

        pollInterval = setInterval(fetchResults, 3000);

    } catch (error) {
        displayMessage(
            `Error starting scan: ${error.message}`,
            "error"
        );
        setButtonState(false);
    }
}

// -------------------- Results Polling --------------------

async function fetchResults() {
    if (!currentScanId) return;

    try {
        const response = await fetch(`/results/${currentScanId}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch results (${response.status})`);
        }

        const data = await response.json();
        const statusText = data.status || "pending";

        statusOutput.className = `status-${statusText}`;
        statusOutput.innerText = JSON.stringify(
            {
                scan_id: data.scan_id,
                status: getStatusMessage(statusText),
                mode: data.mode,
                created_at: data.created_at
            },
            null,
            2
        );

        // ---- Results UX ----
        if (Array.isArray(data.results)) {
            if (data.results.length === 0 && data.mode === "cloud") {
                resultsOutput.innerText = JSON.stringify(
                    "Cloud mode active: live ARP scanning is restricted. Enable Demo Mode to view sample results.",
                    null,
                    2
                );
            } else {
                resultsOutput.innerText = JSON.stringify(
                    data.results,
                    null,
                    2
                );
            }
        } else {
            resultsOutput.innerText = JSON.stringify(
                "Awaiting results...",
                null,
                2
            );
        }

        // ---- Completion ----
        if (statusText === "completed" || statusText === "failed") {
            clearInterval(pollInterval);
            pollInterval = null;
            setButtonState(false);

            displayMessage(
                statusText === "completed"
                    ? `Scan #${currentScanId} completed. Results ready below.`
                    : `Scan #${currentScanId} failed.`,
                statusText === "completed" ? "success" : "error"
            );
        }

    } catch (error) {
        clearInterval(pollInterval);
        pollInterval = null;
        setButtonState(false);
        currentScanId = null;

        displayMessage(
            `Error fetching results: ${error.message}`,
            "error"
        );
    }
}