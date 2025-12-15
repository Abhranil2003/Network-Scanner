from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    ip_range = Column(String, nullable=False)
    ports_scanned = Column(String, nullable=False)

    status = Column(String, default="pending", nullable=False)
    mode = Column(String, default="real", nullable=False)  # real | demo

    created_at = Column(DateTime, default=datetime.utcnow)

    hosts = relationship(
        "Host",
        back_populates="scan",
        cascade="all, delete"
    )


class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id", ondelete="CASCADE"))
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)

    scan = relationship("Scan", back_populates="hosts")
    open_ports = relationship(
        "OpenPort",
        back_populates="host",
        cascade="all, delete"
    )


class OpenPort(Base):
    __tablename__ = "open_ports"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("hosts.id", ondelete="CASCADE"))
    port = Column(Integer, nullable=False)

    host = relationship("Host", back_populates="open_ports")
