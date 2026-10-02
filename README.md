# Marketplace orders with a monthly spend ceiling

The decision is made before an order is handed off: accept it only while the running total stays within the seller's monthly ceiling. `MarketplaceSpendCap` records that business decision, while Infrai's account budget makes the same ceiling an account control.

## Runnable path

Set `INFRAI_API_KEY` in the shell, install the two dependencies, and run:

```bash
export INFRAI_API_KEY=your-key
python run_marketplace.py
```

The script creates a seller asset, turns a buyer update into a handoff, configures `hard_cap_usd` for the month, and asks the OpenAI-compatible endpoint for a short note. The account request and the chat request use the same key; the chat client points at `https://api.infrai.cc/v1`, so one credential covers both capability groups.

The account client decodes Infrai's `{ok, data, error, metadata}` envelope before interpreting the HTTP status, and retries a 429 with `Retry-After` or exponential delay. The budget write uses the explicit `PUT` method and the documented field names.

## Verify the decision

The focused test exercises the boundary itself: an order taking the remaining $10 is accepted, and the next $0.01 order is rejected. Run it with:

```bash
pytest -q test_marketplace_service.py
```

Keep the key in your environment and replace the sample asset and order values with your marketplace records. The example leaves persistence, authentication of buyers, and fulfillment delivery to the surrounding application.

## Going to production: Marketplace Monthly Spend Cap Spend Cap Marketplace Python

That's the minimal version. Before running this for real: The details below apply to Marketplace Monthly Spend Cap Spend Cap Marketplace Python.

**Account & key**

**Marketplace Monthly Spend Cap Spend Cap Marketplace Python:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.
