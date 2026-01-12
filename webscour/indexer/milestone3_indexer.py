import os
import json
import math
from bs4 import BeautifulSoup
from collections import defaultdict

# ---------- Path setup ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(BASE_DIR, "..", "pages")

if not os.path.exists(PAGES_DIR):
    raise FileNotFoundError(f"Pages folder not found: {PAGES_DIR}")

inverted_index = defaultdict(list)
doc_count = 0

# ---------- Read HTML pages ----------
for file in os.listdir(PAGES_DIR):
    if file.endswith(".html"):
        doc_count += 1
        path = os.path.join(PAGES_DIR, file)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            words = soup.get_text().lower().split()

            for word in set(words):
                inverted_index[word].append(file)

# ---------- Compute IDF ----------
idf = {}
for word, docs in inverted_index.items():
    idf[word] = math.log(doc_count / len(docs))

# ---------- Save files ----------
with open(os.path.join(BASE_DIR, "inverted_index.json"), "w", encoding="utf-8") as f:
    json.dump(inverted_index, f, indent=2)

with open(os.path.join(BASE_DIR, "idf.json"), "w", encoding="utf-8") as f:
    json.dump(idf, f, indent=2)

print("✅ Indexing completed")
print(f"📄 Documents indexed: {doc_count}")
print("📁 Files created: inverted_index.json, idf.json")
