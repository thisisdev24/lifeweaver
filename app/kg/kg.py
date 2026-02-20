import os, json, sqlite3
import networkx as nx

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(ROOT, "data", "kg.sqlite")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def init_graph():
    g = nx.DiGraph()
    return g


def save_graph_stub(graph, path=DB_PATH):
    # Simple stub to persist nodes as JSON in sqlite for MVP
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT)")
        conn.execute(
            "REPLACE INTO kv (k,v) VALUES (?,?)",
            ("graph", json.dumps({"nodes": list(graph.nodes)})),
        )
