import tempfile, os
from features import build_bundle
from model import intrinsic_probability
from notification import pick_result_alert

f=build_bundle(starter_edge=.5,offense_edge=.3,bullpen_quality_edge=.2,
               bullpen_fatigue_edge=.1,lineup_platoon_edge=.4,context_edge=.1,
               starter_ok=True,offense_ok=True,bullpen_ok=True,lineup_ok=True,splits_ok=True)
p=intrinsic_probability(f)
assert .5<p<=.9
assert pick_result_alert("A ML","W","A @ B").title.startswith("✅")

for fn in ("render.yaml","Dockerfile","server.py","index.html"):
    assert os.path.exists(fn)
print("final beta bundle tests OK")
