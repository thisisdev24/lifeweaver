import os, tempfile
from app.kg.schema import GraphManager
from app.kg.causal import causal_score

def test_graph_add_and_query():
    tmpdb = os.path.join(tempfile.gettempdir(), 'kg_test.sqlite')
    if os.path.exists(tmpdb):
        try:
            os.remove(tmpdb)
        except Exception:
            pass
    gm = GraphManager(db_path=tmpdb)
    gm.add_node('n1', 'Test Event 1', ntype='Event')
    gm.add_node('n2', 'Test Event 2', ntype='Event')
    gm.add_edge('n1', 'n2', etype='CAUSES', properties={'reason': 'unit-test'})
    nodes = gm.query_nodes(ntype='Event')
    assert any(nid=='n1' for nid, _ in nodes)
    gm.load_graph()
    nodes2 = gm.query_nodes()
    assert len(nodes2) >= 2

def test_causal_score_basic():
    s = causal_score('2023-01-01T00:00:00Z', '2023-01-02T00:00:00Z', count_joint=3, count_a=3, count_b=4)
    assert 0.0 <= s <= 1.0
