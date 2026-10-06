from dataclasses import dataclass, asdict
from typing import Any

from infrai_realtime import InfraiRealtime


@dataclass(frozen=True)
class MaintenanceRequest:
    tenant_id: str
    property_id: str
    summary: str
    document_name: str | None = None
    inspection_due: str | None = None


def submit_request(request: MaintenanceRequest, realtime: InfraiRealtime) -> dict[str, Any]:
    """Create the property's support channel and publish the tenant's request."""
    channel = f"property-{request.property_id}"
    realtime.create_channel(channel)
    event = realtime.publish(channel, "maintenance.requested", asdict(request), request.tenant_id)
    return {"channel": channel, "event": event, "status": "queued-for-support"}

