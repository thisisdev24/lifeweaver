
"""CLI: ingest a file, extract text, and index an Event node into the KG.
Usage:
  python -m app.cli.ingest_and_index --file path/to/doc.pdf --title "Meeting notes"
"""
import argparse, os, uuid
from app.ingest.extractors_ext import extract_text_from_pdf, extract_text_from_image, transcribe_audio
from app.kg.schema import GraphManager
from datetime import datetime, timezone

def mkid(prefix='evt'):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def ingest_and_index(path, title=None, kg_db=None):
    ext = os.path.splitext(path)[1].lower()
    text = ''
    if ext in ['.pdf']:
        text = extract_text_from_pdf(path)
    elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
        text = extract_text_from_image(path)
    elif ext in ['.mp3', '.wav', '.m4a', '.flac']:
        text = transcribe_audio(path)
    else:
        # try reading as text
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception:
            text = '[unknown file type or unreadable]'
    # prepare KG
    gm = GraphManager(db_path=kg_db) if kg_db else GraphManager()
    node_id = mkid('evt')
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    prov = [{'source_path': os.path.abspath(path), 'imported_at': ts}]
    gm.add_node(node_id, title or os.path.basename(path), ntype='Event', timestamp=ts, metadata={'snippet': text[:400]}, provenance=prov)
    print('Indexed node:', node_id)
    return node_id

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--file', required=True)
    p.add_argument('--title', required=False)
    args = p.parse_args()
    nid = ingest_and_index(args.file, args.title)
    print('Done. Node id:', nid)
