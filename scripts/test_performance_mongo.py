import time
from pymongo import MongoClient

client = MongoClient("mongodb://13.37.248.173:27018")
db = client["meteo"]

start = time.time()

results = list(db.measures.find({
    "city": "La Madeleine",
    "timestamp": {
        "$gte": "2024-10-01T00:00:00Z",
        "$lte": "2024-10-01T23:59:59Z"
    }
}))

end = time.time()

print("Nombre de documents trouvés :", len(results))
print("Temps d'exécution (ms):", (end - start) * 1000)
