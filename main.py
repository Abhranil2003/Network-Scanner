from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    BackgroundTasks,
    Request
)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.orm import Session

from utils import validate_ip_range, validate_port_list
from database import SessionLocal
from models import Scan
from tasks import run_scan

# -------------------- App --------------------

app = FastAPI(
    title="Live Network Scanner",
    description="FastAPI-based live network scanning service",
    version="2.5.0"
)

# -------------------- Frontend --------------------

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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
    ports: Optional[List[int]] = [22, 80, 443]
    demo: Optional[bool] = False

class ScanResponse(BaseModel):
    scan_id: int
    message: str

# -------------------- Frontend --------------------

@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# -------------------- API --------------------

@app.post("/scan", response_model=ScanResponse)
def start_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if not validate_ip_range(request.ip_range):
        raise HTTPException(status_code=400, detail="Invalid IP range format")

    if not validate_port_list(request.ports):
        raise HTTPException(status_code=400, detail="Invalid port list")

    scan = Scan(
        ip_range=request.ip_range,
        ports_scanned=",".join(map(str, request.ports)),
        status="pending",
        mode="demo" if request.demo else "cloud"
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    background_tasks.add_task(
        run_scan,
        scan.id,
        request.ip_range,
        request.ports,
        request.demo
    )

    return {
        "scan_id": scan.id,
        "message": "Scan started"
    }

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
        "status": scan.status,
        "mode": scan.mode,
        "ip_range": scan.ip_range,
        "ports_scanned": scan.ports_scanned,
        "created_at": scan.created_at,
        "results": results
    }
