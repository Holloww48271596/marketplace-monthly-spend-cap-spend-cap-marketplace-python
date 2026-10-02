from marketplace_service import MarketplaceSpendCap, OrderHandoff


class AccountStub:
    def set_budget(self, hard_cap_usd, period):
        return {"ok": True, "data": {"hard_cap_usd": hard_cap_usd, "period": period}}


def test_order_at_cap_is_accepted_and_next_order_is_rejected():
    cap = MarketplaceSpendCap(AccountStub(), monthly_cap_usd=10.0)
    assert cap.accept_order(OrderHandoff("o1", "b1", "a1", 10.0)) is True
    assert cap.accept_order(OrderHandoff("o2", "b2", "a2", 0.01)) is False

