from typing import Dict, List
from urllib.parse import urlparse, parse_qs


class TrafficAnalyzer:

    def analyze(self, record: Dict) -> Dict:

        request = record.get("request", {})

        method = request.get("method", "").upper()
        url = request.get("url", "")
        path = request.get("path", "")

        reasons: List[str] = []

        priority = "LOW"

        # ==========================================
        # 1. HTTP 方法分析
        # ==========================================

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

        # ==========================================
        # 2. URL 参数分析
        # ==========================================

        parsed = urlparse(url)

        query_params = parse_qs(
            parsed.query
        )

        if query_params:

            reasons.append(
                "URL 包含用户可控查询参数"
            )

            priority = "HIGH"

        # ==========================================
        # 3. 认证相关
        # ==========================================

        auth_keywords = [
            "/login",
            "/signin",
            "/sign-in",
            "/auth",
            "/logout",
            "/register",
            "/password"
        ]

        path_lower = path.lower()

        if any(
            keyword in path_lower
            for keyword in auth_keywords
        ):

            reasons.append(
                "请求可能与认证或账户流程有关"
            )

            priority = "HIGH"

        # ==========================================
        # 4. 用户 / 权限相关
        # ==========================================

        account_keywords = [
            "/account",
            "/profile",
            "/user",
            "/users",
            "/admin",
            "/administrator"
        ]

        if any(
            keyword in path_lower
            for keyword in account_keywords
        ):

            reasons.append(
                "请求可能涉及用户或权限数据"
            )

            priority = "HIGH"

        # ==========================================
        # 5. API 请求
        # ==========================================

        if (
            "/api/" in path_lower
            or path_lower.startswith("/api")
        ):

            reasons.append(
                "检测到 API 请求"
            )

            if priority == "LOW":
                priority = "MEDIUM"

        # ==========================================
        # 6. 返回分析结果
        # ==========================================

        return {
            "request_id": record.get("id"),
            "priority": priority,
            "reasons": reasons
        }


traffic_analyzer = TrafficAnalyzer()