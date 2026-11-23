from typing import Any

from dify_plugin import ToolProvider


class ShieldzProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # Every tool here is keyless; there is nothing to validate.
        return None
