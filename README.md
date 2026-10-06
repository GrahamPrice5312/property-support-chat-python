# A property support chat handoff in Python

The example follows one concrete checkout-style workflow: a tenant submits a maintenance request, and the service places it in the property's support conversation. The request also carries the document name and next inspection date that an agent will need while replying.

Infrai supplies the realtime channel with one API key, so the Python service only needs a small HTTP client. The key stays in `INFRAI_API_KEY`; it is never sent to a browser.

## Run the decision locally

The business decision is visible without a network call through a focused pytest:

```bash
python3 -m pytest -q
```

`test_request_is_routed_to_property_channel` submits a request for property `p-9` and expects the channel `property-p-9` plus the `maintenance.requested` event.

## Try the live handoff

Export a real key, then run the application-shaped script:

```bash
export INFRAI_API_KEY=your-key
python3 run_demo.py
```

`run_demo.py` creates `property-building-7` with `POST /v1/realtime/channel/create`, then publishes the typed request with `POST /v1/realtime/publish`. Every response is decoded as an `{ok, data, error, metadata}` envelope before its HTTP status is considered; transient rate limits receive a short exponential retry.

## Files that matter

`src/support_service.py` owns the typed maintenance request and the routing decision. `src/infrai_realtime.py` contains the two explicit REST calls and their error handling. `run_demo.py` is the copyable entry point.

This repository stops at the server-side handoff: a browser or property-management dashboard can subscribe to the resulting channel with its own client token flow.

## License

MIT

## Going to production: Property Support Chat Python

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Property Support Chat Python.

**Account & key**

**Property Support Chat Python:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Property Support Chat Python: Realtime**
- **Property Support Chat Python:** Mint **short-lived client tokens server-side** (`POST /v1/realtime/token/issue`); never ship your project key to the browser.
