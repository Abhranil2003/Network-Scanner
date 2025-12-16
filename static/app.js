// app.js — FINAL (Dashboard + Demo + Gateway + Cloud-safe)

let currentScanId = null;
let pollInterval = null;

const startButton = document.getElementById("startScanButton");
const statusOutput = document.getElementById("statusOutput");
const resultsOutput = document.getElementById("resultsOutput");
const scanMessageEl = document.getElementById("scanMessage");

// -------------------- Initial UI State --------------------

resultsOutput.innerText = "[]";
statusOutput.innerText = JSON.stringify(
    { status: "Awaiting scan start..." },
    null,
    2
);

// -------------------- UI Helpers --------------------

function setButtonState(isScanning) {
    startButton.disabled = isScanning;
    if (isScanning) {
        startButton.innerHTML = '<span class="spinner"></span> Scanning...';
    } else {
        startButton.innerText = "Start Scan";
    }
}

function displayMessage(message, type = "success") {
    scanMessageEl.innerText = message;
    scanMessageEl.style.display = "block";

    if (type === "error") {
        scanMessageEl.style.backgroundColor = "#f8d7da";
        scanMessageEl.style.color = "#721c24";
        scanMessageEl.style.border = "1px solid #f5c6cb";
    } else {
        scanMessageEl.style.backgroundColor = "#d4edda";
        scanMessageEl.style.color = "#155724";
        scanMessageEl.style.border = "1px solid #c3e6cb";
    }
}

// -------------------- Start Scan --------------------

async function startScan() {
    scanMessageEl.style.display = "none";
    resultsOutput.innerText = "[]";
    statusOutput.innerText = JSON.stringify(
        { status: "Starting scan..." },
        null,
        2
    );

    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }

    setButtonState(true);

    const ipRange = document.getElementById("ipRange").value.trim();
    const gateway = document.getElementById("gateway").value.trim();
    const portsInput = document.getElementById("ports").value;
    const demoMode = document.getElementById("demoMode").checked;

    // -------- Validation --------

    if (!ipRange) {
        displayMessage(
            "Please enter a valid IP range (e.g. 192.168.1.0/24).",
            "error"
        );
        setButtonState(false);
        return;
    }

    const ports = portsInput
        ? portsInput
            .split(",")
            .map(p => parseInt(p.trim()))
            .filter(p => Number.isInteger(p) && p > 0 && p <= 65535)
        : [22, 80, 443];

    if (ports.length === 0) {
        displayMessage(
            "No valid ports provided. Please enter ports between 1–65535.",
            "error"
        );
        setButtonState(false);
        return;
    }

    // -------- API Call --------

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ip_range: ipRange,
                gateway: gateway || null,
                ports: ports,
                demo: demoMode
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
        }

        const data = await response.json();
        currentScanId = data.scan_id;

        displayMessage(
            `Scan started successfully (ID: ${currentScanId}).`,
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

// -------------------- Poll Scan Results --------------------

async function fetchResults() {
    if (!currentScanId) return;

    try {
        const response = await fetch(`/results/${currentScanId}`);

        if (!response.ok) {
            throw new Error(
                `Failed to fetch results (status ${response.status})`
            );
        }

        const data = await response.json();

        const statusText = data.status || "pending";
        statusOutput.className = `status-${statusText.toLowerCase()}`;

        statusOutput.innerText = JSON.stringify(
            {
                scan_id: data.scan_id,
                status: statusText,
                mode: data.mode,
                created_at: data.created_at
            },
            null,
            2
        );

        if (Array.isArray(data.results)) {
            resultsOutput.innerText = JSON.stringify(
                data.results,
                null,
                2
            );
        } else {
            resultsOutput.innerText = JSON.stringify(
                "Awaiting results...",
                null,
                2
            );
        }

        if (statusText === "completed" || statusText === "failed") {
            clearInterval(pollInterval);
            pollInterval = null;
            setButtonState(false);

            if (statusText === "completed") {
                displayMessage(
                    `Scan ${currentScanId} completed successfully.`,
                    "success"
                );
            } else {
                displayMessage(
                    `Scan ${curr
