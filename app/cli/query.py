import argparse
from app.rags.rag import rag_query

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--q", required=True)
    args = p.parse_args()
    print(rag_query(args.q))
