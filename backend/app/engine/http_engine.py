import requests
from typing import Dict, Optional


class HTTPResponse:

    def __init__(
        self,
        status_code: int,
        headers: Dict,
        body: str,
        url: str
    ):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.url = url


class HTTPEngine:

    def __init__(
        self,
        timeout: int = 10
    ):
        self.timeout = timeout

    def send(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        body: Optional[str] = None,
        params: Optional[Dict] = None
    ) -> HTTPResponse:

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=body,
            params=params,
            timeout=self.timeout
        )

        return HTTPResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response.text,
            url=response.url
        )


http_engine = HTTPEngine()