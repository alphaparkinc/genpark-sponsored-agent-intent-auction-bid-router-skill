"""Client module for SponsoredAgentIntentAuctionRouter (100% Python Standard Library)."""
import json
import time
import uuid
import math
from typing import Dict, Any, List, Optional

class SponsoredAgentIntentAuctionRouter:
    """Manages intent-based brand auction bidding for autonomous agents, implementing
    Vickrey second-price pricing, relevance weighting, and transparent disclosure formatting."""
    
    def __init__(self):
        self.campaigns: Dict[str, Dict[str, Any]] = {}
        self.attributions: List[Dict[str, Any]] = []

    def register_sponsor_campaign(self, brand_name: str, target_keywords: List[str], bid_cpc_usd: float, quality_score: float = 0.9, ad_creative: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Registers a merchant sponsor campaign for agentic commercial queries."""
        cid = f"cmp_{uuid.uuid4().hex[:8]}"
        campaign = {
            "campaign_id": cid,
            "brand_name": brand_name,
            "keywords": [k.lower() for k in target_keywords],
            "bid_cpc_usd": round(float(bid_cpc_usd), 2),
            "quality_score": max(0.1, min(1.0, float(quality_score))),
            "ad_creative": ad_creative or {
                "headline": f"Featured Choice from {brand_name}",
                "call_to_action": "View Official Store Offer"
            },
            "active": True
        }
        self.campaigns[cid] = campaign
        return {"status": "success", "campaign_id": cid, "campaign": campaign}

    def conduct_intent_auction(self, query_text: str) -> Dict[str, Any]:
        """Runs a generalized second-price (GSP) auction based on keyword relevance and quality score."""
        q_words = set(query_text.lower().split())
        candidates = []
        
        for cid, cmp in self.campaigns.items():
            if not cmp["active"]: continue
            matched_keywords = [k for k in cmp["keywords"] if any(w in k for w in q_words)]
            if matched_keywords:
                relevance = len(matched_keywords) / max(1, len(cmp["keywords"]))
                ecpm = cmp["bid_cpc_usd"] * cmp["quality_score"] * (1.0 + relevance)
                candidates.append({
                    "campaign_id": cid,
                    "brand": cmp["brand_name"],
                    "bid": cmp["bid_cpc_usd"],
                    "ecpm": round(ecpm, 4),
                    "relevance": round(relevance, 2),
                    "creative": cmp["ad_creative"]
                })
                
        if not candidates:
            return {"status": "no_bids_matched", "winner": None, "clearing_price_usd": 0.0}
            
        candidates.sort(key=lambda x: x["ecpm"], reverse=True)
        winner = candidates[0]
        
        # Second-price calculation: charge just above second place bid (or 60% of own bid if alone)
        if len(candidates) > 1:
            second_place_ecpm = candidates[1]["ecpm"]
            clearing_price = max(0.10, round(second_place_ecpm / (winner["relevance"] + 0.1), 2))
        else:
            clearing_price = round(winner["bid"] * 0.70, 2)
            
        return {
            "status": "success",
            "query": query_text,
            "bids_evaluated": len(candidates),
            "winner": winner,
            "clearing_price_usd": clearing_price
        }

    def format_sponsored_recommendation(self, query: str, organic_recommendation: str) -> Dict[str, Any]:
        """Synthesizes organic recommendation with clearly disclosed sponsored partner alternative."""
        auction = self.conduct_intent_auction(query)
        winner = auction.get("winner")
        
        sponsored_block = None
        if winner:
            sponsored_block = {
                "badge": "SPONSORED_PARTNER",
                "brand": winner["brand"],
                "headline": winner["creative"]["headline"],
                "cta": winner["creative"]["call_to_action"],
                "clearing_cpc_usd": auction["clearing_price_usd"]
            }
            
        return {
            "status": "success",
            "organic_answer": organic_recommendation,
            "has_sponsored_placement": winner is not None,
            "sponsored_placement": sponsored_block
        }

    def record_conversion_attribution(self, campaign_id: str, action_type: str = "CLICK", revenue_usd: float = 0.0) -> Dict[str, Any]:
        """Logs click-through or transaction conversion for attribution and merchant billing."""
        event_id = f"evt_{uuid.uuid4().hex[:8]}"
        record = {
            "event_id": event_id,
            "campaign_id": campaign_id,
            "action_type": action_type,
            "revenue_usd": revenue_usd,
            "timestamp": time.time()
        }
        self.attributions.append(record)
        return {"status": "success", "event_id": event_id, "attribution": record}
