from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._http import SWAP_BASE, call


class ListSwapAssetsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        q = str(tool_parameters.get("query") or "").strip().lower()
        chain = str(tool_parameters.get("chain") or "").strip().lower()
        assets = call(f"{SWAP_BASE}/v1/assets")["assets"]
        hits = [
            a for a in assets
            if (not q or q in a["symbol"].lower() or q in a["asset_id"].lower())
            and (not chain or a["chain"].lower() == chain)
        ]
        hits.sort(key=lambda a: (not a.get("verified"), a["chain"], a["symbol"]))
        yield self.create_json_message({
            "count": len(hits),
            "assets": [
                {"asset_id": a["asset_id"], "symbol": a["symbol"], "chain": a["chain"],
                 "usd_price": a.get("usd_price"), "verified": bool(a.get("verified"))}
                for a in hits[:50]
            ],
        })
