import json
import time
import uuid
from pathlib import Path

from mitmproxy import http


class AIWebSecProxy:

    def __init__(self):

        self.history_file = Path(
            "/app/data/http_history.jsonl"
        )

        self.history_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        print("=" * 60)
        print("AI-WebSec-Assistant Proxy")
        print(f"History file: {self.history_file}")
        print("=" * 60)

    def request(self, flow: http.HTTPFlow):

        request = flow.request

        record = {
            "id": str(uuid.uuid4()),

            "timestamp": time.time(),

            "request": {
                "method": request.method,
                "scheme": request.scheme,
                "host": request.host,
                "port": request.port,
                "path": request.path,
                "url": request.pretty_url,

                "headers": dict(request.headers),

                "body": request.get_text(
                    strict=False
                )
            },

            "response": None
        }

        flow.metadata["audit_record"] = record

        print(
            f"[REQUEST] "
            f"{request.method} "
            f"{request.pretty_url}"
        )

    def response(self, flow: http.HTTPFlow):

        request = flow.request
        response = flow.response

        record = flow.metadata.get(
            "audit_record"
        )

        if record is None:
            print("[WARN] No audit record found")
            return

        record["response"] = {

            "status_code": response.status_code,

            "headers": dict(response.headers),

            "content_type": response.headers.get(
                "content-type",
                ""
            ),

            "body": response.get_text(
                strict=False
            )
        }

        try:

            with open(
                self.history_file,
                "a",
                encoding="utf-8"
            ) as f:

                f.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    ) + "\n"
                )

                f.flush()

            print(
                f"[HISTORY SAVED] "
                f"id={record['id']} "
                f"file={self.history_file}"
            )

        except Exception as e:

            print(
                f"[HISTORY SAVE ERROR] "
                f"{type(e).__name__}: {e}"
            )

        print(
            f"[RESPONSE] "
            f"{request.method} "
            f"{request.path} "
            f"-> "
            f"{response.status_code}"
        )


addons = [
    AIWebSecProxy()
]