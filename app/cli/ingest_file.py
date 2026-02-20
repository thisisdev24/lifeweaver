import argparse
from app.ingest.watcher import simple_import

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    args = p.parse_args()
    print("Importing", args.file)
    path = simple_import(args.file)
    print("Imported to", path)
