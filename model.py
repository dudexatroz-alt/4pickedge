import math

WEIGHTS={
    "starter_edge":0.30,
    "offense_edge":0.22,
    "bullpen_quality_edge":0.15,
    "bullpen_fatigue_edge":0.10,
    "lineup_platoon_edge":0.18,
    "context_edge":0.05,
}

def sigmoid(x):
    return 1/(1+math.exp(-x))

def intrinsic_probability(bundle):
    # Market price is intentionally excluded.
    raw=sum(getattr(bundle,k)*w for k,w in WEIGHTS.items())
    p=sigmoid(raw*2.35)
    return max(.10,min(.90,p))

def away_probability(home_probability):
    return 1-float(home_probability)

def edge(model_prob, market_prob):
    if market_prob is None:return None
    return float(model_prob)-float(market_prob)

def signal(e, data_quality):
    if e is None:return "SIN PRECIO"
    if data_quality < 80:return "DATOS INSUFICIENTES"
    if e>=.07:return "FUERTE"
    if e>=.04:return "ELEGIBLE"
    if e>=0:return "ESPERAR"
    return "NO ENTRAR"
