from model import intrinsic_probability, edge, signal
from gate import elite_gate, selection_label
from similar_history import summarize_similar

def evaluate_candidate(candidate, feature_bundle, history_rows, model_validated=True, calibrated=True):
    model_prob=intrinsic_probability(feature_bundle)
    market_prob=candidate.get("market_price")
    e=edge(model_prob,market_prob)
    sig=signal(e,feature_bundle.data_quality)
    hist=summarize_similar(history_rows,market_type=candidate.get("market_type","moneyline"),model_prob=model_prob)
    gate=elite_gate(
        model_validated=model_validated,
        model_prob=model_prob,
        edge=e,
        data_quality=feature_bundle.data_quality,
        historical_n=hist["n"],
        historical_hit_rate=hist["hit_rate"],
        calibrated=calibrated,
    )
    eligible=(e is not None and e>=.04 and feature_bundle.data_quality>=80 and model_prob>=.58)
    return {
        **candidate,
        "model_prob":model_prob,
        "edge":e,
        "signal":sig,
        "eligible":eligible,
        "elite_gate":gate,
        "selection_label":selection_label(gate,has_pick=eligible),
        "similar_history":hist,
        "feature_bundle":feature_bundle.as_dict(),
    }

def rank_top4(rows):
    valid=[r for r in rows if r.get("eligible")]
    valid.sort(key=lambda r:(r.get("edge") or -9,r.get("model_prob") or 0),reverse=True)
    return valid[:4]
