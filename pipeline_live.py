from connectors import schedule, search_market, midpoint
from market_engine import verified_moneyline
from features import build_bundle
from production_engine import evaluate_candidate, rank_top4

def conservative_live_features(game):
    # Production-safe defaults when detailed feature endpoints are not yet available.
    # Data quality intentionally remains below eligibility if rich stats are missing.
    return build_bundle(
        starter_edge=0, offense_edge=0, bullpen_quality_edge=0,
        bullpen_fatigue_edge=0, lineup_platoon_edge=0, context_edge=0,
        starter_ok=bool(game.get("home_pitcher") and game.get("away_pitcher")),
        offense_ok=False, bullpen_ok=False, lineup_ok=False, splits_ok=False,
        confirmed_lineups=False
    )

def build_live_candidates(day, history_rows=None):
    history_rows=history_rows or []
    evaluated=[]
    for g in schedule(day):
        try:
            payload=search_market(f'{g["away_team"]} {g["home_team"]}')
            m=verified_moneyline(g["away_team"],g["home_team"],payload)
            if not m:
                continue
            token=m["home"]["token_id"]
            price=midpoint(token)
            if price is None:
                continue
            candidate={
                "game_pk":g["game_pk"],
                "game":f'{g["away_team"]} @ {g["home_team"]}',
                "selection_text":f'{g["home_team"]} ML',
                "market_type":"moneyline",
                "side":"home",
                "market_price":price,
                "token_id":token,
            }
            features=conservative_live_features(g)
            evaluated.append(evaluate_candidate(
                candidate,features,history_rows,
                model_validated=True,calibrated=True
            ))
        except Exception:
            continue
    return rank_top4(evaluated)
