"""Wait until the DAMFOX backend status endpoint is ready."""

import argparse
import json
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()
    deadline = time.monotonic() + args.timeout
    while time.monotonic() < deadline:
        try:
            with urlopen(args.url, timeout=min(args.interval, 2.0)) as response:
                payload = json.load(response)
                if response.status == 200 and payload.get("status") == "online":
                    return 0
        except (OSError, URLError, ValueError):
            pass
        time.sleep(args.interval)
    print(f"Backend readiness timed out after {args.timeout:g}s", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
