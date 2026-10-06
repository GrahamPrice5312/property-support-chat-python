import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from support_service import MaintenanceRequest, submit_request


class FakeRealtime:
    def __init__(self):
        self.calls = []

    def create_channel(self, channel):
        self.calls.append(("create", channel))
        return {"channel": channel}

    def publish(self, channel, event, data, account_id):
        self.calls.append(("publish", channel, event, data, account_id))
        return {"accepted": True}


def test_request_is_routed_to_property_channel():
    fake = FakeRealtime()
    result = submit_request(MaintenanceRequest("t-1", "p-9", "Boiler check"), fake)
    assert result["channel"] == "property-p-9"
    assert fake.calls[1][2] == "maintenance.requested"
    assert fake.calls[1][3]["summary"] == "Boiler check"

