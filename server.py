from flask import Flask,jsonify,request,send_from_directory
import os
from push_store import PushStore
from push_sender import push_enabled, send_push

DB=os.getenv("APP_DB","/tmp/4pickedge.db")
app=Flask(__name__,static_folder=".")

def ps():
    return PushStore(DB)

@app.get("/")
def home():
    return send_from_directory(".","index.html")

@app.get("/manifest.json")
def manifest():
    return send_from_directory(".","manifest.json")

@app.get("/sw.js")
def sw():
    return send_from_directory(".","sw.js",mimetype="application/javascript")

@app.get("/api/health")
def health():
    return jsonify({
        "ok":True,
        "version":"3.7-push-ready",
        "push_configured":push_enabled(),
        "trading_enabled":False
    })

@app.get("/api/push/public-key")
def public_key():
    key=os.getenv("VAPID_PUBLIC_KEY")
    if not key:
        return jsonify({"configured":False}),503
    return jsonify({"configured":True,"publicKey":key})

@app.post("/api/push/subscribe")
def subscribe():
    sub=request.get_json(force=True)
    ps().upsert(sub)
    return jsonify({"ok":True})

@app.post("/api/push/test")
def push_test():
    results=[]
    for sub in ps().all():
        results.append(send_push(sub,title="4 Pick Edge",body="Notificación de prueba ✅"))
    return jsonify({"ok":True,"results":results})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","8000")))
