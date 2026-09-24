from urllib.parse import urlparse

import httpx

from backend.app.models.schemas import HttpRequest


class HttpEngine:

    def __init__(self):
        self.timeout = 10.0

    def _check_target(self, url: str):
        """
        第一版只允许访问本机靶场。
        """

        parsed = urlparse(url)

        allowed_hosts = {
            "127.0.0.1",
            "localhost",
            "::1"
        }

        if parsed.hostname not in allowed_hosts:
            raise ValueError(
                "当前 HTTP Engine 仅允许扫描本机靶场："
                "127.0.0.1 / localhost / ::1"
            )

    async def send(
        self,
        request: HttpRequest
    ) -> httpx.Response:

        self._check_target(request.url)

        headers = dict(request.headers)

        # 不手工发送 Content-Length，
        # 让 httpx 根据实际请求自动计算。
        headers.pop("Content-Length", None)

        async with httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True
        ) as client:

            response = await client.request(
                method=request.method.upper(),
                url=request.url,
                headers=headers,
                content=request.body
            )

        return response