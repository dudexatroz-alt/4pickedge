from flask import Flask, jsonify, request, send_from_directory
import os
from datetime import datetime

from push_store import PushStore
from push_sender import push_enabled, send_push
from connectors import schedule, final
from pipeline_live import build_live_candidates
from store import Store
from settlement import settle

DB = os.getenv("APP_DB", "/tmp/4pickedge.db")
app = Flask(__name__, static_folder=".")


def ps():
    return PushStore(DB)


def store():
    return Store(DB)


@app.get("/")
def home():
    return send_from_directory(".", "index.html")


@app.get("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")


@app.get("/sw.js")
def sw():
    return send_from_directory(".", "sw.js", mimetype="application/javascript")


@app.get("/api/health")
def health():
    return jsonify({
        "ok": True,
        "version": "3.8-dashboard",
        "push_configured": push_enabled(),
        "trading_enabled": False,
        "db": DB,
    })


@app.get("/api/schedule")
def api_schedule():
    day = request.args.get("date") or datetime.utcnow().date().isoformat()
    try:
        return jsonify({"date": day, "games": schedule(day)})
    except Exception as e:
        return jsonify({"date": day, "games": [], "error": str(e)}), 502


@app.get("/api/top4")
def api_top4():
    day = request.args.get("date") or datetime.utcnow().date().isoformat()
    refresh = request.args.get("refresh") in ("1", "true", "yes")
    s = store()
    rows = s.date_rows(day)
    error = None
    if refresh or not rows:
        try:
            picks = build_live_candidates(day, history_rows=[])
            if picks:
                s.save_top4(day, picks)
                rows = s.date_rows(day)
        except Exception as e:
            error = str(e)
    return jsonify({"date": day, "count": len(rows), "picks": rows, "error": error})


@app.post("/api/top4/manual")
def api_top4_manual():
    body = request.get_json(force=True) or {}
    day = body.get("date") or datetime.utcnow().date().isoformat()
    picks = body.get("picks") or []
    if not isinstance(picks, list):
        return jsonify({"error": "picks must be a list"}), 400
    normalized = []
    for p in picks[:4]:
        required = ("game", "selection_text", "side", "market_type")
        if any(not p.get(k) for k in required):
            return jsonify({"error": "Each pick needs game, selection_text, side and market_type"}), 400
        normalized.append({
            "game_pk": p.get("game_pk"),
            "game": p["game"],
            "selection_text": p["selection_text"],
            "side": p["side"],
            "market_type": p["market_type"],
            "token_id": p.get("token_id"),
            "market_price": p.get("market_price"),
            "model_prob": p.get("model_prob"),
            "edge": p.get("edge"),
            "signal": p.get("signal") or "MANUAL",
        })
    s = store()
    s.save_top4(day, normalized)
    return jsonify({"ok": True, "date": day, "picks": s.date_rows(day)})


@app.get("/api/history")
def api_history():
    day = request.args.get("date")
    s = store()
    if day:
        return jsonify({"date": day, "picks": s.date_rows(day)})
    return jsonify({"stats": s.stats()})


@app.get("/api/stats")
def api_stats():
    return jsonify(store().stats())


@app.post("/api/settle")
def api_settle():
    s = store()
    changed = []
    errors = []
    for pick in s.pending():
        try:
            snapshot = final(pick["game_pk"])
            result = settle(pick, snapshot)
            if result:
                s.set_result(pick["id"], result)
                changed.append({"id": pick["id"], "result": result})
        except Exception as e:
            errors.append({"id": pick.get("id"), "error": str(e)})
    return jsonify({"ok": True, "settled": changed, "errors": errors})


@app.get("/api/push/public-key")
def public_key():
    key = os.getenv("VAPID_PUBLIC_KEY")
    if not key:
        return jsonify({"configured": False}), 503
    return jsonify({"configured": True, "publicKey": key})


@app.post("/api/push/subscribe")
def subscribe():
    sub = request.get_json(force=True)
    ps().upsert(sub)
    return jsonify({"ok": True})


@app.post("/api/push/test")
def push_test():
    results = []
    for sub in ps().all():
        results.append(send_push(sub, title="4 Pick Edge", body="Notificación de prueba ✅"))
    return jsonify({"ok": True, "results": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
