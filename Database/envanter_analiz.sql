-- ═══════════════════════════════════════════════════════════════════
--  Envanter Stok Yönetimi — Stokastik Model
--  Rapordaki tüm hesaplamalar: LTD, SS, ROP, EOQ, TC, Stok Analizi
--  Uyumluluk: PostgreSQL / SQLite (POWER → POW, SQRT standart)
-- ═══════════════════════════════════════════════════════════════════


-- ─────────────────────────────────────────
-- 0. TABLO YAPISI (isteğe bağlı — CSV'yi buraya yükleyin)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS inventory (
    Product_Name     TEXT,
    Initial_Stock    INTEGER,
    Daily_Sales_Rate INTEGER,
    Lead_Time_Days   INTEGER,
    Unit_Cost        NUMERIC(10,2),
    Ordering_Cost    NUMERIC(10,2),
    Holding_Cost     NUMERIC(10,2)
);

-- Örnek veri girişi (CSV zaten yüklüyse bu bloğu atlayın)
INSERT INTO inventory VALUES
  ('White Sugar 1kg',   101, 14, 4,  12.68, 33.96,  2.54),
  ('Black Tea 500g',    118, 10, 1, 128.45, 27.67, 25.69),
  ('Sunflower Oil 1L',  171,  6, 2, 148.19, 37.05, 29.64),
  ('Wheat Flour 2kg',   142,  3, 3,  44.03, 32.05,  8.81),
  ('Rice 1kg',          163,  4, 5,  17.79, 37.49,  3.56),
  ('Lentils 1kg',       140,  9, 4,  21.03, 25.19,  4.21),
  ('Pasta 500g',        149, 15, 5, 121.24, 33.04, 24.25),
  ('Tomato Paste 830g', 180, 10, 2,  36.06, 42.06,  7.21),
  ('Salt 750g',         186,  4, 3,  61.92, 48.30, 12.38),
  ('Coffee 100g',       126,  4, 5,  28.86, 27.90,  5.77),
  ('Milk 1L',           175, 11, 1,  67.68, 35.61, 13.54),
  ('Butter 250g',        76, 12, 3,  11.24, 46.29,  2.25),
  ('Eggs 15-pack',      136,  4, 2,  75.30, 36.95, 15.06),
  ('Cheese 500g',       108,  5, 3,  83.21, 46.83, 16.64),
  ('Olive Oil 1L',      139, 10, 5,  38.80, 46.60,  7.76);


-- ─────────────────────────────────────────────────────────────────────
-- TABLO 1 — STOK HESAPLAMA SONUÇLARI
-- Formüller:
--   LTD = d × L
--   σd  = 0.20 × d
--   SS  = 1.645 × σd × √L
--   ROP = LTD + SS
--   D   = d × 365
--   EOQ = √(2 × D × S / H)
-- ─────────────────────────────────────────────────────────────────────
WITH calculations AS (
    SELECT
        Product_Name,
        Initial_Stock,
        Daily_Sales_Rate                                              AS d,
        Lead_Time_Days                                                AS L,
        Unit_Cost,
        Ordering_Cost                                                 AS S,
        Holding_Cost                                                  AS H,

        -- LTD: Sipariş Teslim Süresi Talebi
        Daily_Sales_Rate * Lead_Time_Days                             AS LTD,

        -- σd: Günlük talep standart sapması
        0.20 * Daily_Sales_Rate                                       AS sigma_d,

        -- SS: Emniyet Stoğu
        ROUND(1.645 * (0.20 * Daily_Sales_Rate) * SQRT(Lead_Time_Days), 1)
                                                                      AS SS,

        -- ROP: Yeniden Sipariş Noktası
        ROUND(
            Daily_Sales_Rate * Lead_Time_Days
            + 1.645 * (0.20 * Daily_Sales_Rate) * SQRT(Lead_Time_Days)
        , 0)                                                          AS ROP,

        -- D: Yıllık talep
        Daily_Sales_Rate * 365                                        AS D_annual,

        -- EOQ: Ekonomik Sipariş Miktarı
        ROUND(
            SQRT(2.0 * (Daily_Sales_Rate * 365) * Ordering_Cost / Holding_Cost)
        , 0)                                                          AS EOQ
    FROM inventory
),

