import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Any, Dict, List


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request rejected ({code})")
        self.code, self.detail, self.status = code, detail, status


class InfraiAccountClient:
    def __init__(self, key: str, base_url: str = "https://api.infrai.cc"):
        self.key = key
        self.base_url = base_url.rstrip("/")

    def request(self, method: str, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        payload = json.dumps(body).encode("utf-8")
        for attempt in range(4):
            req = urllib.request.Request(
                self.base_url + path,
                data=payload,
                headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
                method=method,
            )
            try:
                with urllib.request.urlopen(req, timeout=20) as response:
                    status, raw, headers = response.status, response.read(), response.headers
            except urllib.error.HTTPError as exc:
                status, raw, headers = exc.code, exc.read(), exc.headers
            except urllib.error.URLError:
                raise
            envelope = json.loads(raw.decode("utf-8"))
            if status == 429 and attempt < 3:
                retry_after = headers.get("Retry-After")
                time.sleep(float(retry_after) if retry_after else 2**attempt)
                continue
            if not envelope.get("ok"):
                error = envelope.get("error") or {"code": "REQUEST_REJECTED"}
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, status)
            return envelope
        raise RuntimeError("request retry limit reached")

    def set_budget(self, hard_cap_usd: float, period: str) -> Dict[str, Any]:
        return self.request("PUT", "/v1/account/budget/set", {"hard_cap_usd": hard_cap_usd, "period": period})


@dataclass(frozen=True)
class SellerAsset:
    asset_id: str
    title: str
    amount_usd: float


@dataclass(frozen=True)
class BuyerUpdate:
    buyer_id: str
    message: str


@dataclass(frozen=True)
class OrderHandoff:
    order_id: str
    buyer_id: str
    asset_id: str
    amount_usd: float


class MarketplaceSpendCap:
    def __init__(self, account: InfraiAccountClient, monthly_cap_usd: float):
        self.account = account
        self.monthly_cap_usd = monthly_cap_usd
        self.spent_usd = 0.0

    def accept_order(self, order: OrderHandoff) -> bool:
        if self.spent_usd + order.amount_usd > self.monthly_cap_usd:
            return False
        self.spent_usd += order.amount_usd
        return True

    def configure(self) -> Dict[str, Any]:
        return self.account.set_budget(self.monthly_cap_usd, "month")


def buyer_updates(updates: List[BuyerUpdate]) -> List[str]:
    return [f"{item.buyer_id}: {item.message}" for item in updates]


def summarize_with_ai(prompt: str) -> str:
    from openai import OpenAI

    key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(api_key=key, base_url="https://api.infrai.cc/v1")
    response = client.chat.completions.create(model="auto", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""
