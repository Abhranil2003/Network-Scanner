from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from network_scanner import scan_network
from port_scanner import scan_ports
from utils import validate_ip_range, validate_port_list
from config import DEFAULT_PORTS

import csv

app = FastAPI(
    title="Live Network Scanner",
    description="FastAPI-based live network scanning service",
    version="1.0.0"
)

# -------------------- Schemas --------------------

class ScanRequest(BaseModel):
    ip_range: str
    ports: Optional[List[int]] = DEFAULT_PORTS
    save_format: Optional[str] = None  # "txt" or "csv"
    output_filename: Optional[str] = "scan_results"

class HostResult(BaseModel):
    ip: str
    mac: str
    open_ports: List[int]

class ScanResponse(BaseModel):
    results: List[HostResult]

# -------------------- Helper --------------------

def save_results_to_file(results, file_format, filename):
    file_path = f"{filename}.{file_format}"

    if file_format == "txt":
        with open(file_path, "w") as file:
            file.write("IP Address\tMAC Address\tOpen Ports\n")
            for r in results:
                file.write(f"{r['ip']}\t{r['mac']}\t{','.join(map(str, r['open_ports']))}\n")

    elif file_format == "csv":
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["IP Address", "MAC Address", "Open Ports"])
            for r in results:
                writer.writerow([r["ip"], r["mac"], ",".join(map(str, r["open_ports"]))])

# -------------------- API --------------------

@app.post("/scan", response_model=ScanResponse)
def start_scan(request: ScanRequest):

    # Validate IP range
    if not validate_ip_range(request.ip_range):
        raise HTTPException(status_code=400, detail="Invalid IP range format")

    # Validate ports
    if not validate_port_list(request.ports):
        raise HTTPException(status_code=400, detail="Invalid port list")

    # Step 1: Network scan
    active_hosts = scan_network(request.ip_range)
    if not active_hosts:
        return {"results": []}

    # Step 2: Port scan
    results = []
    for host in active_hosts:
        open_ports = scan_ports(host["ip"], request.ports)
        results.append({
            "ip": host["ip"],
            "mac": host["mac"],
            "open_ports": open_ports
        })

    # Step 3: Optional file save
    if request.save_format in ["txt", "csv"]:
        save_results_to_file(results, request.save_format, request.output_filename)

    return {"results": results}
