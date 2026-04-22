from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import os
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

# .env dosyasından bağlantı bilgilerini yükle
load_dotenv()

app = FastAPI(title="DSS Inventory API", version="1.0")

# ─────────────────────────────────────────
# SABİTLER — Yaren'in formüllerinden
# ─────────────────────────────────────────
Z = 1.645        # %95 servis düzeyi
CV = 0.20        # Talep değişkenlik katsayısı
DAYS_PER_YEAR = 365

# ─────────────────────────────────────────
# VERİTABANI BAĞLANTISI
# ─────────────────────────────────────────
def get_db():
    # .env dosyasındaki bilgilerle PostgreSQL'e bağlan
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "stok_takip_sistemi"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        port=os.getenv("DB_PORT", 5432)
    )
    return conn

# ─────────────────────────────────────────
# YAREN'İN FORMÜLLERI — Hesaplama fonksiyonu
# ─────────────────────────────────────────
def calculate_metrics(product: dict) -> dict:
    d = product["daily_sales_rate"]   # günlük satış hızı
    L = product["lead_time_days"]     # teslim süresi
    S = product["ordering_cost"]      # sipariş maliyeti
    H = product["holding_cost"]       # tutma maliyeti
    P = product["unit_cost"]          # birim fiyat
    I = product["initial_stock"]      # başlangıç stoğu

    # LTD — Sipariş teslim süresi talebi
    LTD = d * L

    # SS — Emniyet stoğu
    sigma_d = CV * d
    SS = round(Z * sigma_d * np.sqrt(L), 1)

    # ROP — Yeniden sipariş noktası
    ROP = round(LTD + SS, 0)

    # EOQ — Ekonomik sipariş miktarı
    D_annual = d * DAYS_PER_YEAR
    EOQ = round(np.sqrt(2 * D_annual * S / H), 0) if H > 0 else None

    # TC — Toplam yıllık maliyet
    TC = round(D_annual * P + (D_annual / EOQ) * S + (EOQ / 2) * H, 0) if EOQ else None

    # Tampon ve durum
    Buffer = I - ROP
    Days_to_ROP = round(Buffer / d, 0) if d > 0 else None
    Status = "Yeterli" if I >= ROP else "Kritik"

    return {
        "LTD": LTD,
        "SS": SS,
        "ROP": int(ROP),
        "EOQ": int(EOQ) if EOQ else None,
        "TC": int(TC) if TC else None,
        "Buffer": int(Buffer),
        "Days_to_ROP": int(Days_to_ROP) if Days_to_ROP else None,
        "Status": Status
    }

# ─────────────────────────────────────────
# PYDANTIC MODELİ — POST için veri formatı
# ─────────────────────────────────────────
class InventoryUpdate(BaseModel):
    product_id: int
    change_amount: int
    change_type: str  # "purchase" | "sale" | "adjustment"

# ─────────────────────────────────────────
# SEDRA'NIN ENDPOINTLERİ — dokunma
# ─────────────────────────────────────────
@app.get("/")
def read_root():
    return {"message": "Welcome to DSS Inventory API. Backend is running!"}

@app.get("/api/status")
def get_status():
    return {"status": "ok", "database": "connected"}

# ─────────────────────────────────────────
# GET /products — Tüm ürünleri + hesaplamaları getir
# ─────────────────────────────────────────
@app.get("/products")
def get_products():
    try:
        # Veritabanına bağlan ve tüm ürünleri çek
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM public.products ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Her ürün için Yaren'in formülleriyle hesapla
        products = []
        for row in rows:
            row = dict(row)
            metrics = calculate_metrics(row)
            row.update(metrics)  # hesaplanan değerleri ürüne ekle
            products.append(row)

        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─────────────────────────────────────────
# POST /inventory/update — Stok güncelle
# ─────────────────────────────────────────
@app.post("/inventory/update")
def update_inventory(payload: InventoryUpdate):
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Ürünün var olup olmadığını kontrol et
        cur.execute("SELECT id, initial_stock FROM public.products WHERE id = %s;", (payload.product_id,))
        product = cur.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")

        # Yeni stok miktarını hesapla
        new_stock = product["initial_stock"] + payload.change_amount
        if new_stock < 0:
            raise HTTPException(status_code=400, detail="Stok negatife düşemez")

        # Stoku güncelle
        cur.execute(
            "UPDATE public.products SET initial_stock = %s WHERE id = %s;",
            (new_stock, payload.product_id)
        )

        # Hareketi inventory_logs tablosuna kaydet
        cur.execute(
            """INSERT INTO public.inventory_logs 
               (product_id, change_amount, change_type, log_date)
               VALUES (%s, %s, %s, %s);""",
            (payload.product_id, payload.change_amount, payload.change_type, datetime.now())
        )

        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Stok güncellendi",
            "product_id": payload.product_id,
            "new_stock": new_stock
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))