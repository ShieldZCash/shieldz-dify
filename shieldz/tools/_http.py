import json
import urllib.error
import urllib.request
from typing import Any

SWAP_BASE = "https://swap.shieldz.cash"
UA = "shieldz-dify/0.1.0"


def call(url: str, body: dict | None = None, timeout: float = 30.0) -> Any:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method="POST" if body is not None else "GET",
        headers={"Content-Type": "application/json", "User-Agent": UA, "x-shieldz-channel": "dify"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode())
        except Exception:
            payload = {}
        raise ValueError(_describe(payload) or f"Shieldz returned HTTP {e.code}") from None


def _describe(payload: Any) -> str:
    if isinstance(payload, dict) and isinstance(payload.get("error"), dict):
        return payload["error"].get("message", "")
    if isinstance(payload, list):
        parts = [f"{e.get('protocol', 'router')}: {e.get('detail') or e.get('kind')}" for e in payload[:5] if isinstance(e, dict)]
        return "; ".join(parts)
    return ""
