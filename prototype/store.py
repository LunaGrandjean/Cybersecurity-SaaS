"""Local demo persistence. Inputs must already have been redacted by engine."""
import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path


class Store:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.lock = threading.RLock()
        with self.db:
            self.db.executescript("""
                CREATE TABLE IF NOT EXISTS tickets (id TEXT PRIMARY KEY, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, at TEXT NOT NULL,
                  ticket_id TEXT, actor TEXT NOT NULL, action TEXT NOT NULL, details TEXT NOT NULL);
                INSERT OR IGNORE INTO settings VALUES ('mode','suggestions');
            """)

    def mode(self):
        with self.lock:
            return self.db.execute("SELECT value FROM settings WHERE key='mode'").fetchone()[0]

    def event(self, ticket_id, actor, action, details):
        with self.lock, self.db:
            self.db.execute("INSERT INTO events(at,ticket_id,actor,action,details) VALUES(?,?,?,?,?)",
                            (datetime.now(timezone.utc).isoformat(), ticket_id, actor, action, json.dumps(details)))

    def set_mode(self, mode, actor, reason):
        with self.lock, self.db:
            self.db.execute("UPDATE settings SET value=? WHERE key='mode'", (mode,))
            self.event(None, actor, "switch_mode", {"mode": mode, "reason": reason})

    def put(self, ticket):
        with self.lock, self.db:
            self.db.execute("INSERT OR REPLACE INTO tickets VALUES(?,?)", (ticket["id"], json.dumps(ticket)))

    def get(self, ticket_id):
        with self.lock:
            row = self.db.execute("SELECT payload FROM tickets WHERE id=?", (ticket_id,)).fetchone()
            if row is None:
                raise KeyError(ticket_id)
            return json.loads(row[0])

    def tickets(self):
        with self.lock:
            return [json.loads(row[0]) for row in self.db.execute("SELECT payload FROM tickets ORDER BY id")]

    def events(self):
        with self.lock:
            return [dict(row) | {"details": json.loads(row["details"])} for row in self.db.execute("SELECT * FROM events ORDER BY id")]
