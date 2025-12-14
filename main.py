from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.orm import Session

from network_scanner import scan_network
from port_scanner import scan_ports
from utils import validate_ip_range, validate_port_list
from config import DEFAULT_PORTS

from database import SessionLocal
from models import Scan, Host, OpenPort

# -------------------- App --------------------

app = FastAPI(
    title="Live Network Scanner",
    description="FastAPI-based live network scanning service",
    version="2.0.0"
)

# -------------------- DB Dependency --------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- Schemas --------------------

class ScanRequest(BaseModel):
    ip_range: str
    ports: Optional[List[int]] = DEFAULT_PORTS

class ScanResponse(BaseModel):
    scan_id: int
    message: str

# -------------------- API --------------------

@app.post("/scan", response_model=ScanResponse)
def start_scan(request: ScanRequest, db: Session = Depends(get_db)):

    # Validate input
    if not validate_ip_range(request.ip_range):
        raise HTTPException(status_code=400, detail="Invalid IP range format")

    if not validate_port_list(request.ports):
        raise HTTPException(status_code=400, detail="Invalid port list")

    # 1️⃣ Create scan entry
    scan = Scan(
        ip_range=request.ip_range,
        ports_scanned=",".join(map(str, request.ports))
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    # 2️⃣ Network scan
    active_hosts = scan_network(request.ip_range)

    # 3️⃣ Save hosts & ports
    for host in active_hosts:
        host_obj = Host(
            scan_id=scan.id,
            ip_address=host["ip"],
            mac_address=host["mac"]
        )
        db.add(host_obj)
        db.commit()
        db.refresh(host_obj)

        open_ports = scan_ports(host["ip"], request.ports)
        for port in open_ports:
            db.add(OpenPort(
                host_id=host_obj.id,
                port=port
            ))

    db.commit()

    return {
        "scan_id": scan.id,
        "message": "Scan completed and saved successfully"
    }

# -------------------- RESULTS APIs --------------------

@app.get("/results/{scan_id}")
def get_scan_results(scan_id: int, db: Session = Depends(get_db)):

    scan = db.query(Scan).filter(Scan.id == scan_id).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    results = []
    for host in scan.hosts:
        results.append({
            "ip": host.ip_address,
            "mac": host.mac_address,
            "open_ports": [p.port for p in host.open_ports]
        })

    return {
        "scan_id": scan.id,
        "ip_range": scan.ip_range,
        "ports_scanned": scan.ports_scanned,
        "created_at": scan.created_at,
        "results": results
    }

@app.get("/results")
def list_scans(db: Session = Depends(get_db)):
    scans = db.query(Scan).all()

    return [
        {
            "scan_id": scan.id,
            "ip_range": scan.ip_range,
            "ports_scanned": scan.ports_scanned,
            "created_at": scan.created_at
        }
        for scan in scans
    ]
