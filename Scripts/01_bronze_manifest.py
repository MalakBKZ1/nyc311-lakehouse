import hashlib, json
from datetime import datetime
from pathlib import Path

DEST = Path("data/bronze/311/311_requests.csv")

def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(bloc)
    return h.hexdigest()

with open(DEST, encoding="utf-8") as f:
    entete = f.readline().strip().split(",")

manifeste = {
    "fichier": str(DEST),
    "date_manifeste": datetime.now().isoformat(timespec="seconds"),
    "taille_go": round(DEST.stat().st_size / 1e9, 3),
    "sha256": sha256(DEST),
    "nb_colonnes": len(entete),
    "entete": entete,
}
Path("docs").mkdir(exist_ok=True)
Path("docs/bronze_manifest.json").write_text(
    json.dumps(manifeste, indent=2, ensure_ascii=False), encoding="utf-8")

print(manifeste["taille_go"], "Go,", manifeste["nb_colonnes"], "colonnes")
print(entete)