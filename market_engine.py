import difflib,re
from mapper import team_token

def norm(s):return re.sub(r"[^a-z0-9 ]+"," ",(s or "").lower()).strip()

def markets(payload):
    out=list(payload.get("markets") or [])
    for e in payload.get("events") or []:out.extend(e.get("markets") or [])
    return out

def verified_moneyline(away,home,payload):
    target=norm(f"{away} {home}");best=None
    for m in markets(payload):
        q=m.get("question") or m.get("title") or ""
        sim=difflib.SequenceMatcher(None,target,norm(q)).ratio()
        at=team_token(away,m);ht=team_token(home,m)
        if not at or not ht:continue
        if at["token_id"]==ht["token_id"] or at["outcome"]==ht["outcome"]:continue
        typ=(m.get("sportsMarketType") or m.get("sports_market_type") or "").lower()
        if typ and "moneyline" not in typ and "winner" not in typ:continue
        cand={"similarity":sim,"market":m,"away":at,"home":ht}
        if best is None or sim>best["similarity"]:best=cand
    return best if best and best["similarity"]>=.30 else None
