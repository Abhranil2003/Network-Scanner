let currentScanId = null;
let pollInterval = null;

const startButton = document.getElementById("startScanButton");
const statusOutput = document.getElementById("statusOutput");
const resultsOutput = document.getElementById("resultsOutput");
const scanMessageEl = document.getElementById("scanMessage");

function displayMessage(message, type = "success") {
    scanMessageEl.innerText = message;
    scanMessageEl.style.display = "block";
    scanMessageEl.className = type;
}

function setButtonState(scanning) {
    startButton.disabled = scanning;
    startButton.innerText = scanning ? "Scanning..." : "Start Scan";
}

async function startScan() {
    scanMessageEl.style.display = "none";
    resultsOutput.innerText = "";
    statusOutput.innerText = "";

    setButtonState(true);

    const ipRange = document.getElementById("ipRange").value.trim();
    const gateway = document.getElementById("gateway").value.trim();
    const portsInput = document.getElementById("ports").value;
    const demoMode = document.getElementById("demoMode").checked;

    if (!ipRange) {
        displayMessage("IP range is required", "error");
        setButtonState(false);
        return;
    }

    const ports = portsInput
        .split(",")
        .map(p => parseInt(p.trim()))
        .filter(p => Number.isInteger(p) && p > 0 && p <= 65535);

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                ip_range: ipRange,
                gateway: gateway || null,
                ports: ports.length ? ports : [22, 80, 443],
                demo: demoMode
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Failed to start scan");
        }

        const data = await response.json();
        currentScanId = data.scan_id;

        displayMessage(`Scan started (ID ${currentScanId})`);
        pollInterval = setInterval(fetchResults, 3000);

    } catch (err) {
        displayMessage(err.message, "error");
        setButtonState(false);
    }
}

async function fetchResults() {
    if (!currentScanId) return;

    try {
        const response = await fetch(`/results/${currentScanId}`);
        if (!response.ok) throw new Error("Failed to fetch results");

        const data = await response.json();

        statusOutput.innerText = JSON.stringify({
            status: data.status,
            mode: data.mode,
            gateway: data.gateway,
            created_at: data.created_at
        }, null, 2);

        resultsOutput.innerText = JSON.stringify(data.results || [], null, 2);

        if (data.status === "completed" || data.status === "failed") {
            clearInterval(pollInterval);
            setButtonState(false);
        }

    } catch (err) {
        clearInterval(pollInterval);
        setButtonState(false);
        displayMessage(err.message, "error");
    }
}
