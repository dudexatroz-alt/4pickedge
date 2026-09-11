def settle(pick,f):
    if f.get("status")!="Final":return None
    ar=f.get("away_runs");hr=f.get("home_runs")
    if ar is None or hr is None:return None
    mt=(pick.get("market_type") or "").lower();side=(pick.get("side") or "").lower()
    if mt=="moneyline":
        if ar==hr:return "P"
        return "W" if side==("away" if ar>hr else "home") else "L"
    if mt=="total":
        x=ar+hr;line=float(pick["line"])
        if x==line:return "P"
        return "W" if (side=="over" and x>line) or (side=="under" and x<line) else "L"
    if mt=="runline":
        line=float(pick["line"]);margin=(ar-hr) if side=="away" else (hr-ar);v=margin+line
        return "P" if v==0 else ("W" if v>0 else "L")
    if mt=="nrfi/yrfi":
        fir=f.get("first_inning_runs")
        if fir is None:return None
        yrfi=fir>0
        return "W" if (side=="yrfi" and yrfi) or (side=="nrfi" and not yrfi) else "L"
    return None
