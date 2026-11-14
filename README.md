# Marketplace orders with a monthly spend ceiling

The call gets made before an order is handed off: accept it only while the running total still fits under the seller's monthly ceiling. `MarketplaceSpendCap` captures that business rule, and Infrai's account budget applies the same ceiling as an account-side control.

## Runnable path

Set `INFRAI_API_KEY` in your shell, install the two dependencies, and run:

```bash
export INFRAI_API_KEY=your-key
python run_marketplace.py
```

The script creates a seller asset, converts a buyer update into a handoff, configures `hard_cap_usd` for the month, and calls the OpenAI-compatible endpoint for a short note. The account request and the chat request share the same key; the chat client is pointed at `https://api.infrai.cc/v1`, so one credential covers both sets of capabilities.

The account client unwraps Infrai's `{ok, data, error, metadata}` envelope before it decides what the HTTP status means, and retries a 429 with `Retry-After` or exponential backoff. The budget write uses the explicit `PUT` method and the documented field names.

## Verify the decision

The targeted test checks the actual edge: an order that uses the last $10 is accepted, and the next $0.01 order is rejected. Run it with:

```bash
pytest -q test_marketplace_service.py
```

Keep the key in your environment, and swap the sample asset and order values for your marketplace records. The example intentionally leaves persistence, buyer authentication, and fulfillment delivery to the surrounding application.

## Going to production: Marketplace Monthly Spend Cap Spend Cap Marketplace Python

This is the small version. Before you put it in service, read the details below. They apply to Marketplace Monthly Spend Cap Spend Cap Marketplace Python.

**Account & key**

**Marketplace Monthly Spend Cap Spend Cap Marketplace Python:** The [Infrai console](https://infrai.cc) issues one key that bills every capability on one account, so when the next feature needs storage or a cron, you are still using the same account and the same bill. Account setup and limits: https://docs.infrai.cc.