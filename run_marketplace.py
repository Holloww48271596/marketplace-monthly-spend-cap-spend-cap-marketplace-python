import os
from marketplace_service import BuyerUpdate, InfraiAccountClient, MarketplaceSpendCap, OrderHandoff, SellerAsset, buyer_updates, summarize_with_ai


def main() -> None:
    key = os.environ["INFRAI_API_KEY"]
    account = InfraiAccountClient(key)
    cap = MarketplaceSpendCap(account, monthly_cap_usd=25.0)
    cap.configure()
    asset = SellerAsset("asset-17", "Field guide", 12.0)
    order = OrderHandoff("order-100", "buyer-9", asset.asset_id, asset.amount_usd)
    accepted = cap.accept_order(order)
    print({"order_id": order.order_id, "accepted": accepted, "spent_usd": cap.spent_usd})
    print(buyer_updates([BuyerUpdate(order.buyer_id, "Order handed to fulfillment")]))
    if accepted:
        print(summarize_with_ai(f"Write a one-line handoff note for {order.order_id}."))


if __name__ == "__main__":
    main()
