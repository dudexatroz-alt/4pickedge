import sqlite3
from datetime import datetime

SCHEMA="""
CREATE TABLE IF NOT EXISTS daily_top4(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 snapshot_at TEXT NOT NULL,game_date TEXT NOT NULL,rank INTEGER NOT NULL,game_pk INTEGER,
 game TEXT NOT NULL,selection_text TEXT NOT NULL,side TEXT NOT NULL,market_type TEXT NOT NULL,
 token_id TEXT,market_price REAL,model_prob REAL,edge REAL,signal TEXT,result TEXT,settled_at TEXT,
 UNIQUE(game_date,rank)
);
"""

class Store:
    def __init__(self,path):
        self.path=path
        with sqlite3.connect(path) as c:c.executescript(SCHEMA)

    def save_top4(self,day,rows):
        with sqlite3.connect(self.path) as c:
            for i,r in enumerate(rows[:4],1):
                c.execute("""INSERT INTO daily_top4(snapshot_at,game_date,rank,game_pk,game,selection_text,side,market_type,token_id,market_price,model_prob,edge,signal)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(game_date,rank) DO UPDATE SET snapshot_at=excluded.snapshot_at,game_pk=excluded.game_pk,
                game=excluded.game,selection_text=excluded.selection_text,side=excluded.side,market_type=excluded.market_type,
                token_id=excluded.token_id,market_price=excluded.market_price,model_prob=excluded.model_prob,
                edge=excluded.edge,signal=excluded.signal""",
                (datetime.utcnow().isoformat(),day,i,r.get("game_pk"),r["game"],r["selection_text"],r["side"],r["market_type"],
                 r.get("token_id"),r.get("market_price"),r.get("model_prob"),r.get("edge"),r.get("signal")))

    def date_rows(self,day):
        with sqlite3.connect(self.path) as c:
            c.row_factory=sqlite3.Row
            return [dict(r) for r in c.execute("SELECT * FROM daily_top4 WHERE game_date=? ORDER BY rank",(day,))]

    def pending(self):
        with sqlite3.connect(self.path) as c:
            c.row_factory=sqlite3.Row
            return [dict(r) for r in c.execute("SELECT * FROM daily_top4 WHERE result IS NULL AND game_pk IS NOT NULL")]

    def set_result(self,id_,result):
        with sqlite3.connect(self.path) as c:
            c.execute("UPDATE daily_top4 SET result=?,settled_at=CURRENT_TIMESTAMP WHERE id=?",(result,id_))

    def stats(self):
        with sqlite3.connect(self.path) as c:
            c.row_factory=sqlite3.Row
            rows=[dict(r) for r in c.execute("SELECT * FROM daily_top4 ORDER BY game_date DESC,rank")]
        s=[r for r in rows if r["result"] in ("W","L","P")]
        w=sum(r["result"]=="W" for r in s);l=sum(r["result"]=="L" for r in s);p=sum(r["result"]=="P" for r in s)
        s1=[r for r in s if r["rank"]==1];s1w=sum(r["result"]=="W" for r in s1);s1l=sum(r["result"]=="L" for r in s1)
        return {"all":{"W":w,"L":l,"P":p,"hit_rate":w/(w+l) if w+l else None},
                "selection1":{"W":s1w,"L":s1l,"P":sum(r["result"]=="P" for r in s1),
                              "hit_rate":s1w/(s1w+s1l) if s1w+s1l else None}}
