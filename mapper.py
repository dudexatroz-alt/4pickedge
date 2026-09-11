import json, ast, re

def _arr(v):
    if v is None:return []
    if isinstance(v,list):return v
    if isinstance(v,tuple):return list(v)
    if isinstance(v,str):
        for loader in (json.loads, ast.literal_eval):
            try:
                x=loader(v)
                if isinstance(x,(list,tuple)):return list(x)
            except Exception:
                pass
    return []

def norm(s):
    return re.sub(r"[^a-z0-9]+"," ",(s or "").lower()).strip()

def mapping(m):
    outcomes=_arr(m.get("outcomes"))
    tokens=_arr(m.get("clobTokenIds"))
    prices=_arr(m.get("outcomePrices"))
    if not outcomes or len(outcomes)!=len(tokens):return {}
    return {
        str(o):{
            "token_id":str(tokens[i]),
            "gamma_price":float(prices[i]) if i<len(prices) and prices[i] not in (None,"") else None
        } for i,o in enumerate(outcomes)
    }

def team_token(team,m):
    mp=mapping(m); target=norm(team)
    best=None
    for outcome,data in mp.items():
        no=norm(outcome)
        if no==target:return {"outcome":outcome,**data,"score":1.0}
        a=set(target.split()); b=set(no.split())
        score=(len(a&b)/len(a|b)) if a and b else 0
        if best is None or score>best["score"]:
            best={"outcome":outcome,**data,"score":score}
    return best if best and best["score"]>=.50 else None
