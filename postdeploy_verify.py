import os, sys, requests, json
BASE=os.environ.get("APP_BASE_URL","").rstrip("/")
if not BASE:
    raise SystemExit("Set APP_BASE_URL=https://your-service.onrender.com")

def get(path):
    r=requests.get(BASE+path,timeout=20)
    print(path, r.status_code)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return r.text[:300]

health=get("/api/health")
assert isinstance(health,dict) and health.get("ok") is True
print("health:",json.dumps(health,indent=2))

home=requests.get(BASE+"/",timeout=20)
assert home.status_code==200
assert "4 PICK" in home.text.upper()
print("home: OK")

print("Public HTTPS validation OK")
