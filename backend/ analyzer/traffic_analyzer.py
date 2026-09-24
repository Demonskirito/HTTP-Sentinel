from typing import Dict, List
from urllib.parse import parse_qs, urlparse


class TrafficAnalyzer:

    def analyze(
        self,
        record: Dict
    ) -> Dict:

        request = record["request"]

        method = request["method"]
        url = request["url"]
        path = request["path"]

        reasons: List[str] = []

        priority = "LOW"

        # 1. POST / PUT / DELETE
        if method in {
            "POST",
            "PUT",
            "PATCH",
            "DELETE"
        }:

            reasons.append(
                "请求可能改变服务器状态"
            )

            priority = "MEDIUM"

        # 2. URL 参数
        parsed = urlparse(url)

        query_params = parse_qs(
            parsed.query
        )

        if query_params:

            reasons.append(
                "URL 包含用户可控查询参数"
            )

            priority = "HIGH"

        # 3. 常见认证路径
        auth_keywords = [
            "/login",
            "/signin",
            "/auth",
            "/logout"
        ]

        if any(
            keyword in path.lower()
            for keyword in auth_keywords
        ):

            reasons.append(
                "请求可能与认证流程有关"
            )

            priority = "HIGH"

        # 4. 用户账户
        account_keywords = [
            "/account",
            "/profile",
            "/user",
            "/admin"
        ]

        if any(
            keyword in path.lower()
            for keyword in account_keywords
        ):

            reasons.append(
                "请求可能涉及用户或权限数据"
            )

            priority = "HIGH"

        return {
            "priority": priority,
            "reasons": reasons
        }


traffic_analyzer = TrafficAnalyzer()