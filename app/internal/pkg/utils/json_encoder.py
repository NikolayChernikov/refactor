"""Json ecnoder module."""
import json
from datetime import datetime
from decimal import Decimal
from typing import Any


class CustomJSONEncoder(json.JSONEncoder):
    """Custom json encoder class."""

    def default(self, o: Any) -> Any:
        """Default json ecnoder

        Args:
            o: ...

        Returns: Any
        """
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, datetime):
            return o.timestamp()
        return super(CustomJSONEncoder, self).default(o)  # pylint: disable=super-with-arguments
