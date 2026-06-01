"""Hash-chained trace output for EMEX runs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .hashing import hash_json


@dataclass
class Trace:
    session_id: str
    events: list[dict[str, Any]] = field(default_factory=list)

    def add(self, event_type: str, data: dict[str, Any]) -> None:
        prev_hash = self.events[-1]["event_hash"] if self.events else "0" * 64
        event = {
            "event_id": f"trace-{len(self.events) + 1:04d}",
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
            "prev_hash": prev_hash,
        }
        event["event_hash"] = hash_json(event)
        self.events.append(event)

    def render(self) -> dict[str, Any]:
        return {
            "schema_version": "emex.trace.v0.1",
            "session_id": self.session_id,
            "event_count": len(self.events),
            "events": self.events,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Trace":
        trace = cls(session_id=data.get("session_id", "unknown"))
        trace.events = list(data.get("events", []))
        return trace

    def verify(self) -> tuple[bool, str]:
        prev_hash = "0" * 64
        for idx, event in enumerate(self.events):
            if event.get("prev_hash") != prev_hash:
                return False, f"event {idx} prev_hash mismatch"
            event_copy = {k: v for k, v in event.items() if k != "event_hash"}
            if hash_json(event_copy) != event.get("event_hash"):
                return False, f"event {idx} event_hash mismatch"
            prev_hash = event["event_hash"]
        return True, "trace verified"

    def to_json(self) -> str:
        return json.dumps(self.render(), indent=2)
