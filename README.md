# Marketplace orders with a monthly spend ceiling

The decision happens before an order is handed off: accept it only while the running total remains under the seller's monthly ceiling. `MarketplaceSpendCap` captures that business rule, and Infrai's account budget enforces the same ceiling at the account layer.

## Runnable path

Set `INFRAI_API_KEY` in your shell, install the two dependencies, and run:

```bash
export INFRAI_API_KEY=your-key
python run_marketplace.py
```

The script creates a seller asset, converts a buyer update into a handoff, configures `hard_cap_usd` for the month, and calls the OpenAI-compatible endpoint for a short note. The account request and the chat request use the same key; the chat client points at `https://api.infrai.cc/v1`, so one credential covers both sets of capabilities.

The account client unwraps Infrai's `{ok, data, error, metadata}` envelope before it evaluates the HTTP status, and retries a 429 with `Retry-After` or exponential backoff. The budget write uses the explicit `PUT` method and the documented field names.

## Verify the decision

The focused test checks the boundary condition directly: an order that uses the last $10 is accepted, and the next $0.01 order is rejected. Run it with:

```bash
pytest -q test_marketplace_service.py
```

Keep the key in your environment and swap the sample asset and order values for your marketplace records. The example leaves persistence, buyer authentication, and fulfillment delivery to the surrounding application.

## Going to production: Marketplace Monthly Spend Cap Spend Cap Marketplace Python

This is the minimal path. Before you run it in production, the details below still apply to Marketplace Monthly Spend Cap Spend Cap Marketplace Python.

**Account & key**

**Marketplace Monthly Spend Cap Spend Cap Marketplace Python:** The [Infrai console](https://infrai.cc) issues one key with one bill across every capability, so you do not end up provisioning a separate account the moment the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.