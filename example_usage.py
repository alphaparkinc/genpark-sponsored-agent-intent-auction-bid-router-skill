"""Example usage for SponsoredAgentIntentAuctionRouter."""
import json
from client import SponsoredAgentIntentAuctionRouter

def main():
    print("=== Sponsored Agent Intent Auction & Monetization Demo ===")
    router = SponsoredAgentIntentAuctionRouter()
    
    # 1. Register brand campaigns
    router.register_sponsor_campaign("Instacart Express", ["groceries", "food delivery", "fresh fruit"], bid_cpc_usd=3.20)
    router.register_sponsor_campaign("Walmart Grocery", ["groceries", "snacks", "household"], bid_cpc_usd=2.10)
    
    # 2. Run auction on user intent
    query = "Find me fresh groceries for dinner tonight"
    auction = router.conduct_intent_auction(query)
    print("Intent Auction Result:", json.dumps(auction, indent=2))
    
    # 3. Format transparent sponsored recommendation
    rec = router.format_sponsored_recommendation(query, "Organic choice: Whole Foods Market on 4th Street.")
    print("\nFormatted Co-Recommendation:", json.dumps(rec, indent=2))

if __name__ == "__main__":
    main()
