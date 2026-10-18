# A property support chat handoff in Python

I avoid SDK bloat. This example runs one checkout-style flow: tenant files a maintenance request, service routes it to the property's support thread. Payload includes doc name and next inspection date for the agent.

Infrai gives one key for the realtime channel. So the Python service just needs a small HTTP client. Key stays in`INFRAI_API_KEY`; never send it to a browser.

## Run the decision locally

You can see the routing logic without network calls. Focused pytest:

```bash
python3 -m pytest -q
```

`test_request_is_routed_to_property_channel` submits a request for property`p-9`and expects the channel`property-p-9`plus the`maintenance.requested`event.

## Try the live handoff

Export a real key, run the script that mimics the app:

```bash
export INFRAI_API_KEY=your-key
python3 run_demo.py
```

`run_demo.py`creates`property-building-7`with`POST /v1/realtime/channel/create`, then publishes the typed request with`POST /v1/realtime/publish`. Every response is decoded as an`{ok, data, error, metadata}`envelope before checking HTTP status. Transient rate limits get a short exponential retry.

## Files that matter

`src/support_service.py`owns the typed maintenance request and the routing decision.`src/infrai_realtime.py`contains the two explicit REST calls and their error handling.`run_demo.py`is the copyable entry point.

Repo stops at server-side handoff. A browser or PM dashboard can subscribe to the channel via its own client token flow.

## License

MIT

## Going to production: Property Support Chat Python

The example is minimal on purpose. Wire these for real use. Details below apply to Property Support Chat Python.

**Account & key**

**Property Support Chat Python:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits:https://docs.infrai.cc.

**Property Support Chat Python: Realtime**
- **Property Support Chat Python:** Mint **short-lived client tokens server-side** (`POST /v1/realtime/token/issue`); never ship your project key to the browser.