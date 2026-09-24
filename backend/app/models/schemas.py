from typing import Optional

from pydantic import BaseModel


class HttpRequest(BaseModel):
    method: str
    url: str
    headers: dict[str, str] = {}
    body: Optional[str] = None


class Finding(BaseModel):
    vulnerability_type: str
    severity: str
    confidence: float
    parameter: Optional[str] = None
    description: str
    evidence: Optional[str] = None
    recommendation: Optional[str] = None


class ScanResult(BaseModel):
    target: str
    method: str
    findings: list[Finding]