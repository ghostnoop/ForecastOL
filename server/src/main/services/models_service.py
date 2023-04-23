import json
import os


def extract_fixtures() -> dict:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'fixtures.json'))
    with open(path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data
