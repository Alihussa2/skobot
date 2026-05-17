from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import chromadb
import ollama

app = FastAPI()

# ─── RAG SETUP ───────────────────────────────────────────
client = chromadb.Client()
collection = client.get_or_create_collection("skobot")

def parse_catalog():
    with open("catalog.txt", "r", encoding="utf-8") as f:
        content = f.read()
    shoes = []
    for block in content.strip().split("\n\n"):
        if not block.strip():
            continue
        shoe = {}
        for line in block.strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                shoe[key.strip()] = val.strip()
        if shoe:
            shoes.append(shoe)
    return shoes

def load_catalog():
    shoes = parse_catalog()
    for i, shoe in enumerate(shoes):
        text = "\n".join([f"{k}: {v}" for k, v in shoe.items()])
        collection.upsert(
            documents=[text],
            ids=[f"shoe_{i}"]
        )
    print(f"Indlæst {len(shoes)} sko i RAG database")

load_catalog()
ALL_SHOES = parse_catalog()

# ─── 4T's PROMPT ─────────────────────────────────────────
SYSTEM_PROMPT = """
Traits: Du er en erfaren og venlig skoekspert hos SkoBot — en moderne dansk skobutik.
Task: Din opgave er at hjælpe kunden med at finde den perfekte sko baseret på deres behov, størrelse og budget.
Tone: Venlig, professionel og hjælpsom. Svar altid på dansk.
Target: Kunder der handler online og har brug for personlig rådgivning.

Du må KUN anbefale sko der er i det medfølgende katalog.
Hvis du ikke kan finde en passende sko, skal du sige det ærligt.
Giv altid pris og størrelsesinformation når du anbefaler en sko.
"""

# ─── API ENDPOINTS ────────────────────────────────────────
class Question(BaseModel):
    question: str

class Order(BaseModel):
    shoe_name: str
    size: str

@app.get("/", response_class=HTMLResponse)
def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/shoes")
def get_shoes():
    return ALL_SHOES

@app.post("/ask")
def ask(q: Question):
    results = collection.query(
        query_texts=[q.question],
        n_results=3
    )
    context = "\n\n".join(results["documents"][0])
    prompt = f"""
Her er relevante sko fra vores katalog:

{context}

Kundens spørgsmål: {q.question}

Svar på dansk. Anbefal den mest relevante sko med navn, pris og hvorfor den passer til kunden.
"""
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        options={"num_predict": 300}
    )
    images = []
    for doc in results["documents"][0]:
        for line in doc.split("\n"):
            if line.startswith("Billede:"):
                images.append(line.replace("Billede:", "").strip())
    return {
        "answer": response["message"]["content"],
        "images": images
    }

@app.post("/buy")
def buy(order: Order):
    return {
        "success": True,
        "message": f"Tak for din ordre! {order.shoe_name} i størrelse {order.size} er bestilt. Du modtager en bekræftelse på e-mail. 🎉"
    }