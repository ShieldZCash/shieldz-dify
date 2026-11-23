from collections.abc import Generator
from decimal import Decimal, InvalidOperation
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._http import SWAP_BASE, call


def _resolve(assets: list[dict], q: str) -> dict:
    q = q.strip()
    for a in assets:
        if a["asset_id"].lower() == q.lower():
            return a
    chain, _, symbol = q.partition(".")
    hits = [a for a in assets if a["chain"].lower() == chain.lower() and a["symbol"].lower() == symbol.lower()]
    verified = [a for a in hits if a.get("verified")]
    if len(hits) == 1:
        return hits[0]
    if len(verified) == 1:
        return verified[0]
    if hits:
        raise ValueError(f"'{q}' is ambiguous, use one of: " + ", ".join(a["asset_id"] for a in hits[:10]))
    raise ValueError(f"Unknown asset '{q}'. Use CHAIN.SYMBOL, e.g. BTC.BTC, ETH.ETH, SOL.SOL, BASE.USDC, ZEC.ZEC.")


def _to_base(amount: str, decimals: int) -> str:
    try:
        v = Decimal(amount.strip())
    except InvalidOperation:
        raise ValueError("amount must be a plain decimal number like 0.05 or 100") from None
    if v <= 0:
        raise ValueError("amount must be greater than zero")
    return str(int(v.scaleb(decimals)))


def _from_base(value: Any, decimals: int) -> str | None:
    if value is None or not str(value).isdigit():
        return None
    return format(Decimal(int(value)).scaleb(-decimals).normalize(), "f")


class GetSwapQuoteTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        assets = call(f"{SWAP_BASE}/v1/assets")["assets"]
        src = _resolve(assets, tool_parameters["from_asset"])
        dst = _resolve(assets, tool_parameters["to_asset"])
        amount_in = _to_base(str(tool_parameters["amount"]), src["decimals"])
        q = call(f"{SWAP_BASE}/v1/quote", {
            "origin_asset": src["asset_id"],
            "destination_asset": dst["asset_id"],
            "amount_in": amount_in,
        })

        def view(r: dict) -> dict:
            try:
                cost = round((1 - float(r["amount_out_usd"]) / float(r["amount_in_usd"])) * 100, 3)
            except (KeyError, TypeError, ValueError, ZeroDivisionError):
                cost = None
            return {
                "protocol": r.get("protocol"),
                "amount_out": _from_base(r.get("amount_out"), dst["decimals"]),
                "total_cost_pct": cost,
                "estimated_seconds": r.get("estimated_duration_seconds"),
            }

        result = {
            "from": src["asset_id"],
            "to": dst["asset_id"],
            "amount_in": str(tool_parameters["amount"]),
            "best": view(q["best"]),
            "alternatives": [view(r) for r in q.get("alternatives", [])[:5]],
            "swap_url": f"{SWAP_BASE}/?utm_source=dify",
            "note": "Informational quote; it includes the flat 0.15% Shieldz Swap fee and changes with the market.",
        }
        yield self.create_json_message(result)
        b = result["best"]
        yield self.create_text_message(
            f"Best route for {result['amount_in']} {src['symbol']} -> {dst['symbol']}: "
            f"{b['amount_out']} {dst['symbol']} via {b['protocol']}"
            + (f", all-in cost {b['total_cost_pct']}%" if b["total_cost_pct"] is not None else "")
            + f". Swap: {result['swap_url']}"
        )
