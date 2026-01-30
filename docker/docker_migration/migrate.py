
import json
from pymongo import MongoClient
import os
from pathlib import Path

# =================== CONFIG ===================
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
DB_NAME = os.getenv("DB_NAME", "projet_meteo")
COLLECTION_NAME = "stations_measures"
FINAL_FILE = "/data/output/final_mongo.json"

# =================== CONNEXION ===================
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
col = db[COLLECTION_NAME]

# =================== CHARGEMENT ===================
if not Path(FINAL_FILE).exists():
    raise FileNotFoundError(f"{FINAL_FILE} introuvable")

with open(FINAL_FILE, encoding="utf-8") as f:
    data = json.load(f)

print(f" Relevés chargés : {len(data)}")

# =================== NETTOYAGE ===================
col.delete_many({})
print(f" Collection '{COLLECTION_NAME}' nettoyée")

# =================== INSERTION ===================
if isinstance(data, list) and data:
    col.insert_many(data)
elif isinstance(data, dict):
    col.insert_one(data)

# =================== RÉSUMÉ ===================
count = col.count_documents({})
print(f" {count} documents dans la collection '{COLLECTION_NAME}'")
print(" Migration terminée avec succès")
