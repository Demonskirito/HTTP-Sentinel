from fastapi import APIRouter, HTTPException

from backend.app.services.history_service import history_service

router = APIRouter(
    prefix="/api/history",
    tags=["HTTP History"]
)


@router.get("")
def get_history(limit: int = 100):
    limit = max(1, min(limit, 1000))

    records = history_service.get_latest(limit)

    # 前端列表使用的轻量数据
    data = []

    for record in records:
        request = record.get("request", {})
        response = record.get("response") or {}

        data.append({
            "id": record.get("id"),
            "timestamp": record.get("timestamp"),

            "method": request.get("method"),
            "url": request.get("url"),
            "host": request.get("host"),
            "path": request.get("path"),

            "status_code": response.get("status_code"),
            "content_type": response.get("content_type", ""),

            "request_size": len(
                request.get("body", "") or ""
            ),

            "response_size": len(
                response.get("body", "") or ""
            )
        })

    return {
        "success": True,
        "count": len(data),
        "data": data
    }


@router.get("/{request_id}")
def get_history_detail(request_id: str):

    records = history_service.get_all()

    for record in records:
        if record.get("id") == request_id:
            return {
                "success": True,
                "data": record
            }

    raise HTTPException(
        status_code=404,
        detail="Request not found"
    )