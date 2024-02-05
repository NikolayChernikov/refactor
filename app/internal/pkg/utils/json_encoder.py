import json
from datetime import datetime
from decimal import Decimal
from typing import Any


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, datetime):
            return o.timestamp()
        return super(CustomJSONEncoder, self).default(o)
