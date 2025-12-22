from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    BackgroundTasks,
    Request
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session

from utils import (
    validate_ip_range,
    validate_port_list,
    validate_gateway
)
from database import SessionLocal
from models import Scan
from tasks import run_scan

# -------------------- App --------------------

app = FastAPI(
    title="Live Network Scanner",
    description="FastAPI-based live network scanning service",
    version="2.7.0"
)

# -------------------- Static & Templates --------------------

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
    ip_range: str = Field(..., example="192.168.1.0/24")
    gateway: Optional[str] = Field(None, example="192.168.1.1")
    ports: Optional[List[int]] = Field(default_factory=lambda: [22, 80, 443])
    demo: Optional[bool] = False


class ScanResponse(BaseModel):
    scan_id: int
    status: str
    message: str

# -------------------- Frontend --------------------

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -------------------- API --------------------

@app.post("/scan", response_model=ScanResponse)
def start_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if not validate_ip_range(request.ip_range):
        raise HTTPException(400, "Invalid IP range")

    if request.gateway:
        if not validate_gateway(request.ip_range, request.gateway):
            raise HTTPException(400, "Gateway must belong to the IP range")

    if not validate_port_list(request.ports):
        raise HTTPException(400, "Invalid port list")

    scan = Scan(
        ip_range=request.ip_range,
        gateway=request.gateway,
        ports_scanned=",".join(map(str, request.ports)),
        status="created",
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
        "status": scan.status,
        "message": "Scan queued successfully"
    }
