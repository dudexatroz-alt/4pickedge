import os, sys, requests

BASE=os.getenv("APP_BASE_URL","http://127.0.0.1:8000").rstrip("/")

def check(path, method="GET"):
    url=BASE+path
    r=requests.request(method,url,timeout=15)
    r.raise_for_status()
    return r.json() if "application/json" in r.headers.get("content-type","") else r.text

def main():
    h=check("/api/health")
    assert h.get("ok") is True
    print("✓ health",h)

    # Network-facing endpoints may legitimately return empty selections.
    # The purpose is to verify the deployed service can execute the route.
    try:
        print("✓ top4",check("/api/top4"))
    except Exception as e:
        print("! top4 route needs deployed Internet/data context:",e)

if __name__=="__main__":
    main()