-- TC (Toplam Yıllık Maliyet) ayrı CTE — EOQ'ya bağımlı
final AS (
    SELECT
        *,
        -- TC = D×P + (D/EOQ)×S + (EOQ/2)×H
        ROUND(
            D_annual * Unit_Cost
            + (D_annual / EOQ) * S
            + (EOQ / 2.0) * H
        , 0)                                                          AS TC,

        -- Tampon = Başlangıç Stok – ROP
        Initial_Stock - ROP                                           AS Buffer,

        -- ROP'a kalan gün
        ROUND((Initial_Stock - ROP) * 1.0 / d, 0)                    AS Days_to_ROP,

        -- Durum
        CASE WHEN Initial_Stock >= ROP THEN 'Yeterli' ELSE 'Kritik' END AS Status
    FROM calculations
)


-- ─────────────────────────────────────────
-- TABLO 1 — Stok Hesaplama Özeti
-- ─────────────────────────────────────────
SELECT
    Product_Name,
    Initial_Stock  AS "Başlangıç Stok",
    d              AS "d (adet/gün)",
    L              AS "L (gün)",
    SS,
    ROP,
    EOQ,
    Status         AS "Stok Durumu"
FROM final
ORDER BY Product_Name;


-- ─────────────────────────────────────────
-- TABLO 2 — Detaylı Hesaplamalar
-- ─────────────────────────────────────────
SELECT
    Product_Name,
    d,
    L,
    LTD,
    SS,
    ROP,
    D_annual       AS "D (yıllık)",
    S              AS "S (₺)",
    H              AS "H (₺)",
    EOQ
FROM final
ORDER BY Product_Name;


-- ─────────────────────────────────────────
-- TABLO 3 — Stok Durum Analizi
-- ─────────────────────────────────────────
SELECT
    Product_Name,
    Initial_Stock         AS "Başlangıç Stok",
    ROP,
    Buffer                AS "Stok – ROP (Tampon)",
    Days_to_ROP           AS "ROP'a Kalan Gün",
    TC                    AS "Toplam Yıllık Maliyet (₺)",
    Status                AS "Durum"
FROM final
ORDER BY Days_to_ROP ASC;


-- ─────────────────────────────────────────
-- TABLO 4 — Öncelikli İzleme Listesi
--           (ROP'a ≤ 11 gün kalanlar)
-- ─────────────────────────────────────────
SELECT
    Product_Name,
    Initial_Stock         AS "Mevcut Stok",
    ROP,
    Buffer                AS "Tampon",
    Days_to_ROP           AS "ROP'a Kalan",
    SS                    AS "Emniyet Stoğu"
FROM final
WHERE Days_to_ROP <= 11
ORDER BY Days_to_ROP ASC;


-- ─────────────────────────────────────────
-- ÖZET: En kritik metrikler
-- ─────────────────────────────────────────
SELECT
    MAX(ROP)    AS "En Yüksek ROP",
    (SELECT Product_Name FROM final ORDER BY ROP DESC LIMIT 1)
                AS "En Yüksek ROP Ürünü",

    MAX(EOQ)    AS "En Yüksek EOQ",
    (SELECT Product_Name FROM final ORDER BY EOQ DESC LIMIT 1)
                AS "En Yüksek EOQ Ürünü",

    MIN(Days_to_ROP)
                AS "ROP'a En Yakın (gün)",
    (SELECT Product_Name FROM final ORDER BY Days_to_ROP ASC LIMIT 1)
                AS "ROP'a En Yakın Ürün",

    MAX(TC)     AS "En Yüksek Yıllık Maliyet (₺)",
    (SELECT Product_Name FROM final ORDER BY TC DESC LIMIT 1)
                AS "En Yüksek Maliyet Ürünü"
FROM final;
