import sqlite3, json, os

SCHEMA="""
CREATE TABLE IF NOT EXISTS push_subscriptions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT UNIQUE NOT NULL,
    subscription_json TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

class PushStore:
    def __init__(self,path):
        self.path=path
        with sqlite3.connect(self.path) as c:
            c.executescript(SCHEMA)

    def upsert(self, subscription):
        endpoint=subscription.get("endpoint")
        if not endpoint:
            raise ValueError("subscription endpoint required")
        with sqlite3.connect(self.path) as c:
            c.execute("""
            INSERT INTO push_subscriptions(endpoint,subscription_json)
            VALUES(?,?)
            ON CONFLICT(endpoint) DO UPDATE SET subscription_json=excluded.subscription_json
            """,(endpoint,json.dumps(subscription)))
        return True

    def all(self):
        with sqlite3.connect(self.path) as c:
            rows=c.execute("SELECT endpoint,subscription_json FROM push_subscriptions").fetchall()
        return [json.loads(r[1]) for r in rows]

    def remove_endpoint(self,endpoint):
        with sqlite3.connect(self.path) as c:
            c.execute("DELETE FROM push_subscriptions WHERE endpoint=?",(endpoint,))
