from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class FeatureBundle:
    starter_edge: float
    offense_edge: float
    bullpen_quality_edge: float
    bullpen_fatigue_edge: float
    lineup_platoon_edge: float
    context_edge: float
    data_quality: float
    confirmed_lineups: bool = False
    starter_data_complete: bool = False
    bullpen_data_complete: bool = False

    def as_dict(self):
        return asdict(self)

def clamp_edge(x):
    return max(-1.0, min(1.0, float(x)))

def quality_score(*, starter_ok, offense_ok, bullpen_ok, lineup_ok, splits_ok):
    score=0
    score += 22 if starter_ok else 0
    score += 20 if offense_ok else 0
    score += 18 if bullpen_ok else 0
    score += 20 if lineup_ok else 0
    score += 20 if splits_ok else 0
    return score

def build_bundle(
    starter_edge=0, offense_edge=0, bullpen_quality_edge=0,
    bullpen_fatigue_edge=0, lineup_platoon_edge=0, context_edge=0,
    starter_ok=False, offense_ok=False, bullpen_ok=False,
    lineup_ok=False, splits_ok=False, confirmed_lineups=False
):
    return FeatureBundle(
        clamp_edge(starter_edge),
        clamp_edge(offense_edge),
        clamp_edge(bullpen_quality_edge),
        clamp_edge(bullpen_fatigue_edge),
        clamp_edge(lineup_platoon_edge),
        clamp_edge(context_edge),
        quality_score(
            starter_ok=starter_ok, offense_ok=offense_ok, bullpen_ok=bullpen_ok,
            lineup_ok=lineup_ok, splits_ok=splits_ok
        ),
        confirmed_lineups=confirmed_lineups,
        starter_data_complete=starter_ok,
        bullpen_data_complete=bullpen_ok,
    )
