# SkoBot — AI-drevet Skobutik

SkoBot er en lokal RAG-baseret skoassistent der hjælper kunder med at finde den perfekte sko via en AI-chat assistent. Systemet bruger Ollama som lokal LLM og ChromaDB som vector database til RAG.

---

## Forudsætninger

Inden du starter skal du have installeret følgende:

- **Python 3.12** — download fra https://www.python.org/downloads/
- **Ollama** — download fra https://ollama.ai
- **Git** — download fra https://git-scm.com

---

## Installation

### 1. Klon projektet
```bash
git clone https://github.com/Alihussa2/skobot.git
cd skobot
```

### 2. Download AI-modellen
Åbn en terminal og kør:
```bash
ollama pull qwen2.5:3b
```
Dette downloader den lokale AI-model (ca. 2 GB). Vent til den er færdig.

### 3. Opret virtuelt Python-miljø
```bash
py -3.12 -m venv venv
```

### 4. Aktivér det virtuelle miljø

**Windows:**
```bash
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 5. Installer afhængigheder
```bash
pip install -r requirements.txt
```

---

## Start systemet

### 1. Start Ollama
Åbn en terminal og kør:
```bash
ollama serve
```
Hvis du får beskeden "address already in use" kører Ollama allerede — det er fint.

### 2. Start applikationen
Åbn en **ny** terminal, aktivér venv og kør:
```bash
venv\Scripts\activate.bat
uvicorn main:app --reload
```


-----
cd C:\Users\ali05\skobot
venv\Scripts\activate.bat
uvicorn main:app --reload
-----



### 3. Åbn browseren
Gå til:
```
http://localhost:8000
```

---

## Sådan bruger du siden

### Forsiden
- Når siden åbner ser du en **hero-sektion** øverst med en "Se sortiment" knap
- Klik på **"Se sortiment"** for at scrolle ned til produkterne
- Du kan **filtrere sko** efter type ved at klikke på kategori-knapperne (Løbesko, Sneakers, Vandresko osv.)

### Produktkort
Hvert produktkort viser:
- Billede af skoen
- Navn, type og pris
- Tilgængelige størrelser

På hvert kort er der to knapper:
- **"Spørg AI"** — åbner AI-assistenten og spørger om den specifikke sko
- **"Køb"** — åbner købs-dialog

### Køb en sko (mock)
1. Klik **"Køb"** på et produktkort
2. Vælg din størrelse i størrelsesguiden
3. Klik **"Læg i kurv"**
4. Du får en bekræftelsesbesked (mock — ingen rigtig betaling)

### AI Assistent
1. Klik på **"AI Assistent"** knappen øverst til højre ELLER på **💬 ikonet** nederst til højre
2. Skriv dit spørgsmål i chat-feltet — f.eks.:
   - *"Jeg søger løbesko til asfalt størrelse 42"*
   - *"Hvad er jeres billigste sko?"*
   - *"Anbefal en vandresko under 1500 kr"*
3. Tryk **Enter** eller klik **"Send"**
4. AI-assistenten finder relevante sko fra kataloget og giver en anbefaling

Du kan også klikke på de hurtige forslag-knapper i bunden af chat-vinduet.

---

## RAG kildemateriale

Skokatalogen ligger i filen `catalog.txt`. Den indlæses automatisk i ChromaDB når applikationen starter.

For at tilføje eller ændre sko:
1. Åbn `catalog.txt`
2. Tilføj en ny sko i samme format som de eksisterende
3. Genstart serveren med `uvicorn main:app --reload`

---

## Arkitektur

```
Browser (HTML/CSS/JS)
    └── FastAPI backend (main.py)
            ├── GET  /        — returnerer forsiden
            ├── GET  /shoes   — returnerer alle sko fra kataloget
            ├── POST /ask     — RAG + LLM svar
            └── POST /buy     — mock køb bekræftelse

RAG Pipeline:
    catalog.txt → ChromaDB (vector database) → Ollama (qwen2.5:3b)
```

## 4T's Prompt Engineering

Synlig i `main.py` under `SYSTEM_PROMPT`:

| T | Indhold |
|---|---|
| **Traits** | Erfaren og venlig skoekspert hos SkoBot |
| **Task** | Hjælp kunden med at finde den perfekte sko |
| **Tone** | Venlig, professionel og hjælpsom — svar altid på dansk |
| **Target** | Kunder der handler online og har brug for personlig rådgivning |

---

## Kendte begrænsninger

- Køb er **mock** — ingen rigtig betaling eller ordrehåndtering
- AI-modellen kan være **langsom** på ældre hardware (qwen2.5:3b kræver ca. 4 GB RAM)
- Svar er begrænset til **300 tokens** for hurtigere responstid
- Kataloget er statisk — ingen dynamisk database

---

## Teknologier

| Teknologi | Formål |
|---|---|
| FastAPI | Backend web framework |
| ChromaDB | Vector database til RAG |
| Ollama | Lokal LLM runtime |
| qwen2.5:3b | Lokal sprogmodel |
| HTML/CSS/JS | Frontend |
