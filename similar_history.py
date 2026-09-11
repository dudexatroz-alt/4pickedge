def probability_band(p):
    lo=int(float(p)*10)*10
    hi=min(lo+9,99)
    return f"{lo}-{hi}%"

def summarize_similar(rows, *, market_type, model_prob):
    band_lo=int(float(model_prob)*10)/10
    band_hi=band_lo+.1
    rel=[
        r for r in rows
        if (r.get("market_type") or "").lower()==market_type.lower()
        and r.get("model_prob") is not None
        and band_lo <= float(r["model_prob"]) < band_hi
        and r.get("result") in ("W","L")
    ]
    w=sum(r["result"]=="W" for r in rel)
    l=sum(r["result"]=="L" for r in rel)
    return {
        "band":probability_band(model_prob),
        "n":len(rel),
        "wins":w,
        "losses":l,
        "hit_rate":w/(w+l) if (w+l) else None,
        "sufficient_sample":len(rel)>=20
    }
