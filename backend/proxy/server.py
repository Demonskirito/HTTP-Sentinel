from pathlib import Path
import subprocess
import sys


def start_proxy():

    python_dir = Path(sys.executable).parent
    mitmdump = python_dir / "Scripts" / "mitmdump.exe"

    addon = (
        Path(__file__).resolve().parent / "addon.py"
    )

    command = [
        str(mitmdump),
        "-s",
        str(addon),
        "--listen-host",
        "127.0.0.1",
        "--listen-port",
        "8080",
    ]

    print("=" * 60)
    print("AI-WebSec-Assistant Proxy")
    print(f"Proxy : http://127.0.0.1:8080")
    print(f"Addon : {addon}")
    print("=" * 60)

    subprocess.run(command)


if __name__ == "__main__":
    start_proxy()