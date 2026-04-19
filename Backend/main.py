from fastapi import FastAPI

# FastAPI
app = FastAPI(title="DSS Inventory API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to DSS Inventory API. Backend is running!"}

# --- Abdourahman: Buraya ROP ve EOQ hesaplayan ve veritabanına bağlanan endpoint'leri ekleyebilirsin ---

@app.get("/api/status")
def get_status():
    return {"status": "ok", "database": "waiting for connection details from Erva"}