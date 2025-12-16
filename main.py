from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.orm import Session

from utils import validate_ip_range, validate_port_list, validate_gateway
from database import SessionLocal
from models import Scan

from tasks import run_scan


app = FastAPI(
    title="Live Network Scanner",
    description="FastAPI-based live network scanning service",
    version="2.6.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ScanRequest(BaseModel):
    ip_range: str
    gateway: Optional[str] = None  
    ports: Optional[List[int]] = [22, 80, 443]
    demo: Optional[bool] = False


class ScanResponse(BaseModel):
    scan_id: int
    message: str


@app.post("/scan", response_model=ScanResponse)
def start_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if not validate_ip_range(request.ip_range):
        raise HTTPException(status_code=400, detail="Invalid IP range")

    if not validate_gateway(request.ip_range, request.gateway):
        raise HTTPException(
            status_code=400,
            detail="Gateway must belong to the given IP range"
        )

    if not validate_port_list(request.ports):
        raise HTTPException(status_code=400, detail="Invalid port list")

    scan = Scan(
        ip_range=request.ip_range,
        gateway=request.gateway,
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
        request.gateway,
        request.demo
    )

    return {
        "scan_id": scan.id,
        "message": "Scan started successfully"
    }
