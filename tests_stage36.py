from pathlib import Path
required=[
 "server.py","render.yaml","Dockerfile","requirements.txt",
 "WORK_DEPLOY_PROMPT.txt","postdeploy_verify.py","RELEASE_STATUS.txt"
]
for f in required:
    assert Path(f).exists(), f
txt=Path("WORK_DEPLOY_PROMPT.txt").read_text()
assert "/api/health" in txt
assert "Polymarket" in txt
assert "No habilitar trading" in txt
print("deploy handoff tests OK")
