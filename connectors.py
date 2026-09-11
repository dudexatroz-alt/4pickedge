import requests
S=requests.Session()
S.headers.update({"User-Agent":"4PickEdge/3.2"})
MLB="https://statsapi.mlb.com/api"
GAMMA="https://gamma-api.polymarket.com"
CLOB="https://clob.polymarket.com"

def schedule(day,timeout=20):
    r=S.get(f"{MLB}/v1/schedule",params={"sportId":1,"date":day},timeout=timeout);r.raise_for_status()
    out=[]
    for d in r.json().get("dates",[]):
        for g in d.get("games",[]):
            t=g.get("teams") or {}
            out.append({
                "game_pk":g.get("gamePk"),"game_date":d.get("date"),"status":(g.get("status") or {}).get("abstractGameState"),
                "game_time":g.get("gameDate"),
                "away_team":((t.get("away") or {}).get("team") or {}).get("name"),
                "home_team":((t.get("home") or {}).get("team") or {}).get("name"),
                "away_pitcher":((t.get("away") or {}).get("probablePitcher") or {}).get("fullName"),
                "home_pitcher":((t.get("home") or {}).get("probablePitcher") or {}).get("fullName"),
            })
    return out

def final(game_pk,timeout=20):
    r=S.get(f"{MLB}/v1.1/game/{game_pk}/feed/live",timeout=timeout);r.raise_for_status()
    f=r.json(); status=((f.get("gameData") or {}).get("status") or {}).get("abstractGameState")
    ls=((f.get("liveData") or {}).get("linescore") or {});teams=ls.get("teams") or {};inn=ls.get("innings") or []
    first=inn[0] if inn else {}
    return {"status":status,
            "away_runs":((teams.get("away") or {}).get("runs")),
            "home_runs":((teams.get("home") or {}).get("runs")),
            "first_inning_runs":(((first.get("away") or {}).get("runs") or 0)+((first.get("home") or {}).get("runs") or 0)) if inn else None}

def search_market(q,timeout=20):
    r=S.get(f"{GAMMA}/public-search",params={"q":q},timeout=timeout);r.raise_for_status();return r.json()

def midpoint(token_id,timeout=20):
    r=S.get(f"{CLOB}/midpoint",params={"token_id":token_id},timeout=timeout);r.raise_for_status()
    d=r.json();v=d.get("mid_price",d.get("mid"))
    return float(v) if v is not None else None
