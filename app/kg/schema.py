"""Temporal-Causal Knowledge Graph Manager

Provides a GraphManager class with two backend modes:
- neo4j (if neo4j python driver is installed and NEO4J_URL provided)
- fallback: networkx DiGraph persisted into sqlite as JSON blobs

Nodes and edges have provenance and timestamps.
This is a scaffold and designed to be simple, robust and easy to extend.
"""

from datetime import datetime
import json
import os

# Try optional imports
try:
    from neo4j import GraphDatabase

    NEO4J_AVAILABLE = True
except Exception:
    NEO4J_AVAILABLE = False

import networkx as nx
import sqlite3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_DB = os.path.join(ROOT, "data", "kg.sqlite")
os.makedirs(os.path.dirname(DEFAULT_DB), exist_ok=True)


def _now_ts():
    return datetime.utcnow().isoformat() + "Z"


class GraphManager:
    def __init__(
        self, neo4j_url=None, neo4j_user=None, neo4j_password=None, db_path=DEFAULT_DB
    ):
        self.neo4j_url = neo4j_url
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.db_path = db_path
        self.use_neo4j = False
        if neo4j_url and NEO4J_AVAILABLE:
            try:
                self.driver = GraphDatabase.driver(
                    neo4j_url, auth=(neo4j_user, neo4j_password)
                )
                # quick verify
                with self.driver.session() as s:
                    s.run("RETURN 1").single()
                self.use_neo4j = True
            except Exception as e:
                print("Neo4j init failed, falling back to local graph:", e)
                self.driver = None
        # fallback graph
        self.graph = nx.DiGraph()
        # ensure sqlite
        self._init_sqlite()

    def _init_sqlite(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT)")
        conn.commit()
        conn.close()

    # Node insertion helpers
    def add_node(
        self,
        node_id,
        label,
        ntype="Event",
        timestamp=None,
        metadata=None,
        provenance=None,
    ):
        timestamp = timestamp or _now_ts()
        if metadata is None:
            metadata = {}
        if provenance is None:
            provenance = []
        node = {
            "id": node_id,
            "label": label,
            "type": ntype,
            "timestamp": timestamp,
            "metadata": metadata,
            "provenance": provenance,
        }
        if self.use_neo4j:
            with self.driver.session() as s:
                s.run(
                    """MERGE (n:Node {id:$id}) SET n.label=$label, n.type=$type, n.timestamp=$ts, n.metadata=$meta, n.provenance=$prov""",
                    id=node_id,
                    label=label,
                    type=ntype,
                    ts=timestamp,
                    meta=json.dumps(metadata),
                    prov=json.dumps(provenance),
                )
        else:
            self.graph.add_node(node_id, **node)
            self._persist_graph()

    def add_edge(self, src_id, dst_id, etype="RELATES_TO", properties=None):
        if properties is None:
            properties = {}
        edge = {"type": etype, "properties": properties, "first_observed": _now_ts()}
        if self.use_neo4j:
            with self.driver.session() as s:
                s.run(
                    """MATCH (a:Node {id:$src}), (b:Node {id:$dst}) MERGE (a)-[r:REL {type:$t}]->(b) SET r.props=$props""",
                    src=src_id,
                    dst=dst_id,
                    t=etype,
                    props=json.dumps(properties),
                )
        else:
            self.graph.add_edge(src_id, dst_id, **edge)
            self._persist_graph()

    def query_nodes(self, ntype=None, since_ts=None, until_ts=None):
        results = []
        for nid, data in self.graph.nodes(data=True):
            if ntype and data.get("type") != ntype:
                continue
            if since_ts and data.get("timestamp") < since_ts:
                continue
            if until_ts and data.get("timestamp") > until_ts:
                continue
            results.append((nid, data))
        return results

    def find_by_label(self, label_substr):
        matches = []
        for nid, data in self.graph.nodes(data=True):
            if label_substr.lower() in data.get("label", "").lower():
                matches.append((nid, data))
        return matches

    def _persist_graph(self):
        # persist graph nodes and edges as a JSON blob into sqlite
        gdata = {"nodes": {}, "edges": []}
        for nid, data in self.graph.nodes(data=True):
            gdata["nodes"][nid] = data
        for u, v, data in self.graph.edges(data=True):
            gdata["edges"].append((u, v, data))
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "REPLACE INTO kv (k,v) VALUES (?,?)", ("graph", json.dumps(gdata))
            )
            conn.commit()

    def load_graph(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT v FROM kv WHERE k=?", ("graph",))
            row = cur.fetchone()
            if not row:
                return
            payload = json.loads(row[0])
            self.graph = nx.DiGraph()
            for nid, data in payload.get("nodes", {}).items():
                self.graph.add_node(nid, **data)
            for u, v, ed in payload.get("edges", []):
                self.graph.add_edge(u, v, **ed)

    def close(self):
        if self.use_neo4j and self.driver:
            self.driver.close()
