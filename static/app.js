let currentScanId = null;
let pollInterval = null;

async function startScan() {
    const ipRange = document.getElementById("ipRange").value;
    const portsInput = document.getElementById("ports").value;
    const demoMode = document.getElementById("demoMode").checked;

    const ports = portsInput
        ? portsInput.split(",").map(p => parseInt(p.trim()))
        : [22, 80, 443];

    const response = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            ip_range: ipRange,
            ports: ports,
            demo: demoMode
        })
    });

    const data = await response.json();
    currentScanId = data.scan_id;

    document.getElementById("scanMessage").innerText =
        `Scan started with ID: ${currentScanId}`;

    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(fetchResults, 3000);
}

async function fetchResults() {
    if (!currentScanId) return;

    const response = await fetch(`/results/${currentScanId}`);
    const data = await response.json();

    document.getElementById("statusOutput").innerText =
        JSON.stringify({
            scan_id: data.scan_id,
            status: data.status,
            mode: data.mode,
            created_at: data.created_at
        }, null, 2);

    document.getElementById("resultsOutput").innerText =
        JSON.stringify(data.results, null, 2);

    if (data.status === "completed" || data.status === "failed") {
        clearInterval(pollInterval);
    }
}
