from fastapi import APIRouter

from backend.app.models.schemas import HttpRequest, ScanResult
from backend.app.Scanner.xss import XSSScanner


router = APIRouter(
    prefix="/api/scan",
    tags=["Security Scan"]
)


@router.post("/xss", response_model=ScanResult)
async def scan_xss(request: HttpRequest):

    scanner = XSSScanner()

    findings = await scanner.scan(request)

    return ScanResult(
        target=request.url,
        method=request.method,
        findings=findings
    )