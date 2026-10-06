import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from infrai_realtime import InfraiRealtime
from support_service import MaintenanceRequest, submit_request


def main() -> None:
    request = MaintenanceRequest(
        tenant_id="tenant-104",
        property_id="building-7",
        summary="Kitchen tap is leaking",
        document_name="lease-104.pdf",
        inspection_due="2026-10-15",
    )
    print(json.dumps(submit_request(request, InfraiRealtime()), indent=2))


if __name__ == "__main__":
    main()
