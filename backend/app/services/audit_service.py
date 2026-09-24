from backend.app.Scanner.xss import xss_scanner


class AuditService:

    def audit(self, record):

        findings = []

        request = record.get(
            "request",
            {}
        )

        url = request.get(
            "url",
            ""
        )

        if "?" in url:

            findings.extend(
                xss_scanner.scan(record)
            )

        return findings


audit_service = AuditService()