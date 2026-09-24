import uuid
from urllib.parse import (
    urlparse,
    parse_qsl,
    urlencode,
    urlunparse
)

from backend.app.engine.http_engine import http_engine
from backend.app.models.finding import (
    Finding,
    Evidence
)


class XSSScanner:

    name = "XSSScanner"

    def scan(self, record):

        request = record["request"]

        url = request["url"]

        parsed = urlparse(url)

        params = parse_qsl(
            parsed.query,
            keep_blank_values=True
        )

        findings = []

        for index, (name, value) in enumerate(params):

            marker = (
                "AIWSX_"
                + uuid.uuid4().hex[:8]
            )

            new_params = params.copy()

            new_params[index] = (
                name,
                marker
            )

            new_query = urlencode(
                new_params
            )

            test_url = urlunparse(
                (
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    new_query,
                    parsed.fragment
                )
            )

            try:

                response = http_engine.send(
                    method=request["method"],
                    url=test_url,
                    headers=request.get(
                        "headers",
                        {}
                    )
                )

            except Exception as e:

                print(
                    f"[XSSScanner] "
                    f"request failed: {e}"
                )

                continue

            if marker in response.body:

                evidence = Evidence(
                    type="reflection",
                    description=(
                        "测试标记被服务器响应反射"
                    ),
                    data={
                        "parameter": name,
                        "marker": marker,
                        "test_url": test_url,
                        "status_code": (
                            response.status_code
                        )
                    }
                )

                finding = Finding(
                    scanner=self.name,
                    vulnerability=(
                        "Potential Reflected XSS"
                    ),
                    severity="MEDIUM",
                    confidence=0.75,
                    url=url,
                    parameter=name,
                    evidence=[evidence],
                    description=(
                        "用户可控参数被反射到 HTTP 响应中，"
                        "需要进一步分析输出上下文以确认 "
                        "是否可以形成可执行的 XSS。"
                    ),
                    remediation=(
                        "对用户输入进行上下文相关的输出编码，"
                        "并避免将未可信输入直接插入 HTML。"
                    )
                )

                findings.append(
                    finding
                )

        return findings


xss_scanner = XSSScanner()